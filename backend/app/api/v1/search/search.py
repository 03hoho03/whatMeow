from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from fastapi.security import HTTPBearer

from app.api.schemas import search_schema
from app.api.v1.search import search_utils
from app import model
from app.database import get_db

router = APIRouter(tags=["Search"])
security = HTTPBearer()


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
        .offset(data.start)
        .limit(data.limit)
        .all()
    )

    post_lst = await search_utils.return_post_by_hashtag(db, result)
    return JSONResponse(content=post_lst)


@router.get("/username", status_code=status.HTTP_200_OK)
async def get_name_result(data: search_schema.SearchName = Depends(), db: Session = Depends(get_db)):
    """
    검색한 사용자 닉네임에 해당하는 결과 return
    """

    result = (
        db.query(model.Post).filter(model.Post.uploader_name == data.name).offset(data.start).limit(data.limit).all()
    )
    print(result)
    post_lst = await search_utils.return_post_by_name(result)
    return JSONResponse(content=post_lst)
