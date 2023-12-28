from app.model import Follow


async def find_followings_by_user_id(id, db):
    return db.query(Follow).filter_by(fromUserId=id).all()


async def find_followers_by_user_id(id, db):
    return db.query(Follow).filter_by(toUserId=id).all()
