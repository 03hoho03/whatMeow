import io
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.config import settings
from app import model


async def return_hashtag_ids(db, name_lst):
    hashtag_id_lst = []
    for name in name_lst:
        existing_hashtag = db.query(model.HashTag).filter_by(hashtag=name).first()
        if existing_hashtag:
            hashtag_id = existing_hashtag.id
        else:
            new_hashtag = model.HashTag(hashtag=name)
            db.add(new_hashtag)
            db.commit()
            hashtag_id = new_hashtag.id

        hashtag_id_lst.append(hashtag_id)

    return hashtag_id_lst


async def insert_posthashtags(db, hashtag_id_lst, row_id):
    for hashtag_id in hashtag_id_lst:
        db.execute(model.post_hashtags.insert().values(post_id=row_id, hashtag_id=hashtag_id))
        db.commit()


async def save_images(db, username, image_lst, row_id):
    # S3에 객체 업로드
    for i, file_obj in enumerate(image_lst):
        content_type = file_obj.content_type
        if content_type.startswith("image/"):
            obj_path = f"{username}/{row_id}/{i}.jpg"
            content = await file_obj.read()
            settings.s3.upload_fileobj(
                io.BytesIO(content), settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
            )
            row = model.Image(url=obj_path, post_id=row_id)
            db.add(row)

    db.commit()


async def post_delete(db, username, post_id):
    # DB에서 Post 관련 row 지우기
    post_row = db.query(model.Post).filter_by(id=post_id).first()
    if post_row is None:
        raise HTTPException(status_code=404, detail="Post Not Found.")
    db.delete(post_row)
    db.commit()

    # S3에서 객체 지우기
    objects_to_del = settings.s3.list_objects(Bucket=settings.BUCKET_NAME, Prefix=f"{username}/{post_id}/")
    if "Contents" in objects_to_del:
        for obj in objects_to_del["Contents"]:
            settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=obj["Key"])

    return True


async def return_detailed_post(db, post_id):
    try:
        post = (
            db.query(model.Post)
            .options(
                joinedload(model.Post.likes),
                joinedload(model.Post.comments),
                joinedload(model.Post.post_owner),
                joinedload(model.Post.hashtags),
                joinedload(model.Post.images),
            )
            .filter_by(id=post_id)
            .first()
        )
        return post
    except NoResultFound:
        return None
