from fastapi import Depends, APIRouter, status
from fastapi import File, UploadFile, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session
from typing import List

from app import model
from app.database import get_db
from app.api.v1.auth import auth_utils
from app.api.v1.post import post_utils

router = APIRouter(tags=["Post"])
security = HTTPBearer()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def post_upload(
    title: str = Form(...),
    hashtag: str = Form(...),
    images: List[UploadFile] = File(...),
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    입력받을 데이터 => 게시글, 해시태그, (고양이 품종)
    """
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        # hashtag ID가 담겨져 있는 list
        hashtag_id_lst = await post_utils.return_hashtag_ids(db, hashtag.split(","))
        row = model.Post(title=title, uploader_name=decoded_dict["username"])
        db.add(row)
        db.commit()

        # post_hashtags 테이블에 연결 정보 추가
        await post_utils.insert_posthashtags(db, hashtag_id_lst, row.id)

        # images 테이블에 추가 및 스토리지에 저장
        await post_utils.save_images(db, decoded_dict.get("username"), images, row.id)

        return {"success": True}


@router.get("/delete/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def post_delete(
    post_id: int, cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
):
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        if await post_utils.post_delete(db, post_id):
            return {"Success": True}
