import io
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from PIL import Image

from app.config import settings
from app import model


async def image_to_thumnail(image):
    image = Image.open(image.file)
    resized_image = image.resize((200, 200))
    return resized_image


async def check_duplication(nickname, db):
    try:
        db.query(model.User).filter_by(nickname=nickname).first()
        return False
    except NoResultFound:
        return True


async def save_thumnail_image(image, username, user_id):
    content_type = image.content_type
    if content_type.startswith("image/"):
        thumnail_path = f"thumnail/{username}/user.jpg"
        resized_image = await image_to_thumnail(image)
        in_mem_file = io.BytesIO()
        resized_image.save(in_mem_file, format="jpeg")
        in_mem_file.seek(0)
        settings.s3.upload_fileobj(
            in_mem_file, settings.BUCKET_NAME, thumnail_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
        return thumnail_path
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Upload Thumnail User Image to Bucket"
        )


async def save_user_image(image, username, user_id):
    content_type = image.content_type
    if content_type.startswith("image/"):
        obj_path = f"{username}/user.jpg"
        content = await image.read()
        settings.s3.upload_fileobj(
            io.BytesIO(content), settings.BUCKET_NAME, obj_path, ExtraArgs={"ContentType": "image/jpeg"}
        )
        return obj_path
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Upload User Image to Bucket"
        )


async def update_image(user_id, image, db):
    user_row = db.query(model.User).filter_by(id=user_id).first()
    try:
        settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"thumnail/{user_row.username}/user.jpg")
        settings.s3.delete_object(Bucket=settings.BUCKET_NAME, Key=f"{user_row.username}/user.jpg")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while deleting user pic"
        )
    try:
        new_url = await save_user_image(image, user_row.username, user_id)
        await save_thumnail_image(image, user_row.username, user_id)
        user_row.profile_image = new_url
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured while uploading user pic"
        )
    db.commit()

    return True


async def update_nickname(user_id, nickname, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        user_row.nickname = nickname
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} occured")


async def update_name(user_id, name, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        user_row.name = name
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} occured")


async def update_explain(user_id, explain, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        user_row.explain = explain
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error {e} Occured")


async def load_mypage_utils(nickname, my_id, db):
    try:
        user_row = (
            db.query(model.User)
            .options(
                joinedload(model.User.posts),
                joinedload(model.User.cats),
                joinedload(model.User.following),
                joinedload(model.User.follower),
            )
            .filter_by(nickname=nickname)
            .first()
        )

        my_row = db.query(model.User).filter_by(id=my_id).first()
        follow = False
        if my_id:
            if user_row.id == my_id:
                is_owner = True
            else:
                is_owner = False

            for following in my_row.following:
                if user_row.id == following.id:
                    follow = True

        to_return_dict = {
            "userId": user_row.id,
            "nickname": user_row.nickname,
            "profileThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user_row.profile_image}",
            "postCount": len(user_row.posts),
            "explain": user_row.explain if user_row.explain is not None else "",
            "follow": {
                "followerCount": len(user_row.follower),
                "followingCount": len(user_row.following),
                "isFollowing": follow,
            },
            "cats": [
                {
                    "catName": cat.catname,
                    "catID": cat.id,
                    "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{cat.image}",
                }
                for cat in user_row.cats
            ],
            "posts": [
                {
                    "postId": post.id,
                    "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user_row.username}/{post.id}.jpg",
                }
                for post in user_row.posts
            ],
            "owner": is_owner,
        }

        return to_return_dict
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An error occured while returning user my page"
        )


async def send_catInfo(user_id, db):
    user_row = db.query(model.User).filter_by(id=user_id).first()
    to_return = [{"cat": {"name": cat.catname, "id": cat.id}} for cat in user_row.cats]
    return to_return


async def update_profile_info(user_id, db):
    try:
        user_row = db.query(model.User).filter_by(id=user_id).first()
        to_return_dict = {
            "name": user_row.name,
            "nickname": user_row.nickname,
            "explain": user_row.explain,
            "image": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user_row.profile_image}",
        }

        return to_return_dict
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} Occured")
