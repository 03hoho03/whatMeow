from ..utils import databases, images, tools


async def userRegister(data, db):
    username = await databases.get_random_username(db)
    url = await images.upload_default_image(username)
    password = await tools.create_hashed_password(data.password)
    user = await databases.add_generaluser(data, username, url, password, db)

    return user
