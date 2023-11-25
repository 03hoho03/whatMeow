from fastapi import HTTPException

from app import model


async def add_like(post_id, user_id, db):
    try:
        post_row = db.query(model.Post).filter_by(id=post_id).first()
        for like in post_row.likes:
            if like.owner_id == user_id:
                like_row = db.query(model.Like).filter_by(owner_id=user_id).first()
                db.delete(like_row)
                db.commit()
                return "UNLIKE", len(post_row.likes)

        like_row = model.Like(owner_id=user_id, post_id=post_id)
        db.add(like_row)
        db.commit()

        return "LIKE", len(post_row.likes)
    except Exception as e:
        print(f"An error occured : {e}")
        return "FAIL", 0


async def is_like(post_id, user_id, db):
    try:
        post_row = db.query(model.Post).filter_by(id=post_id).first()
        status = False
        for like in post_row.likes:
            if like.owner_id == user_id:
                status = True

        return status
    except Exception as e:
        print(e)
        raise HTTPException(422)
