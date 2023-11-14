from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session

from app.api.v1.auth import auth_utils
from app.api.v1.like import like_utils
from app.api.schemas import like_schema
from app.database import get_db

router = APIRouter(tags=["Like"])
security = HTTPBearer()


@router.get("/like", status_code=status.HTTP_202_ACCEPTED)
async def like(
    data: like_schema.like = Depends(),
    db: Session = Depends(get_db),
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        if await like_utils.add_like(data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to like")


@router.get("/unlike", status_code=status.HTTP_202_ACCEPTED)
async def unlike(
    data: like_schema.like = Depends(),
    db: Session = Depends(get_db),
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    decoded_dict = await auth_utils.verify_access_token(cred)
    if decoded_dict:
        if await like_utils.unlike(data.post_id, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to follow")
