from ..follow.utils import databases as followdb
from ..user.utils import databases as userdb


async def get_users_from_follow_ids(fromUserId, db):
    subq = await followdb.make_toUserId_subquery(fromUserId, db)
    toUsers = await userdb.find_users_by_follow_subquery(subq, db)

    return toUsers
