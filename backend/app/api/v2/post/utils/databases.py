from fastapi import HTTPException, status

from app.model import Post, Image, HashTag, PostHashTag, PostCats


async def find_posts_by_uploader_id(id, db):
    return db.query(Post).filter_by(uploaderId=id).all()


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
