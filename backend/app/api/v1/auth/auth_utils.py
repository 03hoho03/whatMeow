import random
import string

from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError


from app.config import settings
from app.api.schemas import user_schema
from app import model


async def set_cookie_response(response, token_info):
    response.set_cookie(
        key="accessToken", samesite="None", value=token_info.get("access_token"), httponly=True, secure=True
    )
    response.set_cookie(
        key="refreshToken", samesite="None", value=token_info.get("refresh_token"), httponly=True, secure=True
    )
    return response


async def get_random_username(db):
    letters = string.ascii_letters
    while True:
        random_string = "".join(random.choice(letters) for _ in range(8))
        if not db.query(model.User).filter_by(username=random_string).first():
            return random_string


async def get_random_nickname(db):
    while True:
        random_constant = random.randint(10000000, 99999999)
        random_nickname = "집사_" + str(random_constant)
        if not db.query(model.User).filter_by(nickname=random_nickname).first():
            return random_nickname


async def create_user_dict(user):
    return {
        "email": user.email,
        "nickname": user.nickname,
        "name": user.name,
        "profile_image": user.profile_image,
        "id": user.id,
    }


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
    user = db.query(model.User).filter_by(id=user_access_info.id).first()
    user_dict = await create_user_dict(user)
    if existing_user:
        db.delete(existing_user)
        db.commit()

    row = model.RefreshToken(**{"refresh_token": refresh_token, "user_id": user_access_info.id})
    db.add(row)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "user": user_dict}


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
    user = db.query(model.User).filter_by(id=user_access_info.id).first()
    user_dict = await create_user_dict(user)
    if existing_user:
        db.delete(existing_user)
        db.commit()

    row = model.RefreshToken(**{"refresh_token": refresh_token, "user_id": user_access_info.id})
    db.add(row)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "user": user_dict}


async def verify_access_token(token):
    """
    입력한 액세스 토큰이 만료되었는지 아닌지 체크하는 함수
    만료되었다면 401 반환
    """
    try:
        jwt_dict = jwt.decode(token, settings.SECRET_ACCESS_KEY, settings.ALGORITHM)
        if jwt_dict:
            return jwt_dict
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired")
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An Error Occured")


async def return_user_from_refresh_token(token, db):
    """
    cred 정보를 받아 refresh_token 정보를 반환해주는 함수
    """
    return db.query(model.RefreshToken).filter_by(refresh_token=token).first()


async def verify_refesh_token(token, db, exp: Optional[timedelta] = None):
    """
    입력한 리프레쉬 토큰이 만료되었는지 아닌지 체크하는 함수
    만료되지 않았다면 access_token 갱신해서 return
    만료되었다면 401 토큰 반환 후 refresh_token 삭제
    프론트측에서는 여기서 바로 로그인화면에서 redirect 해줌
    """
    rf_token = await return_user_from_refresh_token(token, db)
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


async def upload_default_image(image, username, nickname):
    obj_path = f"{username}/{nickname}.jpg"
    settings.s3.upload_file(image, settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"})
    return obj_path
