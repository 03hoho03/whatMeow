from fastapi import Depends, status, APIRouter, Request
from sqlalchemy.orm.session import Session

from app.api.schemas import search_schema
from app.api.v1.search import search_utils
from app.api.v1.auth import auth_utils
from app import model
from app.database import get_db

router = APIRouter(tags=["Search"])


# Pydantic 모델을 query parameter로 받을 때는 Depends() 사용할 것
@router.get("/hashtag", status_code=status.HTTP_200_OK)
async def get_hashtag_result(data: search_schema.SearchHashTag = Depends(), db: Session = Depends(get_db)):
    """
    검색한 해시태그에 해당하는 결과 return
    """
    hashtag_obj = db.query(model.HashTag).filter_by(hashtag=data.hashtag).first()
    result = (
        db.query(model.post_hashtags)
        .filter(model.post_hashtags.c.hashtag_id == hashtag_obj.id)
        .offset(data.start * data.limit)
        .limit(data.limit)
        .all()
    )

    return await search_utils.return_post_by_hashtag(db, result)


@router.get("/nickname", status_code=status.HTTP_200_OK)
async def get_name_result(data: search_schema.SearchName = Depends(), db: Session = Depends(get_db)):
    """
    검색한 사용자 닉네임에 해당하는 결과 return
    """
    user = db.query(model.User).filter_by(nickname=data.name).first()
    result = (
        db.query(model.Post)
        .filter(model.Post.uploader_id == user.id)
        .offset(data.start * data.limit)
        .limit(data.limit)
        .all()
    )
    return await search_utils.return_post_by_name(result)


@router.get("/main", status_code=status.HTTP_200_OK)
async def get_main_result(
    request: Request, data: search_schema.SearchFollower = Depends(), db: Session = Depends(get_db)
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        return await search_utils.return_follow_posts(db, data.user_id, data.start * data.limit, data.limit)
