from app.config import settings


async def upload_default_image(username):
    obj_path = f"{username}/user.jpg"
    thumnail_path = f"thumnail/{username}/user.jpg"
    settings.s3.upload_file(
        "images/default.jpg", settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
    )
    settings.s3.upload_file(
        "images/default_thumnail.jpg", settings.BUCKET_NAME, thumnail_path, ExtraArgs={"ContentType": "image/jpeg"}
    )
    return obj_path
