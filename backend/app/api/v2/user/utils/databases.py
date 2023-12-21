import string
import random

from fastapi import HTTPException, status
from app.model import User, RefreshToken


async def add_generaluser(data, username, url, password, db):
    try:
        row = User(
            **{
                "email": data.email,
                "nickname": data.nickname,
                "name": data.name,
                "username": username,
                "profile_image": url,
                "password": password,
            }
        )

        db.add(row)
        db.commit()

        return row
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e}, add_generaluser")


async def get_random_username(db):
    letters = string.ascii_letters
    while True:
        random_string = "".join(random.choice(letters) for _ in range(8))
        if not db.query(User).filter_by(username=random_string).first():
            return random_string


async def find_user_by_email(email, db):
    row = db.query(User).filter_by(email=email).first()
    if row:
        return row
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Informaition")


async def update_refresh_token_info(user, token, db):
    exist = db.query(RefreshToken).filter_by(user_id=user.id).first()
    if exist:
        db.delete(exist)
    row = RefreshToken(**{"refresh_token": token["refresh_token"], "user_id": user.id})
    db.add(row)
    db.commit()


async def is_duplicated(nickname, db):
    row = db.query(User).filter_by(nickname=nickname).first()
    if row:
        return True
    else:
        return False
