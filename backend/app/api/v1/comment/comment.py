from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm.session import Session

from app.api.v1.auth import auth_utils
from app.api.v1.comment import comment_utils
from app.api.schemas import comment_schema
from app.database import get_db

router = APIRouter(tags=["Comment"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def comment_upload(
    request: Request,
    data: comment_schema.add_comment,
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await comment_utils.upload_comment(data.comment, data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Add Comment")


@router.get("/delete", status_code=status.HTTP_202_ACCEPTED)
async def comment_delete(
    request: Request,
    data: comment_schema.delete_comment = Depends(),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await comment_utils.delete_comment(data.comment_id, data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_coce=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Delete Comment")


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
async def comment_update(
    request: Request,
    data: comment_schema.update_comment,
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await comment_utils.update_comment(
            data.new_comment, data.comment_id, data.post_id, decoded_dict.get("id"), db
        ):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Update Comment")
