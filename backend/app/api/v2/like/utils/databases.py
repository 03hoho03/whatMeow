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


async def is_like(userId, postId, db):
    like = db.query(Like).filter_by(ownerId=userId, postId=postId).first()
    if like:
        return True
    else:
        return False


async def is_likes(userId, posts, db):
    likes = []
    if userId:
        for i in range(len(posts)):
            like = db.query(Like).filter_by(ownerId=userId, postId=posts[i].id).first()
            if like:
                likes.append(True)
            else:
                likes.append(False)
    else:
        likes = [False] * len(posts)
    return likes
