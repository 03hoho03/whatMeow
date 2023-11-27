from app import model
from fastapi import HTTPException, status


async def add_follow(follow_nickname, user_id, db):
    check_row = db.query(model.User).filter_by(nickname=follow_nickname).first()
    for follower in check_row.follower:
        if follower.id == user_id:
            try:
                db.query(model.followers).filter(
                    model.followers.c.follower_id == user_id, model.followers.c.following_id == check_row.id
                ).delete(synchronize_session=False)
                db.commit()

                return "UNFOLLOW", len(check_row.follower)
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} occured while unfollowing"
                )
    db.execute(model.followers.insert().values(follower_id=user_id, following_id=check_row.id))
    db.commit()

    return "FOLLOW", len(check_row.follower)
