from ...application import get_users_from_follow_ids, apply_follow_to_timeline
from ..utils import databases


async def applyFollow(fromUserId, toUserId, db):
    toUsers = await get_users_from_follow_ids.get_fromUsers_from_follow_ids(toUserId, db)
    follow = await databases.apply_follow_request_by_toUser_id(fromUserId, toUserId, toUsers, db)
    db.commit()
    if follow["isFollowing"]:
        await apply_follow_to_timeline.add_items_to_timeline(fromUserId, toUserId, db)

    return follow
