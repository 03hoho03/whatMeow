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
    refresh_expire = datetime.utcnow() + timedelta(days=14)
    user_access_info = UserPayload(**user.__dict__, exp=access_expire)
    user_refresh_info = UserPayload(**user.__dict__, exp=refresh_expire)

    access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(user_refresh_info.dict(), settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": access_token, "refresh_token": refresh_token}
