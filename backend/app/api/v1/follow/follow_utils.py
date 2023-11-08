from app import model


async def add_follow(follow_id, user_id, db):
    if db.execute(model.followers.insert().values(follower_id=user_id, following_id=follow_id)):
        db.commit()
        return True
    else:
        return False
