from ...application import apply_like_get_post


async def applyLike(userId, postId, data, db):
    stat, likeCount = await apply_like_get_post.apply_like_get_post(userId, postId, data.version, db)
    db.commit()

    return {"like": {"isLike": stat, "count": likeCount}}
