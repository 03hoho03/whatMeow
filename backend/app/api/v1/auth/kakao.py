from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

from app.api.v1.auth import auth_utils
from app.config import settings
from app import model
from app.database import get_db


router = APIRouter(tags=["Auth"])


@router.get("/kakao")
def kakao():
    redirect_url = f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}&redirect_uri={settings.KAKAO_REDIRECT_URI}&response_type=code"
    return RedirectResponse(url=redirect_url)


@router.get("/kakao_login")
async def kakao_login(
    cookie_response: Response,
    code: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    db: Session = Depends(get_db),
):
    async with httpx.AsyncClient() as client:
        # KaKao 토큰 발급
        response = await client.post(
            url="https://kauth.kakao.com/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "charset": "utf-8",
                "Cache-Control": "no-cache",
            },
            data={
                "grant_type": "authorization_code",
                "client_id": str(settings.KAKAO_CLIENT_ID),
                "client_secret": str(settings.KAKAO_CLIENT_SECRET),
                "redirect_uri": str(settings.KAKAO_REDIRECT_URI),
                "code": str(code),
            },
        )
        response = response.json()
        # 토큰으로 유저 정보 획득
        access_token = response.get("access_token")
        result = await client.post(
            url="https://kapi.kakao.com/v2/user/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
                "Authorization": "Bearer " + access_token,
            },
            data={},
        )
        result = result.json()
        _property = result.get("properties")
        _profile = result.get("kakao_account")
        db_user_info = auth_utils.get_username(db, "kakao_" + str(result.get("id")))

        if db_user_info:
            return await auth_utils.social_create_access_token(db_user_info, db, exp=timedelta(minutes=720))
        else:
            # 유저 정보가 존재하지 않는다면?
            # 유저 정보 저장
            try:
                user_row = model.User(
                    **{
                        "name": _property.get("nickname"),
                        "email": _profile.get("email", None),
                        "gender": _profile.get("gender", None),
                        "profile_image": _property.get("profile_image"),
                        "nickname": await auth_utils.get_random_nickname(db),
                    }
                )

                db.add(user_row)
                db.commit()

                user = db.query(model.User).filter(model.User.nickname == user_row.nickname).first()
                token_info = await auth_utils.social_create_access_token(user, db, exp=timedelta(minutes=720))
                cookie_response = JSONResponse(content=token_info.get("user"))
                cookie_response = await auth_utils.set_cookie_response(cookie_response, token_info)

                return cookie_response
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email Duplicated")
