from fastapi import Depends, APIRouter, status
from fastapi import File, UploadFile, Form, Request

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from typing import List

from app.config import settings
from app import model
from app.database import get_db
from app.api.schemas import post_schema
from app.api.v1.auth import auth_utils
from app.api.v1.post import post_utils

router = APIRouter(tags=["Post"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def post_upload(
    request: Request,
    content: str = Form(...),
    tags: List[str] = Form(...),
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
        hashtag_id_lst = await post_utils.return_hashtag_ids(db, tags[0].split(","))
        row = model.Post(title=content, uploader_id=decoded_dict["id"])
        db.add(row)
        db.commit()
        # post_hashtags 테이블에 연결 정보 추가
        await post_utils.insert_posthashtags(db, hashtag_id_lst, row.id)

        # images 테이블에 추가 및 스토리지에 저장
        await post_utils.save_images(db, decoded_dict.get("username"), files, row.id)

        return {"success": True}


@router.get("/delete/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def post_delete(request: Request, post_id: int, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await post_utils.post_delete(db, decoded_dict.get("username"), post_id):
            return {"success": True}


@router.get("/detail")
async def post_detail(request: Request, data: post_schema.PostDetail = Depends(), db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        return await post_utils.return_detailed_post(db, decoded_dict.get("nickname"), data.post_id)


async def make_dict_from_follow_posts(latest_posts):
    to_return_lst = []
    for post in latest_posts:
        to_return_lst.append(
            {
                "nickname": post.post_owner.nickname,
                "likeLength": len(post.likes),
                "createdAt": post.created_at,
                "content": post.title,
                "postId": post.id,
                "images": [f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{post.images[0].url}"],
            }
        )

    return to_return_lst


@router.get("/test")
async def post_test(request: Request, start: int, limit: int, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        post_row = (
            db.query(model.Post)
            .options(
                joinedload(model.Post.likes),
                joinedload(model.Post.hashtags),
                joinedload(model.Post.images),
                joinedload(model.Post.post_owner),
            )
            .all()
        )

        return await make_dict_from_follow_posts(post_row)
