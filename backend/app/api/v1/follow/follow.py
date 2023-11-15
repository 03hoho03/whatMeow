from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm.session import Session

from app import model
from app.api.v1.auth import auth_utils
from app.api.v1.follow import follow_utils
from app.api.schemas import follow_schema
from app.database import get_db

router = APIRouter(tags=["Follow"])


@router.get("/follow", status_code=status.HTTP_202_ACCEPTED)
async def add_follower(
    request: Request,
    data: follow_schema.add_follow = Depends(),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        # 여기에 팔로우 추가하는 함수 utils 에서 구현
        if await follow_utils.add_follow(data.to_follow, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to follow")


@router.get("/unfollow", status_code=status.HTTP_202_ACCEPTED)
async def delete_follower(
    request: Request,
    data: follow_schema.delete_follow = Depends(),
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        if await follow_utils.delete_follow(data.to_unfollow, decoded_dict.get("id"), db):
            return {"success": True}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follower Not Found")


# Follower, Following 리스트 확인용 엔드포인트


@router.get("/following", status_code=status.HTTP_200_OK)
async def return_following_users(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    user_info = db.query(model.User).filter_by(id=decoded_dict.get("id")).first()
    return user_info.following_lst


@router.get("/follower", status_code=status.HTTP_200_OK)
async def return_follower_users(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    user_info = db.query(model.User).filter_by(id=decoded_dict.get("id")).first()
    return user_info.follower_lst
