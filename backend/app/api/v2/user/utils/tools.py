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
    access_expire = datetime.now() + timedelta(days=1)
    user_access_info = UserPayload(**user.__dict__, exp=access_expire)

    access_token = jwt.encode(user_access_info.dict(), settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)

    return access_token


async def create_refresh_token(user):
    refresh_expire = datetime.now() + timedelta(days=14)
    user_refresh_info = UserPayload(**user.__dict__, exp=refresh_expire)
    refresh_token = jwt.encode(user_refresh_info.dict(), settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    return refresh_token


async def get_google_redirect_uri():
    return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI_V2}&response_type=code&scope=openid email profile"


async def get_kakao_redirect_url():
    return f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}&redirect_uri={settings.KAKAO_REDIRECT_URI_V2}&response_type=code"


async def make_return_dict(user, id, data):
    is_owner = True if user.id == id else False
    if id:
        follow = False
        for f in data["followers"]:
            if id == f.fromUserId:
                follow = True
                break
    else:
        follow = False

    _dict = {
        "userId": user.id,
        "nickname": user.nickname,
        "profileThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user.profileImage}",
        "postCount": len(data["posts"]),
        "explain": user.explain if user.explain else "",
        "follow": {
            "followerCount": len(data["followers"]),
            "followingCount": len(data["followings"]),
            "isFollowing": follow,
        },
        "cats": [
            {
                "catName": cat.catName,
                "catId": cat.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{cat.image}",
            }
            for cat in data["cats"]
        ],
        "posts": [
            {
                "postId": post.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/post/{user.id}/{post.id}/0.jpg",
            }
            for post in data["posts"]
        ],
        "owner": is_owner,
    }

    return _dict


async def make_cat_ids(cats):
    return [{"catId": cat.id, "catName": cat.catName} for cat in cats]
