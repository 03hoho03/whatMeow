from ...application.get_posts_users_hashtags_by_post_id import get_posts_users_hashtags_by_post_id
from ...application.get_posts_users_images import get_posts_users_images
from ...application.get_posts_users_images_follow import get_posts_users_images_follow
from ..utils import tools


async def findDetailedPost(userId, postId, db):
    post, user, images, hashtags, comments, statLike = await get_posts_users_hashtags_by_post_id(userId, postId, db)

    return await tools.make_detailed_post(post, user, images, hashtags, comments, statLike)


async def searchMainFeed(userId, key, size, db):
    posts, users, images, likes = await get_posts_users_images(userId, key, size, db)

    return await tools.make_mainfeed_posts(users, posts, images, likes)


async def searchFollow(userId, key, size, db):
    posts, users, images, likes = await get_posts_users_images_follow(userId, key, size, db)

    return await tools.make_mainfeed_posts(users, posts, images, likes)
