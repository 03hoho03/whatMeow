from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm.session import Session

from app.api.v1.comment import comment_utils, schema
from app.database import get_db

router = APIRouter(tags=["Comment"])


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
async def comment_upload(
    request: Request,
    post_id: int,
    data: schema.add_comment,
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await comment_utils.upload_comment(data.comment, post_id, decoded_dict.get("id"), db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.delete("/{comment_id}", status_code=status.HTTP_202_ACCEPTED)
async def comment_delete(
    request: Request,
    comment_id: int,
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await comment_utils.delete_comment(comment_id, decoded_dict.get("id"), db):
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


@router.put("/{comment_id}", status_code=status.HTTP_202_ACCEPTED)
async def comment_update(
    request: Request,
    comment_id: int,
    data: schema.update_comment,
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await comment_utils.update_comment(data.new_comment, comment_id, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to Update Comment")
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")
