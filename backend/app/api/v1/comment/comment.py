from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm.session import Session

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
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await comment_utils.upload_comment(data.comment, data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.get("/delete", status_code=status.HTTP_202_ACCEPTED)
async def comment_delete(
    request: Request,
    data: comment_schema.delete_comment = Depends(),
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await comment_utils.delete_comment(data.comment_id, data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_coce=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Delete Comment")
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def return_comments(post_id: int, request: Request, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        return await comment_utils.return_comments_utils(post_id, db)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
async def comment_update(
    request: Request,
    data: comment_schema.update_comment,
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await comment_utils.update_comment(
            data.new_comment, data.comment_id, data.post_id, decoded_dict.get("id"), db
        ):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Update Comment")
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")
