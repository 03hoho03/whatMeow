from ..cat.utils.databases import find_cats_by_owner_id


async def get_cat_info_by_user_id(id, db):
    return await find_cats_by_owner_id(id, db)
