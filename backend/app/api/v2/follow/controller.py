from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService


router = APIRouter(tags=["FollowV2"])


# Follow 추가 및 삭제 담당 함수
@router.post("/{toUserId}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.FollowReturn)
async def apply(request: Request, toUserId: int, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await writeService.applyFollow(access_token.get("id"), toUserId, db)
