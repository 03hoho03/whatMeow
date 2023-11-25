from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm.session import Session

from app.api.v1.auth import auth_utils
from app.api.v1.like import like_utils
from app.database import get_db

router = APIRouter(tags=["Like"])


# 좋아요 누르는 엔드포인트
@router.post("/like/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def like(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        stat = await like_utils.add_like(post_id, decoded_dict.get("id"), db)
        if stat == "LIKE":
            return {"status": stat}
        elif stat == "UNLIKE":
            return {"status": stat}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to like")


@router.get("/like/{post_id}", status_code=status.HTTP_200_OK)
async def is_like(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        stat = await like_utils.is_like(post_id, decoded_dict.get("id"), db)
        if stat == "YES":
            return {"status": stat}
        elif stat == "NO":
            return {"status": stat}
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detali="Failed to check like or unlike"
            )
