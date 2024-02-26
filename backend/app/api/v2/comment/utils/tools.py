from app.config import settings


async def make_comment_list(comments):
    return [
        {
            "commentId": comment.id,
            "comment": comment.comment,
            "nickname": comment.nickname,
            "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/user/{comment.uploader}/user.jpg",
            "uploader": comment.uploader,
            "createdAt": comment.createdAt,
        }
        for comment in comments
    ]
