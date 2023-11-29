import io
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.api.v1.user import user_utils
from app.api.v1.like import like_utils
from app.config import settings
from app import model


async def return_hashtag_ids(db, name_lst):
    hashtag_lst = []
    hashtag_id_lst = []
    for name in name_lst:
        val = name.split(" ")
        if len(val) == 1:
            hashtag_lst.append(val)
        else:
            for v in val:
                hashtag_lst.append(v)

    for hashtag in hashtag_lst:
        existing_hashtag = db.query(model.HashTag).filter_by(hashtag=hashtag).first()
        if existing_hashtag:
            hashtag_id = existing_hashtag.id
        else:
            new_hashtag = model.HashTag(hashtag=hashtag)
            db.add(new_hashtag)
            db.commit()
            hashtag_id = new_hashtag.id

        hashtag_id_lst.append(hashtag_id)

    return hashtag_id_lst


async def insert_posthashtags(db, hashtag_id_lst, row_id):
    for hashtag_id in hashtag_id_lst:
        db.execute(model.post_hashtags.insert().values(post_id=row_id, hashtag_id=hashtag_id))
        db.commit()


async def save_thumnail(username, file_obj, row_id):
    thumnail_path = f"thumnail/{username}/{row_id}.jpg"
    resized_image = await user_utils.image_to_thumnail(file_obj)
    in_mem_file = io.BytesIO()
    resized_image.save(in_mem_file, format="jpeg")
    in_mem_file.seek(0)
    settings.s3.upload_fileobj(
        in_mem_file, settings.BUCKET_NAME, thumnail_path, ExtraArgs={"ContentType": "image/jpeg"}
    )


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
    if username == post_row.post_owner.username:
        if post_row is None:
            raise HTTPException(status_code=404, detail="Post Not Found.")
        db.delete(post_row)

        # S3에서 객체 지우기
        objects_to_del = settings.s3.list_objects(Bucket=settings.BUCKET_NAME, Prefix=f"{username}/{post_id}/")
        if "Contents" in objects_to_del:
            for obj in objects_to_del["Contents"]:
                settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=obj["Key"])
        db.commit()
        return True
    else:
        return False


async def return_detailed_post(db, user_id, post_id):
    try:
        post = (
            db.query(model.Post)
            .options(
                joinedload(model.Post.likes),
                joinedload(model.Post.hashtags),
                joinedload(model.Post.images),
                joinedload(model.Post.comments),
                joinedload(model.Post.post_owner),
            )
            .filter_by(id=post_id)
            .first()
        )
        stat = False
        if not user_id:
            stat = await like_utils.is_like(post.id, user_id, db)

        to_return = {
            "nickname": post.post_owner.nickname,
            "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{post.post_owner.profile_image}",
            "postId": post_id,
            "like": {"count": len(post.likes), "isLike": stat},
            "content": post.title,
            "createdAt": post.created_at,
            "images": [
                f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image.url}" for image in post.images
            ],
            "hashtags": [hashtag.hashtag for hashtag in post.hashtags],
            "comments": [
                {
                    "commentId": comment.id,
                    "comment": comment.comment,
                    "nickname": comment.comment_owner.nickname,
                    "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{comment.comment_owner.profile_image}",
                }
                for comment in post.comments
            ],
        }

        return to_return
    except NoResultFound:
        return None


async def insert_postcats(db, cat_id_lst, post_id):
    for cat_id in cat_id_lst:
        db.execute(model.post_cats.insert().values(post_id=post_id, cat_id=cat_id))
        db.commit()
