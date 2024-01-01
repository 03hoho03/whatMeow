from ..utils import databases, images


async def createCat(userId, catName, age, gender, explain, breed, file, hashtags, db):
    cat = await databases.create_cat(userId, catName, age, gender, explain, breed, db)
    url = await images.upload_cat_image(cat.id, file)
    await images.upload_cat_thumnail(url, file)
    cat.image = url

    if hashtags:
        await databases.apply_hashtag(cat.id, hashtags, db)

    db.commit()
    return cat
