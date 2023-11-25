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
        stat, count = await like_utils.add_like(post_id, decoded_dict.get("id"), db)
        if stat == "LIKE":
            return {"like": {"isLike": True, "count": count}}
        elif stat == "UNLIKE":
            return {"like": {"isLike": False, "count": count}}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to like")
