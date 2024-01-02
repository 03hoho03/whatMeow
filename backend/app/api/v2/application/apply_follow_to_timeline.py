from ..post.utils import databases as postdb


async def add_items_to_timeline(fromUserId, toUserId, db):
    posts = await postdb.find_posts_by_uploader_id_order_by_id(toUserId, db)
    await postdb.timeline_upload_by_fromUser_posts(posts, fromUserId, db)
