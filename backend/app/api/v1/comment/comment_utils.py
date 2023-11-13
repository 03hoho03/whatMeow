from app import model
from sqlalchemy.orm.exc import NoResultFound


async def upload_comment(comment, post_id, user_id, db):
    try:
        row = model.Comment(comment=comment, uploader=user_id, post_id=post_id)
        db.add(row)
        db.commit()
        return True
    except Exception:
        return False


async def delete_comment(comment_id, post_id, user_id, db):
    try:
        c_row = db.query(model.Comment).filter_by(id=comment_id, post_id=post_id, uploader=user_id).first()
        db.delete(c_row)
        db.commit()
        return True
    except NoResultFound:
        return False


async def update_comment(new_comment, comment_id, post_id, user_id, db):
    try:
        c_row = db.query(model.Comment).filter_by(id=comment_id, post_id=post_id, uploader=user_id).first()
        c_row.comment = new_comment
        db.commit()
        return True
    except NoResultFound:
        return False
