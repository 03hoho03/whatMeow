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


@router.get("/google")
def google():
    redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid email profile"
    return RedirectResponse(url=redirect_url)


@router.get("/google_login")
async def google_login(
    cookie_response: Response,
    code: str | None = None,
    db: Session = Depends(get_db),
):
    async with httpx.AsyncClient() as client:
        # Google 토큰 발급
        response = await client.post(
            url="https://oauth2.googleapis.com/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "charset": "utf-8",
                "Cache-Control": "no-cache",
            },
            data={
                "grant_type": "authorization_code",
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "code": code,
            },
        )
        response = response.json()
        id_token = response.get("id_token")
        result = await client.get(
            url=f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}",
        )
        result = result.json()
        db_user_info = auth_utils.get_username(db, str(result.get("email")))

        if db_user_info:
            return await auth_utils.social_create_access_token(db_user_info, db, exp=timedelta(minutes=720))
        else:
            # 유저 정보가 존재하지 않는다면?
            # 유저 정보 저장
            try:
                user_row = model.User(
                    **{
                        "name": result.get("name"),
                        "email": result.get("email"),
                        "profile_image": result.get("picture"),
                        "nickname": await auth_utils.get_random_nickname(db),
                        "username": await auth_utils.get_random_username(db),
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
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email duplicated")
