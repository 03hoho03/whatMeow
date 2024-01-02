from ...application import get_users_from_follow_ids
from ..utils import tools


async def getFollowingUsers(userId, db):
    fromUsers = await get_users_from_follow_ids.get_fromUsers_from_follow_ids(userId, db)

    return await tools.make_follow_list(fromUsers)


async def getFollowerUsers(userId, db):
    toUsers = await get_users_from_follow_ids.get_toUsers_from_follow_ids(userId, db)

    return await tools.make_follow_list(toUsers)
