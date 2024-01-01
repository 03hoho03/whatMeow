from app.config import settings


async def make_detailed_cat(cat, user, tokenUserId, posts):
    _dict = {
        "owner": {"nickname": user.nickname, "isOwner": True if cat.ownerId == tokenUserId else False},
        "name": cat.catName,
        "explain": cat.explain,
        "breed": cat.breed,
        "gender": cat.gender,
        "image": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{cat.image}",
        "posts": [
            {
                "post_id": post.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/post/{post.uploaderId}/{post.id}/0.jpg",
            }
            for post in posts
        ],
    }

    return _dict
