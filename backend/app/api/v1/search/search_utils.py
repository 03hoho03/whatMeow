from app import model
from PIL import Image
import base64
import io


async def return_post_by_hashtag(db, lst):
    post_lst = []
    for post_id, _ in lst:
        post_item = db.query(model.Post).filter_by(id=post_id).first()
        img = Image.open(post_item.images[0].url)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        return_dict = {"title": post_item.title, "post_id": post_item.id, "image": img_base64}
        post_lst.append(return_dict)

    return post_lst


async def return_post_by_name(lst):
    post_lst = []
    for post_item in lst:
        img = Image.open(post_item.images[0].url)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        return_dict = {"title": post_item.title, "post_id": post_item.id, "image": img_base64}
        post_lst.append(return_dict)

    return post_lst
