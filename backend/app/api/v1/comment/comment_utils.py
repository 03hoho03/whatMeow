from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status

from app import model


# Comment 작성 함수 구현
async def upload_comment(comment, post_id, user_id, db):
    try:
        row = model.Comment(comment=comment, uploader=user_id, post_id=post_id)
        db.add(row)
        db.commit()
        return True
    except Exception:
        return False


# Comment 삭제 함수 구현
async def delete_comment(comment_id, post_id, user_id, db):
    try:
        c_row = db.query(model.Comment).filter_by(id=comment_id, post_id=post_id, uploader=user_id).first()
        db.delete(c_row)
        db.commit()
        return True
    except NoResultFound:
        return False


# Comment 업데이트 함수 구현
async def update_comment(new_comment, comment_id, post_id, user_id, db):
    try:
        c_row = db.query(model.Comment).filter_by(id=comment_id, post_id=post_id, uploader=user_id).first()
        c_row.comment = new_comment
        db.commit()
        return True
    except NoResultFound:
        return False


# Comment 목록 반환 함수 구현
async def return_comment_utils(post_id, db):
    try:
        post_row = db.query(model.Post).filter_by(id=post_id).first()
        return_lst = []
        for comment in post_row.comments:
            return_lst.append(
                {
                    "comment_id": comment.id,
                    "comment": comment.comment,
                    "created_at": comment.created_at,
                    "nickname": comment.comment_owner.nickname,
                }
            )
            return return_lst
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"{e} occured while returning comment list"}
        )
