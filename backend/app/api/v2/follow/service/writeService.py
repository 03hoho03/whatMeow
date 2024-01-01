from ...application import get_users_from_follow_ids
from ..utils import databases


async def applyFollow(fromUserId, toUserId, db):
    toUsers = await get_users_from_follow_ids.get_toUsers_from_follow_ids(fromUserId, db)
    follow = await databases.apply_follow_request_by_toUser_id(fromUserId, toUserId, toUsers, db)
    db.commit()

    return follow
