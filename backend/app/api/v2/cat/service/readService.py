from ..utils import tools
from ...application import get_cat_post_user


async def findCat(userId, catId, db):
    cat, user, posts = await get_cat_post_user.get_cat_post_user(catId, db)
    return await tools.make_detailed_cat(cat, user, userId, posts)
