from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm.session import Session

from app.api.schemas import cat_schema
from app.api.v1.cat import cat_utils
from app.api.v1.auth import auth_utils
from app.database import get_db

router = APIRouter(tags=["Cat"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def cat_add(request: Request, data: cat_schema.CatAdd, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await cat_utils.cat_add_utils(db, data, decoded_dict.get("id")):
            return {"success": True}
