from fastapi import HTTPException, status

from app.model import Post, Image, HashTag, PostHashTag, PostCats, Timeline


async def find_post_by_post_id(id, db):
    return db.query(Post).filter_by(id=id).first()


async def find_posts_by_uploader_id(id, db):
    return db.query(Post).filter_by(uploaderId=id).all()


async def find_urls_by_post_id(id, db):
    return db.query(Image.url).filter_by(postId=id).all()


async def find_hashtagids_by_post_id(id, db):
    return db.query(PostHashTag.hashtagId).filter_by(postId=id).all()


async def find_hashtags_by_hashtagids(hashtagIds, db):
    ids = [hashtagId[0] for hashtagId in hashtagIds]
    return db.query(HashTag.hashtag).filter(HashTag.id.in_(ids)).all()


async def find_posts_by_post_ids(postIds, db):
    ids = [postId[0] for postId in postIds]
    return db.query(Post).filter(Post.id.in_(ids)).all()


async def timeline_upload(postId, fromUsers, db):
    data = [Timeline(postId=postId, userId=fromUser.id) for fromUser in fromUsers]

    db.bulk_insert_mappings(Timeline, [timeline.__dict__ for timeline in data])


async def create_post(id, content, db):
    try:
        row = Post(title=content, uploaderId=id)
        db.add(row)
        db.flush()

        return row
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while create_post")


async def create_image(id, images, db):
    try:
        for image in images:
            row = Image(url=image, postId=id)
            db.add(row)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while create_image")


async def apply_hashtag(id, tags, db):
    try:
        hashtag_lst = []

        for tag in tags:
            val = tag.split(" ")
            if len(val) == 1:
                hashtag_lst.append(val)
            else:
                for v in val:
                    hashtag_lst.append(v)

        for hashtag in hashtag_lst:
            existing_hashtag = db.query(HashTag).filter_by(hashtag=hashtag).first()
            if existing_hashtag:
                posthashtag = PostHashTag(postId=id, hashtagId=existing_hashtag.id)
                db.add(posthashtag)
            else:
                new_hashtag = HashTag(hashtag=hashtag)
                db.add(new_hashtag)
                db.flush()
                posthashtag = PostHashTag(postId=id, hashtagId=new_hashtag.id)
                db.add(posthashtag)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while apply_hashtag")


async def insert_postcats(id, catIds, db):
    try:
        for catId in catIds:
            postcat = PostCats(postId=id, catId=catId)
            db.add(postcat)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while insert_postcats")


async def delete_post(userId, postId, db):
    post = db.query(Post).filter_by(id=postId).first()
    if post:
        if post.uploaderId == userId:
            db.delete(post)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Owner")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Post with this ID")
