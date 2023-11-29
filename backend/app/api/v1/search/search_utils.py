from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from app import model
from app.api.v1.like import like_utils
from app.config import settings


async def return_post_by_hashtag(db, lst):
    post_lst = []
    for post_id, _ in lst:
        post_item = db.query(model.Post).options(joinedload(model.Post.images)).filter_by(id=post_id).first()
        post_lst.append(
            {
                "postId": post_item.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{post_item.post_owner.username}/{post_item.id}.jpg",
            }
        )

    return post_lst


async def return_post_by_name(lst):
    post_lst = []
    for post_item in lst:
        post_lst.append(
            {
                "postId": post_item.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{post_item.post_owner.username}/{post_item.id}.jpg",
            }
        )

    return post_lst


async def append_following_ids(followings):
    following_ids = []
    for following in followings:
        following_ids.append(following.id)

    return following_ids


async def make_dict_from_follow_posts(latest_posts, user_id, db):
    to_return_lst = []
    for post in latest_posts:
        stat = await like_utils.is_like(post.id, user_id, db)
        to_return_lst.append(
            {
                "nickname": post.post_owner.nickname,
                "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{post.post_owner.profile_image}",
                "like": {"count": len(post.likes), "isLike": stat},
                "createdAt": post.created_at,
                "content": post.title,
                "postId": post.id,
                "images": [f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{post.images[0].url}"],
            }
        )

    return to_return_lst


async def return_follow_posts(db, user_id, start, limit):
    try:
        user = db.query(model.User).filter_by(id=user_id).first()
        following_ids = await append_following_ids(user.following)
        latest_posts = (
            db.query(model.Post)
            .options(
                joinedload(model.Post.likes),
                joinedload(model.Post.hashtags),
                joinedload(model.Post.images),
                joinedload(model.Post.post_owner),
            )
            .filter(model.Post.uploader_id.in_(following_ids))
            .order_by(desc(model.Post.created_at))
            .offset(start)
            .limit(limit)
            .all()
        )

        return await make_dict_from_follow_posts(latest_posts, user_id, db)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def make_dict_from_recent_posts(latest_posts, user_id, db):
    to_return_lst = []
    for post in latest_posts:
        stat = False
        if user_id:
            stat = await like_utils.is_like(post.id, user_id, db)
        to_return_lst.append(
            {
                "nickname": post.post_owner.nickname,
                "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{post.post_owner.profile_image}",
                "like": {"count": len(post.likes), "isLike": stat},
                "createdAt": post.created_at,
                "content": post.title,
                "postId": post.id,
                "images": [
                    f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image.url}"
                    for image in post.images
                ],
            }
        )

    return to_return_lst


async def return_recent_posts_without_login(db, user_id, start, limit):
    try:
        post_row = (
            db.query(model.Post)
            .options(
                joinedload(model.Post.likes),
                joinedload(model.Post.hashtags),
                joinedload(model.Post.images),
                joinedload(model.Post.post_owner),
            )
            .order_by(desc(model.Post.created_at))
            .offset(start)
            .limit(limit)
            .all()
        )

        return await make_dict_from_recent_posts(post_row, user_id, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} Occured")
