import string
import random

from fastapi import HTTPException, status
from app.model import User


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


async def is_duplicated(nickname, db):
    row = db.query(User).filter_by(nickname=nickname).first()
    if row:
        return True
    else:
        return False
