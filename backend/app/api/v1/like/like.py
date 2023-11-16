from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm.session import Session

from app.api.v1.auth import auth_utils
from app.api.v1.like import like_utils
from app.api.schemas import like_schema
from app.database import get_db

router = APIRouter(tags=["Like"])


@router.get("", status_code=status.HTTP_202_ACCEPTED)
async def like(
    request: Request,
    data: like_schema.like = Depends(),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        stat = await like_utils.add_like(data.post_id, decoded_dict.get("id"), db)
        if stat == "like":
            return {"status": stat}
        elif stat == "unlike":
            return {"status": stat}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to like")
