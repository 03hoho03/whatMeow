from datetime import datetime, timedelta
from app.config import settings
from app.api.schemas import user_schema
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app import model


def get_username(db, email):
    user = db.query(model.User).filter(model.User.email == email).first()

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

    existing_user = db.query(model.RefreshToken).filter_by(user_id=user_access_info.id).first()

    if existing_user:
        db.delete(existing_user)
        db.commit()

    row = model.RefreshToken(**{"refresh_token": refresh_token, "user_id": user_access_info.id})
    db.add(row)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}


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

    existing_user = db.query(model.RefreshToken).filter_by(user_id=user_access_info.id).first()

    if existing_user:
        db.delete(existing_user)
        db.commit()

    row = model.RefreshToken(**{"refresh_token": refresh_token, "user_id": user_access_info.id})
    db.add(row)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}


async def verify_access_token(cred):
    """
    입력한 액세스 토큰이 만료되었는지 아닌지 체크하는 함수
    만료되었다면 401 반환
    """
    token = cred.credentials
    try:
        jwt_dict = jwt.decode(token, settings.SECRET_ACCESS_KEY, settings.ALGORITHM)
        if jwt_dict:
            return jwt_dict
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired")


async def return_user_from_refresh_token(cred, db):
    """
    cred 정보를 받아 refresh_token 정보를 반환해주는 함수
    """
    token = cred.credentials
    return db.query(model.RefreshToken).filter_by(refresh_token=token).first()


async def verify_refesh_token(cred, db, exp: Optional[timedelta] = None):
    """
    입력한 리프레쉬 토큰이 만료되었는지 아닌지 체크하는 함수
    만료되지 않았다면 access_token 갱신해서 return
    만료되었다면 401 토큰 반환 후 refresh_token 삭제
    프론트측에서는 여기서 바로 로그인화면에서 redirect 해줌
    """
    token = cred.credentials
    rf_token = await return_user_from_refresh_token(cred, db)
    try:
        if jwt.decode(token, settings.SECRET_REFRESH_KEY, settings.ALGORITHM):
            """
            Access Token 갱신 후에 Access Token 반환
            """
            access_expire = datetime.utcnow() + (exp or timedelta(days=1))
            user_access_info = user_schema.UserPayload(**rf_token.user.__dict__, exp=access_expire)
            access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)
            return access_token
    except ExpiredSignatureError:
        """
        DB에서 refresh_token 삭제
        """
        db.delete(rf_token)
        db.commit()

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired")
