from app import model


async def add_like(post_id, user_id, db):
    try:
        post_row = db.query(model.Post).filter_by(id=post_id).first()
        for like in post_row.likes:
            if like.owner_id == user_id:
                like_row = db.query(model.Like).filter_by(owner_id=user_id).first()
                db.delete(like_row)
                db.commit()
                return "unlike"

        like_row = model.Like(owner_id=user_id, post_id=post_id)
        db.add(like_row)
        db.commit()

        return "like"
    except Exception as e:
        print(f"An error occured : {e}")
        return "fail"
