from ...application import apply_like_get_post


async def applyLike(userId, postId, db):
    stat, likeCount = await apply_like_get_post.apply_like_get_post(userId, postId, db)
    db.commit()

    return {"like": {"isLike": stat, "count": likeCount}}
