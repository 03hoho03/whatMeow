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


async def update_user_info(image, data, user_id, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        if image is not None:
            try:
                settings.s3.delete_object(
                    Bucket=settings.BUCKET_NAME, Key=f"{user_row.username}/{user_row.nickname}.jpg"
                )
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while deleting cat pic"
                )
            try:
                nickname = user_row.nickname if data["nickname"] is None else data["nickname"]
                new_url = await save_user_image(image, user_row.username, nickname)
                user_row.profile_image = new_url
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while uploading cat pic"
                )
        for key, value in data.items():
            if value is not None:
                setattr(user_row, key, value)
        db.commit()
        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An Error Occured")


async def load_mypage_utils(user_id, db):
    try:
        user_row = (
            db.query(model.User)
            .options(
                joinedload(model.User.posts),
                joinedload(model.User.cats),
                joinedload(model.User.following),
                joinedload(model.User.follower),
            )
            .filter_by(id=user_id)
            .first()
        )

        to_return_dict = {
            "nickname": user_row.nickname,
            "profile_image": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{user_row.profile_image}",
            "post_length": len(user_row.posts),
            "follower_length": len(user_row.follower),
            "following_length": len(user_row.following),
            "cats": [{"catname": cat.catname, "image": cat.image} for cat in user_row.cats],
        }

        return to_return_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An error occured while returning user my page"
        )
