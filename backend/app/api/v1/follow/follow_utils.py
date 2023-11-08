from app import model
from sqlalchemy.orm.exc import NoResultFound


async def add_follow(follow_id, user_id, db):
    if db.execute(model.followers.insert().values(follower_id=user_id, following_id=follow_id)):
        db.commit()
        return True
    else:
        return False


async def delete_follow(unfollow_id, user_id, db):
    try:
        db.query(model.followers).filter(
            model.followers.c.follower_id == user_id, model.followers.c.following_id == unfollow_id
        ).delete(synchronize_session=False)

        db.commit()
        return True
    except NoResultFound:
        return False
