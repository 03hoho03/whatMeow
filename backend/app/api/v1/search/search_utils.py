from app import model
from PIL import Image
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
import base64
import io
from app.config import settings


async def return_post_by_hashtag(db, lst):
    post_lst = []
    for post_id, _ in lst:
        post_item = db.query(model.Post).filter_by(id=post_id).first()
        img = Image.open(post_item.images[0].url)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        return_dict = {"title": post_item.title, "post_id": post_item.id, "image": img_base64}
        post_lst.append(return_dict)

    return post_lst


async def return_post_by_name(lst):
    post_lst = []
    for post_item in lst:
        img = Image.open(post_item.images[0].url)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        return_dict = {"title": post_item.title, "post_id": post_item.id, "image": img_base64}
        post_lst.append(return_dict)

    return post_lst


async def append_following_ids(followings):
    following_ids = []
    for following in followings:
        following_ids.append(following.id)

    return following_ids


async def make_dict_from_follow_posts(latest_posts):
    to_return_lst = []
    for post in latest_posts:
        to_return_lst.append(
            {
                "nickname": post.post_owner.nickname,
                "like_length": len(post.likes),
                "created_at": post.created_at,
                "content": post.title,
                "post_id": post.id,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{post.images[0].url}",
            }
        )

    return to_return_lst


"""
반환 해줘야 할 것
    - nickname
    - Thumnail(1장)
    - 좋아요 갯수
    - created_at
    - content
    - post_id
"""


async def return_follow_posts(db, user_id, start, limit):
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

    return await make_dict_from_follow_posts(latest_posts)
