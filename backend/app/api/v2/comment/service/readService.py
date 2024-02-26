from ..utils import databases, tools


async def lookupComment(postId, db):
    comments = await databases.find_commets_by_post_id(postId, db)
    return await tools.make_comment_list(comments)
