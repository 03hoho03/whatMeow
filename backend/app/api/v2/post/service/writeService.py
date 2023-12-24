from ..utils import databases, images


async def createPost(id, username, content, tags, cat_ids, files, db):
    post = await databases.create_post(id, content, db)
    imageList = await images.upload_post_images(username, post.id, files)
    await images.upload_post_thumnail(username, post.id, files[0])
    await databases.create_image(post.id, imageList, db)
    if tags:
        await databases.apply_hashtag(post.id, tags, db)
    if cat_ids:
        await databases.insert_postcats(post.id, cat_ids, db)

    db.commit()
    return post
