from fastapi import HTTPException, status

from app.model import Comment


async def create_comment(userId, nickname, postId, comment, db):
    comment = Comment(uploader=userId, nickname=nickname, postId=postId, comment=comment)
    db.add(comment)

    return comment


async def delete_comment(userId, commentId, db):
    comment = db.query(Comment).filter_by(id=commentId).first()
    if comment:
        if comment.uploader == userId:
            db.delete(comment)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong User Information")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comment with this ID")


async def update_comment(userId, commentId, newComment, db):
    comment = db.query(Comment).filter_by(id=commentId).first()
    if comment:
        if comment.uploader == userId:
            comment.comment = newComment
            return comment
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong User Information")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comment with this ID")
