from fastapi import HTTPException, status

from app.model import Cat, HashTag, CatHashTag


async def find_cats_by_owner_id(userId, db):
    return db.query(Cat).filter_by(ownerId=userId).all()


async def create_cat(userId, catName, age, gender, explain, breed, db):
    cat = Cat(catName=catName, age=age, gender=gender, explain=explain, breed=breed, ownerId=userId)
    db.add(cat)
    db.flush()

    return cat


async def apply_hashtag(catId, tags, db):
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
                posthashtag = CatHashTag(catId=catId, hashtagId=existing_hashtag.id)
                db.add(posthashtag)
            else:
                new_hashtag = HashTag(hashtag=hashtag)
                db.add(new_hashtag)
                db.flush()
                posthashtag = CatHashTag(catId=catId, hashtagId=new_hashtag.id)
                db.add(posthashtag)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while apply_hashtag")
