from fastapi import Depends, APIRouter, status, UploadFile, File, Form, Request
from typing import Optional
from sqlalchemy.orm.session import Session

from app.database import get_db

from app.api.v1.auth import auth_utils
from app.api.v1.user import user_utils

router = APIRouter(tags=["User"])


@router.get("/duplicated", status_code=status.HTTP_200_OK)
async def is_duplicated(nickname: str, db: Session = Depends(get_db)):
    if await user_utils.check_duplication(nickname, db):
        return True
    else:
        return False


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
async def update_userdata(
    request: Request,
    nickname: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    explain: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        _dict = {"nickname": nickname, "name": name, "explain": explain}
        if await user_utils.update_user_info(file, _dict, decoded_dict.get("id"), db):
            return {"success": True}


@router.get("/profile/{nickname}", status_code=status.HTTP_200_OK)
async def load_mypage(nickname: str, request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        return await user_utils.load_mypage_utils(nickname, decoded_dict.get("id"), db)
