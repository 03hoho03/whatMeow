from fastapi import Depends, APIRouter, status, UploadFile, File, Request
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.api.schemas import user_schema
from app.api.v1.auth import auth_utils
from app.api.v1.user import user_utils

router = APIRouter(tags=["User"])


@router.get("/duplicated", status_code=status.HTTP_200_OK)
async def is_duplicated(nickname: str, db: Session = Depends(get_db)):
    if await user_utils.check_duplication(nickname, db):
        return True
    else:
        return False


@router.put("/update/nickname", status_code=status.HTTP_202_ACCEPTED)
async def update_nickname(
    request: Request,
    data: user_schema.UpdateNickname,
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await user_utils.update_nickname(decoded_dict.get("id"), data.nickname, db):
            return {"success": True}


@router.put("/update/name", status_code=status.HTTP_202_ACCEPTED)
async def update_name(request: Request, data: user_schema.UpdateName, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await user_utils.update_name(decoded_dict.get("id"), data.name, db):
            return {"success": True}


@router.put("/update/explain", status_code=status.HTTP_202_ACCEPTED)
async def update_explain(request: Request, data: user_schema.UpdateExplain, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await user_utils.update_explain(decoded_dict.get("id"), data.explain, db):
            return {"success": True}


@router.put("/update/image", status_code=status.HTTP_202_ACCEPTED)
async def update_image(request: Request, file: UploadFile = File(), db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await user_utils.update_image(decoded_dict.get("id"), file, db):
            return {"success": True}


@router.get("/profile/{nickname}", status_code=status.HTTP_200_OK)
async def load_mypage(nickname: str, request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        return await user_utils.load_mypage_utils(nickname, decoded_dict.get("id"), db)
