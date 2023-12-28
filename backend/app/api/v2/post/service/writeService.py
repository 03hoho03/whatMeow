from ..utils import databases, images


async def createPost(userId, content, tags, cat_ids, files, db):
    post = await databases.create_post(userId, content, db)
    imageList = await images.upload_post_images(userId, post.id, files)
    await images.upload_post_thumnail(imageList[0], files[0])
    await databases.create_image(post.id, imageList, db)
    if tags:
        await databases.apply_hashtag(post.id, tags, db)
    if cat_ids:
        await databases.insert_postcats(post.id, cat_ids, db)

    db.commit()
    return post


async def deletePost(userId, postId, db):
    await databases.delete_post(userId, postId, db)
    db.commit()