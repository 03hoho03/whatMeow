from fastapi import Depends, APIRouter, status, Request

from sqlalchemy.orm.session import Session

from app.database import get_db
from app.api.schemas import post_schema
from app.api.v1.user import user_utils
from app.api.v1.cat import cat_utils
from app.api.v1.search import search_utils
from app.api.v1.post import post_utils

router = APIRouter(tags=["Guest"])


@router.get("/post/{post_id}")
async def post_detail(data: post_schema.PostDetail = Depends(), db: Session = Depends(get_db)):
    return await post_utils.return_detailed_post(db, 0, data.post_id)


@router.get("/search")
async def post_test(request: Request, start: int, limit: int, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        return await search_utils.return_recent_posts_without_login(
            db, decoded_dict.get("id"), start * limit, (start * limit) + limit
        )
    else:
        return await search_utils.return_recent_posts_without_login(db, 0, start * limit, (start * limit) + limit)


@router.get("/user/{nickname}", status_code=status.HTTP_200_OK)
async def load_mypage_nologin(nickname: str, db: Session = Depends(get_db)):
    return await user_utils.load_mypage_utils(nickname, 0, db)


@router.get("/{cat_id}", status_code=status.HTTP_200_OK)
async def cat_info(cat_id: int, db: Session = Depends(get_db)):
    return await cat_utils.cat_info(cat_id, 0, db)
