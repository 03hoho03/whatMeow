from fastapi import Depends, APIRouter, status
from fastapi import File, UploadFile, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session
from typing import List

# from app.api.schemas import post_schema
from app import model
from app.database import get_db
from app.api.v1.auth import auth_utils
from app.api.v1.post import post_utils

router = APIRouter()
security = HTTPBearer()


@router.post("/post_upload", status_code=status.HTTP_201_CREATED)
async def post_upload(
    title: str = Form(...),
    hashtag: List[str] = Form(...),
    images: List[UploadFile] = File(...),
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    입력받을 데이터 => 게시글, 해시태그, (고양이 품종)
    """
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        # hashtag가 담겨져 있는 list
        hashtag_id_lst = post_utils.return_hashtag_ids(db, hashtag)

        row = model.Post(title=title, uploader=decoded_dict["id"])
        db.add(row)
        db.commit()

        # post_hashtags 테이블에 연결 정보 추가
        post_utils.insert_posthashtags(db, hashtag_id_lst, row.id)

        # images 테이블에 추가 및 스토리지에 저장
        post_utils.save_image(db, decoded_dict.get("username"), images, row.id)
        # db.execute(model.post_hashtags.insert().values(post_id=row.id,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     eeeeeeeeeeeee hashtag_id=hashtag_id))
        # db.commit()

        return {"success": True}


@router.post("/post_delete", status_code=status.HTTP_202_ACCEPTED)
async def image_upload(cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return 1


# @router.post("/update", status_code=status.HTTP_202_ACCEPTED)
# async def post_update(
#     data: post_schema.PostUpload, cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
# ):
#     """
#     입력받을 데이터 => 이미지, 게시글, 해시태그, (고양이 품종?)
#     """
#     a = 1


# @router.post("/delete")
