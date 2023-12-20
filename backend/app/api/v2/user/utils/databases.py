import string
import random

from app.model import User


async def add_generaluser(data, username, url, password, db):
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


async def get_random_username(db):
    letters = string.ascii_letters
    while True:
        random_string = "".join(random.choice(letters) for _ in range(8))
        if not db.query(User).filter_by(username=random_string).first():
            return random_string
