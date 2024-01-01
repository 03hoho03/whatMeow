from app.model import Follow


async def find_followings_by_user_id(id, db):
    return db.query(Follow).filter_by(fromUserId=id).all()


async def find_followers_by_user_id(id, db):
    return db.query(Follow).filter_by(toUserId=id).all()


async def make_toUserId_subquery(fromUserId, db):
    return db.query(Follow.toUserId).filter(Follow.fromUserId == fromUserId).subquery()


async def apply_follow_request_by_toUser_id(fromUserId, toUserId, toUsers, db):
    follow = db.query(Follow).filter_by(fromUserId=fromUserId, toUserId=toUserId).first()
    if follow:
        db.delete(follow)
        return {"isFollowing": False, "followerCount": len(toUsers) - 1}
    else:
        newFollow = Follow(fromUserId=fromUserId, toUserId=toUserId)
        db.add(newFollow)
        return {"isFollowing": True, "followerCount": len(toUsers) + 1}
