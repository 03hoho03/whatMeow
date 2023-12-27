from app.model import Comment


async def create_comment(userId, postId, comment, db):
    comment = Comment(uploader=userId, postId=postId, comment=comment)
    db.add(comment)

    return comment
