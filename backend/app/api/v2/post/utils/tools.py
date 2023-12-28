from app.config import settings


async def make_detailed_post(post, user, images, hashtags):
    """
    필요한 것 : Post, Uploader(User), PostHashTag에서 추출한 HashTag
    """
    _dict = {
        "nickname": user.nickname,
        "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user.profileImage}",
        "postId": post.id,
        # Like, Comment는 리팩토링 X
        # 추후에 수정 예정
        "like": {"count": 0, "isLike": False},
        "content": post.title,
        "createdAt": post.createdAt,
        "images": [f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image.url}" for image in images],
        "hashtags": [hashtag.hashtag for hashtag in hashtags],
        "comments": [
            {
                "commentId": "commentId",
                "comment": "comment",
                "nickname": "comment_nickname",
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/user.jpg",
            }
        ],
    }

    return _dict
