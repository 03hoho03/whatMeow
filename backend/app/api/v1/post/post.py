from fastapi import Depends, APIRouter, status
from fastapi import File, UploadFile, Form, Request

from sqlalchemy.orm.session import Session
from typing import List

from app import model
from app.database import get_db
from app.api.schemas import post_schema
from app.api.v1.auth import auth_utils
from app.api.v1.post import post_utils

router = APIRouter(tags=["Post"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_upload(
    request: Request,
    content: str = Form(...),
    tags: List[str] = Form(None),
    cat_ids: List[int] = Form(None),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """
    입력받을 데이터 => 게시글, 해시태그, (고양이 품종)
    """
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)

    if decoded_dict:
        # hashtag ID가 담겨져 있는 list
        if tags:
            hashtag_id_lst = await post_utils.return_hashtag_ids(db, tags)
        row = model.Post(title=content, uploader_id=decoded_dict["id"])
        db.add(row)
        db.commit()
        # post_hashtags 테이블에 연결 정보 추가
        if tags:
            await post_utils.insert_posthashtags(db, hashtag_id_lst, row.id)

        # post_cats 테이블에 연결 정보 추가
        if cat_ids:
            await post_utils.insert_postcats(db, cat_ids, row.id)
        # images 테이블에 추가 및 스토리지에 저장
        await post_utils.save_images(db, decoded_dict.get("username"), files, row.id)
        await post_utils.save_thumnail(decoded_dict.get("username"), files[0], row.id)

        return {"success": True}


@router.delete("/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def post_delete(request: Request, post_id: int, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await post_utils.post_delete(db, decoded_dict.get("username"), post_id):
            return {"success": True}


@router.get("/{post_id}")
async def post_detail(request: Request, data: post_schema.PostDetail = Depends(), db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        return await post_utils.return_detailed_post(db, decoded_dict.get("id"), data.post_id)
