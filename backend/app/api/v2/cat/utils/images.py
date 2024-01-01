import io

from fastapi import HTTPException, status
from PIL import Image

from app.config import settings


async def upload_cat_thumnail(obj_path, file):
    async def image_to_thumnail(image):
        image = Image.open(image.file)
        rgb_img = image.convert("RGB")
        resized_image = rgb_img.resize((200, 200))

        return resized_image

    try:
        resized_image = await image_to_thumnail(file)
        in_mem_file = io.BytesIO()
        resized_image.save(in_mem_file, format="jpeg")
        in_mem_file.seek(0)
        thunmnail_path = f"thumnail/{obj_path}"
        settings.s3.upload_fileobj(
            in_mem_file, settings.BUCKET_NAME, thunmnail_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while upload_post_thumnail")


async def upload_cat_image(catId, image):
    try:
        content_type = image.content_type
        if content_type.startswith("image/"):
            obj_path = f"cat/{catId}/cat.jpg"
            content = await image.read()
            settings.s3.upload_fileobj(
                io.BytesIO(content), settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
            )

            return obj_path

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while upload_post_images")
