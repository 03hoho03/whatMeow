from ..like.utils import databases as likedb
from ..post.utils import databases as postdb


async def apply_like_get_post(userId, postId, db):
    stat = await likedb.apply_like(userId, postId, db)
    likeCount = await postdb.update_version_likes(postId, stat, db)

    return stat, likeCount
