from ..cat.utils.databases import find_cats_by_owner_id
from ..post.utils.databases import find_posts_by_uploader_id
from ..follow.utils.databases import find_followers_by_user_id, find_followings_by_user_id


async def get_cats_posts_follows_by_user(user, db):
    posts = await find_posts_by_uploader_id(user.id, db)
    cats = await find_cats_by_owner_id(user.id, db)
    followers = await find_followers_by_user_id(user.id, db)
    followings = await find_followings_by_user_id(user.id, db)

    return {"posts": posts, "cats": cats, "followers": followers, "followings": followings}
