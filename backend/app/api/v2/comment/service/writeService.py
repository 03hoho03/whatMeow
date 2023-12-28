from ..utils import databases


async def createComment(userId, postId, data, db):
    comment = await databases.create_comment(userId, postId, data.comment, db)
    db.commit()

    return comment


async def deleteComment(userId, commentId, db):
    if await databases.delete_comment(userId, commentId, db):
        db.commit()


async def updateComment(userId, commentId, data, db):
    comment = await databases.update_comment(userId, commentId, data.comment, db)
    db.commit()

    return comment
