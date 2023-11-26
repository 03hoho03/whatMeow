import io
from fastapi import HTTPException, status

from app import model
from app.config import settings
from app.api.v1.user import user_utils


async def save_cat_image(image, username, catname):
    content_type = image.content_type
    if content_type.startswith("image/"):
        obj_path = f"{username}/{catname}.jpg"
        content = await image.read()
        settings.s3.upload_fileobj(
            io.BytesIO(content), settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
        return obj_path
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Upload Cat Image to Bucket"
        )


async def save_cat_thumnail_image(image, username, catname):
    content_type = image.content_type
    if content_type.startswith("image/"):
        thumnail_path = f"thumnail/{username}/{catname}.jpg"
        resized_image = await user_utils.image_to_thumnail(image)
        in_mem_file = io.BytesIO()
        resized_image.save(in_mem_file, format="jpeg")
        in_mem_file.seek(0)
        settings.s3.upload_fileobj(
            in_mem_file, settings.BUCKET_NAME, thumnail_path, ExtraArgs={"ContentType": "image/jpeg"}
        )


async def cat_add_utils(db, image, catname, explain, user_id):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        image_path = await save_cat_image(image, user_row.username, catname)
        await save_cat_thumnail_image(image, user_row.username, catname)
        row = model.Cat(catname=catname, explain=explain, owner_id=user_id, image=image_path)
        db.add(row)
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} Occured")


async def cat_update_image(db, image, cat_id, user_id):
    row = db.query(model.Cat).filter_by(id=cat_id).first()
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"thumnail/{user_row.username}/{row.catname}.jpg")
        settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"{user_row.username}/{row.catname}.jpg")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while deleting cat pic"
        )
    try:
        new_url = await save_cat_image(image, user_row.username, row.catname)
        await save_cat_thumnail_image(image, user_row.username, row.catname)
        row.image = new_url
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while uploading cat pic"
        )
    return True


async def cat_change_image(username, oldname, newname):
    settings.s3.copy_object(
        Bucket=settings.BUCKET_NAME,
        CopySource={"Bucket": settings.BUCKET_NAME, "Key": f"thumnail/{username}/{oldname}.jpg"},
        Key=f"thumnail/{username}/{newname}.jpg",
    )
    settings.s3.copy_object(
        Bucket=settings.BUCKET_NAME,
        CopySource={"Bucket": settings.BUCKET_NAME, "Key": f"{username}/{oldname}.jpg"},
        Key=f"{username}/{newname}.jpg",
    )
    settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"thumnail/{username}/{oldname}.jpg")
    settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"{username}/{oldname}.jpg")


async def update_catname(cat_id, username, catname, db):
    try:
        cat_row = db.query(model.Cat).filter_by(id=cat_id).first()
        await cat_change_image(username, cat_row.catname, catname)
        cat_row.catname = catname
        db.commit()
        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} Occured.")


async def update_explain(cat_id, explain, db):
    try:
        cat_row = db.query(model.Cat).filter_by(id=cat_id).first()
        cat_row.explain = explain
        db.commit()
        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} Occured.")


async def cat_info(cat_id, username, db):
    try:
        cat_row = db.query(model.Cat).filter_by(id=cat_id).first()
        to_return_dict = {
            "name": cat_row.catname,
            "explain": cat_row.explain,
            "image": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{username}/{cat_row.catname}.jpg",
            "posts": [
                {
                    "post_id": post.id,
                    "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{username}/{post.id}.jpg",
                }
                for post in cat_row.posts
            ],
        }

        return to_return_dict
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} Occured.")
