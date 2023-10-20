# hashtag_name_list 순회하면서 하나하나 존재하는지 체크하고
# hashtag_id_list 반환하는 함수 작성하기
import os

from app import model

image_dir = os.path.join(os.getcwd(), "images")


def return_hashtag_ids(db, name_lst):
    hashtag_id_lst = []
    for name in name_lst:
        existing_hashtag = db.query(model.HashTag).filter_by(hashtag=name).first()
        if existing_hashtag:
            hashtag_id = existing_hashtag.id
        else:
            new_hashtag = model.HashTag(hashtag=name)
            db.add(new_hashtag)
            db.commit()
            hashtag_id = new_hashtag.id

        hashtag_id_lst.append(hashtag_id)

    return hashtag_id_lst


def insert_posthashtags(db, hashtag_id_lst, row_id):
    for hashtag_id in hashtag_id_lst:
        db.execute(model.post_hashtags.insert().values(post_id=row_id, hashtag_id=hashtag_id))
        db.commit()


def save_images(db, username, image_lst, row_id):
    target_dir = os.path.join(image_dir, username)
    post_dir = os.path.join(target_dir, str(row_id))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    os.makedirs(post_dir)

    for i, image in enumerate(image_lst):
        file_path = os.path.join(post_dir, str(i) + ".jpg")
        print(file_path)
        with open(file_path, "wb") as f:
            f.write(image.file.read())
        row = model.Image(url=file_path, post_id=row_id)
        db.add(row)

    db.commit()
