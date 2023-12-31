from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.responses import RedirectResponse
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


@router.get("/google/callback")
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
        db_user_info = db.query(model.User).filter_by(email=result.get("email")).first()

        if db_user_info:
            token_info = await auth_utils.social_create_access_token(db_user_info, db, exp=timedelta(minutes=720))
            user_info = token_info.get("user")
            _nickname = user_info.get("nickname")
            cookie_response = RedirectResponse(url=f"https://www.whatmeow.shop/?nickname={_nickname}")
            cookie_response = await auth_utils.set_cookie_response(cookie_response, token_info)

            return cookie_response
        else:
            # 유저 정보가 존재하지 않는다면?
            # 유저 정보 저장
            try:
                nickname = await auth_utils.get_random_nickname(db)
                username = await auth_utils.get_random_username(db)
                try:
                    url = await auth_utils.upload_default_image(username)
                except Exception as e:
                    print(e)
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="An Error Occured while Uploading default Image",
                    )
                user_row = model.User(
                    **{
                        "name": result.get("name"),
                        "email": result.get("email"),
                        "profile_image": url,
                        "nickname": nickname,
                        "username": username,
                    }
                )

                db.add(user_row)
                db.commit()

                user = db.query(model.User).filter(model.User.nickname == user_row.nickname).first()
                token_info = await auth_utils.social_create_access_token(user, db, exp=timedelta(minutes=720))
                cookie_response = RedirectResponse(url=f"https://www.whatmeow.shop/?nickname={nickname}")
                cookie_response = await auth_utils.set_cookie_response(cookie_response, token_info)

                return cookie_response
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email duplicated")
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An Error Occured while registering"
                )
