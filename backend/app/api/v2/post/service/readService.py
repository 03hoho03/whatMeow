from ...application.get_posts_users_hashtags_by_post_id import get_posts_users_hashtags_by_post_id
from ..utils import tools


async def findDetailedPost(userId, postId, db):
    post, user, images, hashtags, comments, statLike = await get_posts_users_hashtags_by_post_id(userId, postId, db)

    return await tools.make_detailed_post(post, user, images, hashtags, comments, statLike)
