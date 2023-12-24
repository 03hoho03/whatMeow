import io

from fastapi import HTTPException, status
from PIL import Image

from app.config import settings


async def upload_post_thumnail(username, postId, file):
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
        thunmnail_path = f"post/{username}/{postId}/thumnail.jpg"
        settings.s3.upload_fileobj(
            in_mem_file, settings.BUCKET_NAME, thunmnail_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while upload_post_thumnail")


async def upload_post_images(username, postId, files):
    try:
        images = []
        for i, file_obj in enumerate(files):
            content_type = file_obj.content_type
            if content_type.startswith("image/"):
                obj_path = f"post/{username}/{postId}/{i}.jpg"
                content = await file_obj.read()
                settings.s3.upload_fileobj(
                    io.BytesIO(content), settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
                )
                images.append(obj_path)

        return images
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while upload_post_images")
