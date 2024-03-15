from app.config import settings


async def make_follow_list(users):
    _dict = [
        {
            "nickname": user.nickname,
            "userThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user.profileImage}",
        }
        for user in users
    ]

    return _dict
