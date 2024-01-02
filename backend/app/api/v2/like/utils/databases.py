from app.model import Like


async def apply_like(userId, postId, db):
    like = db.query(Like).filter_by(ownerId=userId, postId=postId).first()
    if like:
        db.delete(like)
        return False
    else:
        likeNew = Like(ownerId=userId, postId=postId)
        db.add(likeNew)
        return True
