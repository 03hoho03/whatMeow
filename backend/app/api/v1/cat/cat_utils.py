import io
from fastapi import HTTPException, status

from app import model
from app.config import settings

from sqlalchemy.orm.exc import NoResultFound


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


async def cat_add_utils(db, image, data, user_id):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        image_path = await save_cat_image(image, user_row.username, data["catname"])
        row = model.Cat(**data, owner_id=user_id, image=image_path)
        db.add(row)
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured")


async def cat_update_utils(db, image, data, user_id):
    try:
        row = db.query(model.Cat).filter_by(id=data["id"]).first()
        if image is not None:
            try:
                user_row = db.query(model.User).filter_by(id=user_id).first()
                settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"{user_row.username}/{row.catname}.jpg")
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while deleting cat pic"
                )
            try:
                catname = row.catname if data["catname"] is None else data["catname"]
                await save_cat_image(image, user_row.username, catname)
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while uploading cat pic"
                )
        for key, value in data.items():
            if value is not None:
                setattr(row, key, value)
        db.commit()
        return True
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No Cat Found.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured.")
