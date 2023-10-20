from fastapi import Depends, APIRouter, status
from fastapi import File, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session
from typing import List

from app.api.schemas import post_schema
from app import model
from app.database import get_db
from app.api.v1.auth import auth_utils
from app.api.v1.post import post_utils

router = APIRouter()
security = HTTPBearer()


@router.post("/post_upload", status_code=status.HTTP_201_CREATED)
async def post_upload(
    data: post_schema.PostUpload,
    hashtag: post_schema.HashTagUpload,
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    입력받을 데이터 => 게시글, 해시태그, (고양이 품종)
    """
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        # hashtag가 담겨져 있는 list
        hashtag_name_lst = hashtag.dict().get("hashtag")
        hashtag_id_lst = post_utils.return_hashtag_ids(db, hashtag_name_lst)

        row = model.Post(**data.dict(), uploader=decoded_dict["id"])
        db.add(row)
        db.commit()

        # # post_hashtags 테이블에 연결 정보 추가
        post_utils.insert_posthashtags(db, hashtag_id_lst, row.id)
        # db.execute(model.post_hashtags.insert().values(post_id=row.id, hashtag_id=hashtag_id))
        # db.commit()

        return {"username": decoded_dict.get("username"), "id": row.id}


@router.post("/upload_image", status_code=status.HTTP_201_CREATED)
async def image_upload(username: str, post_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """
    이전에 post_upload에서 token 관련된건 이미 처리한 이후라고 가정
    """
    post_utils.save_images(db, username, files, post_id)


# @router.post("/update", status_code=status.HTTP_202_ACCEPTED)
# async def post_update(
#     data: post_schema.PostUpload, cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
# ):
#     """
#     입력받을 데이터 => 이미지, 게시글, 해시태그, (고양이 품종?)
#     """
#     a = 1


# @router.post("/delete")
