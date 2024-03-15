from ..user.utils import databases as userdb
from ..cat.utils import databases as catdb
from ..post.utils import databases as postdb


async def get_cat_post_user(catId, db):
    cat = await catdb.find_cat_by_cat_id(catId, db)
    user = await userdb.find_user_by_id(cat.ownerId, db)
    postids = await catdb.find_postids_by_cat_id(catId, db)
    posts = await postdb.find_posts_by_post_ids(postids, db)

    return cat, user, posts
