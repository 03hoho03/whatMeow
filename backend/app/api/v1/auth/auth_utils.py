from datetime import datetime, timedelta
from app.config import settings
from app.api.schemas import user_schema
from typing import Optional
from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app import model


def get_username(db, username):
    user = db.query(model.User).filter(model.User.username == username).first()

    if not user:
        return None
    return user


async def general_create_access_token(
    data: user_schema.User,
    db,
    exp: Optional[timedelta] = None,
):
    """
    우리 서비스에 따로 가입한 유저에게 최초 토큰 발급
    """
    access_expire = datetime.utcnow() + (exp or timedelta(days=1))
    refresh_expire = datetime.utcnow() + (exp or timedelta(days=14))
    user_access_info = user_schema.UserPayload(**data.__dict__, exp=access_expire)
    user_refresh_info = user_schema.UserPayload(**data.__dict__, exp=refresh_expire)
    access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(user_refresh_info.dict(), settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    row = model.RefreshToken(**{"refresh_token": refresh_token, "user_id": user_access_info.id})
    db.add(row)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "expire": access_expire}


async def social_create_access_token(
    data: user_schema.User,
    db,
    exp: Optional[timedelta] = None,
):
    """
    소셜 로그인으로 서비스 가입한 유저에게 최초 토큰 발급
    """
    access_expire = datetime.utcnow() + (exp or timedelta(days=1))
    refresh_expire = datetime.utcnow() + (exp or timedelta(days=14))
    user_access_info = user_schema.UserPayload(**data.__dict__, exp=access_expire)
    user_refresh_info = user_schema.UserPayload(**data.__dict__, exp=refresh_expire)

    access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(user_refresh_info.dict(), settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    row = model.RefreshToken(**{"refresh_token": refresh_token, "user_id": user_access_info.id})
    db.add(row)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "expire": access_expire}


async def verify_user(cred):
    """
    입력한 토큰이 만료되었는지 아닌지 체크하는 함수
    만료되었다면 401 반환
    """
    token = cred.credentials
    try:
        if jwt.decode(token, settings.SECRET_ACCESS_KEY, settings.ALGORITHM):
            return True
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired")
