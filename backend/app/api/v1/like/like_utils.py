from app import model
from sqlalchemy.orm.exc import NoResultFound


async def add_like(post_id, user_id, db):
    try:
        like_row = model.Like(owner_id=user_id, post_id=post_id)
        db.add(like_row)
        db.commit()
        return True
    except Exception:
        return False


async def unlike(post_id, user_id, db):
    try:
        unlike_row = db.query(model.Like).filter_by(owner_id=user_id, post_id=post_id).first()
        db.delete(unlike_row)
        db.commit()
        return True
    except NoResultFound:
        return False
