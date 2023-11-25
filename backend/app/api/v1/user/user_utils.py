import io
from sqlalchemy.orm.exc import NoResultFound
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
                await save_user_image(image, user_row.username, nickname)
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
