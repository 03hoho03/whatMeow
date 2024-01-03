import random

from fastapi import HTTPException, status
from app.model import User, RefreshToken


async def add_generaluser(data, password, db):
    try:
        row = User(
            **{
                "email": data.email,
                "nickname": data.nickname,
                "name": data.name,
                "password": password,
            }
        )

        db.add(row)
        db.flush()

        return row
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e}, add_generaluser")


async def add_google_user(result, nickname, db):
    try:
        row = User(
            **{
                "name": result.get("name"),
                "email": result.get("email"),
                "nickname": nickname,
            }
        )

        db.add(row)
        db.flush()

        return row
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e}, add_google_user")


async def add_kakao_user(result, _property, _profile, nickname, db):
    try:
        row = User(
            **{
                "name": _property.get("nickname"),
                "kakaoId": result.get("id"),
                "email": _profile.get("email", None),
                "gender": _profile.get("gender", None),
                "nickname": nickname,
            }
        )

        db.add(row)
        db.flush()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e}, add_kakao_user")


async def get_random_nickname(db):
    while True:
        random_constant = random.randint(10000000, 99999999)
        random_nickname = "집사_" + str(random_constant)
        if not db.query(User).filter_by(nickname=random_nickname).first():
            return random_nickname


async def find_user_by_email(email, db):
    row = db.query(User).filter_by(email=email).first()
    if row:
        return row
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Informaition")


async def find_user_by_email_without_exception(email, db):
    return db.query(User).filter_by(email=email).first()


async def find_user_by_nickname(nickname, db):
    return db.query(User).filter_by(nickname=nickname).first()


async def find_user_by_kakao_id(id, db):
    return db.query(User).filter_by(kakaoId=id).first()


async def find_users_by_follow_subquery(subq, db):
    return db.query(User).filter(User.id.in_(subq)).all()


async def find_users_by_posts(posts, db):
    return [db.query(User).filter_by(id=post.uploaderId).first() for post in posts]


async def find_user_by_id(id, db):
    row = db.query(User).filter_by(id=id).first()
    if row:
        return row
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No User with {id}")


async def update_refresh_token_info(user, refresh_token, db):
    exist = db.query(RefreshToken).filter_by(userId=user.id).first()
    if exist:
        db.delete(exist)
    row = RefreshToken(**{"refresh_token": refresh_token, "userId": user.id})
    db.add(row)
    db.commit()


async def delete_refreshtoken_info(id, db):
    try:
        row = db.query(RefreshToken).filter_by(userId=id).first()
        db.delete(row)
        db.commit()

        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while deleting refreshtoken")


async def is_duplicated(nickname, db):
    row = db.query(User).filter_by(nickname=nickname).first()
    if row:
        return True
    else:
        return False
