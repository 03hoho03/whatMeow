from fastapi import HTTPException, status
from app.config import settings


async def upload_default_image(username):
    try:
        obj_path = f"user/{username}/user.jpg"
        thumnail_path = f"user/{username}/thumnail.jpg"
        settings.s3.upload_file(
            "images/default.jpg", settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
        settings.s3.upload_file(
            "images/default_thumnail.jpg", settings.BUCKET_NAME, thumnail_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
        return obj_path
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e}, upload_default_image")
