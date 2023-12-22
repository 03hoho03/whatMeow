import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt

from app.config import settings
from ..schema import UserPayload


async def create_hashed_password(password):
    salt_value = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt_value)


async def is_password_correct(data, user):
    stat = bcrypt.checkpw(data.password.encode(), user.password.encode())
    if stat:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Information")


async def create_access_token(user):
    access_expire = datetime.utcnow() + timedelta(days=1)
    user_access_info = UserPayload(**user.__dict__, exp=access_expire)

    access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)

    return access_token


async def create_refresh_token(user):
    refresh_expire = datetime.utcnow() + timedelta(days=14)
    user_refresh_info = UserPayload(**user.__dict__, exp=refresh_expire)
    refresh_token = jwt.encode(user_refresh_info.dict(), settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    return refresh_token


async def get_google_redirect_uri():
    return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI_V2}&response_type=code&scope=openid email profile"


async def get_kakao_redirect_url():
    return f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}&redirect_uri={settings.KAKAO_REDIRECT_URI_V2}&response_type=code"
