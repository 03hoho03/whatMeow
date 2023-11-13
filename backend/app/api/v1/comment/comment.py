from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session

from app.api.v1.auth import auth_utils
from app.api.v1.comment import comment_utils
from app.api.schemas import comment_schema
from app.database import get_db

router = APIRouter(tags=["Comment"])
security = HTTPBearer()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def comment_upload(
    data: comment_schema.add_comment,
    db: Session = Depends(get_db),
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        # Comment 추가 함수 구현
        if await comment_utils.upload_comment(data.comment, data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Add Comment")


@router.get("/delete", status_code=status.HTTP_202_ACCEPTED)
async def comment_delete(
    data: comment_schema.delete_comment = Depends(),
    db: Session = Depends(get_db),
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        # Comment 삭제 함수 구현
        if await comment_utils.delete_comment(data.comment_id, data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_coce=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Delete Comment")


@router.get("/update", status_code=status.HTTP_202_ACCEPTED)
async def comment_update(
    data: comment_schema.update_comment = Depends(),
    db: Session = Depends(get_db),
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        # Comment 업데이트 함수 구현
        if await comment_utils.update_comment(
            data.new_comment, data.comment_id, data.post_id, decoded_dict.get("id"), db
        ):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Update Comment")
