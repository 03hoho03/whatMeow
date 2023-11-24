from fastapi import APIRouter, status, Request, Depends, UploadFile, File, Form
from sqlalchemy.orm.session import Session
from typing import Optional, List

# from app.api.schemas import cat_schema
from app.api.v1.cat import cat_utils
from app.api.v1.auth import auth_utils
from app.database import get_db

router = APIRouter(tags=["Cat"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def cat_add(
    request: Request,
    file: UploadFile = File(),
    age: Optional[int] = Form(None),
    catname: str = Form(),
    breed: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    explain: Optional[str] = Form(None),
    cat_hashtags: Optional[List[str]] = Form(None),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        data = {
            "age": age,
            "catname": catname,
            "breed": breed,
            "gender": gender,
            "explain": explain,
            "cat_hashtags": cat_hashtags,
        }
        if await cat_utils.cat_add_utils(db, file, data, decoded_dict.get("id")):
            return {"success": True}


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
async def cat_update(
    request: Request,
    cat_id: int = Form(),
    file: Optional[UploadFile] = File(None),
    age: Optional[int] = Form(None),
    catname: Optional[str] = Form(None),
    breed: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    explain: Optional[str] = Form(None),
    cat_hashtags: Optional[List[str]] = Form(None),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        data = {
            "id": cat_id,
            "age": age,
            "catname": catname,
            "breed": breed,
            "gender": gender,
            "explain": explain,
            "cat_hashtags": cat_hashtags,
        }
        if await cat_utils.cat_update_utils(db, file, data, decoded_dict.get("id")):
            return {"success": True}
