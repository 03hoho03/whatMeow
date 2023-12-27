from ..utils import databases


async def createComment(userId, postId, data, db):
    comment = await databases.create_comment(userId, postId, data.comment, db)
    db.commit()

    return comment
