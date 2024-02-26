from ..utils import databases


async def lookupComment(postId, db):
    comments = await databases.find_commets_by_post_id(postId, db)

    return comments
