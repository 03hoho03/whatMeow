from ..post.utils import databases as postdb
from ..user.utils import databases as userdb
from ..like.utils import databases as likedb


async def get_posts_users_images_follow(userId, key, size, db):
    postIds = await postdb.find_postIds_from_timeline(userId, key, size, db)
    posts = await postdb.find_posts_by_post_ids_order_by_id(postIds, db)
    images = await postdb.find_urls_by_posts(posts, db)
    users = await userdb.find_users_by_posts(posts, db)
    likes = await likedb.is_likes(userId, posts, db)

    return posts, users, images, likes
