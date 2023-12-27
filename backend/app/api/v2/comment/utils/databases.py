from fastapi import HTTPException, status

from app.model import Comment


async def create_comment(userId, postId, comment, db):
    comment = Comment(uploader=userId, postId=postId, comment=comment)
    db.add(comment)

    return comment


async def delete_comment(userId, commentId, db):
    comment = db.query(Comment).filter_by(id=commentId).first()
    if comment:
        if comment.id == userId:
            db.delete(comment)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong User Information")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comment with this ID")
