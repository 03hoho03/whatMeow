from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService, readService


router = APIRouter(tags=["FollowV2"])


@router.post("/{toUserId}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.FollowReturn)
async def apply(request: Request, toUserId: int, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await writeService.applyFollow(access_token.get("id"), toUserId, db)


# access_token을 받아서 없으면 모든 Item들을 Follow하게 만들고
# ID 추출 후, 팔로우 거 그거 알지 그거 ㄱㄱ
@router.get("/{userId}/following", status_code=status.HTTP_200_OK)
async def getFollowing(userId: int, db: Session = Depends(get_db)):
    return await readService.getFollowingUsers(userId, db)


@router.get("/{userId}/follower", status_code=status.HTTP_200_OK)
async def getFollower(userId: int, db: Session = Depends(get_db)):
    return await readService.getFollowerUsers(userId, db)
