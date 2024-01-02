from app.config import settings


async def make_detailed_post(post, user, images, hashtags, comments, statLike):
    """
    필요한 것 : Post, Uploader(User), PostHashTag에서 추출한 HashTag
    """
    _dict = {
        "nickname": user.nickname,
        "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user.profileImage}",
        "postId": post.id,
        "version": post.version,
        "like": {"count": post.likeCount, "isLike": statLike},
        "content": post.title,
        "createdAt": post.createdAt,
        "images": [f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image.url}" for image in images],
        "hashtags": [hashtag.hashtag for hashtag in hashtags],
        "comments": [
            {
                "commentId": comment.id,
                "comment": comment.comment,
                "nickname": comment.nickname,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/user/{comment.uploader}/user.jpg",
            }
            for comment in comments
        ],
    }

    return _dict
