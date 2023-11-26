import io
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

from app.config import settings
from app import model


async def check_duplication(nickname, db):
    try:
        db.query(model.User).filter_by(nickname=nickname).first()
        return False
    except NoResultFound:
        return True


async def save_user_image(image, username, nickname):
    content_type = image.content_type
    if content_type.startswith("image/"):
        obj_path = f"{username}/{nickname}.jpg"
        content = await image.read()
        settings.s3.upload_fileobj(
            io.BytesIO(content), settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
        return obj_path
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Upload Cat Image to Bucket"
        )


async def update_image(user_id, image, db):
    user_row = db.query(model.User).filter_by(id=user_id).first()
    try:
        settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"{user_row.username}/{user_row.nickname}.jpg")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while deleting cat pic"
        )
    try:
        new_url = await save_user_image(image, user_row.username, user_row.nickname)
        user_row.profile_image = new_url
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while uploading cat pic"
        )
    db.commit()

    return True


async def update_nickname(user_id, nickname, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        user_row.nickname = nickname
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} occured")


async def update_name(user_id, name, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        user_row.name = name
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} occured")


async def update_explain(user_id, explain, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        user_row.explain = explain
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} Occured")


async def load_mypage_utils(nickname, my_id, db):
    try:
        user_row = (
            db.query(model.User)
            .options(
                joinedload(model.User.posts),
                joinedload(model.User.cats),
                joinedload(model.User.following),
                joinedload(model.User.follower),
            )
            .filter_by(nickname=nickname)
            .first()
        )

        my_row = db.query(model.User).filter_by(id=my_id).first()
        if user_row.id == my_id:
            relation = "ME"
        else:
            relation = "UNFOLLOW"
            for following in my_row.following:
                if user_row.id == following.id:
                    relation = "FOLLOW"

        to_return_dict = {
            "userId": user_row.id,
            "nickname": user_row.nickname,
            "profileImage": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{user_row.profile_image}",
            "postCount": len(user_row.posts),
            "followerCount": len(user_row.follower),
            "followingCount": len(user_row.following),
            "cats": [{"catName": cat.catname, "thumnail": cat.image} for cat in user_row.cats],
            "posts": [
                {
                    "postId": post.id,
                    "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{post.images[0].url}",
                }
                for post in user_row.posts
            ],
            "relation": relation,
        }

        return to_return_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An error occured while returning user my page"
        )
