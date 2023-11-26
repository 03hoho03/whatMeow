from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm.session import Session

from app import model
from app.api.v1.auth import auth_utils
from app.api.v1.follow import follow_utils
from app.database import get_db

router = APIRouter(tags=["Follow"])


@router.post("/follow/{toFollow}", status_code=status.HTTP_202_ACCEPTED)
async def add_follower(
    request: Request,
    toFollow: str,
    db: Session = Depends(get_db),
):
    access_token = request.cookies.get("accessToken")
    decoded_dict = await auth_utils.verify_access_token(access_token)
    if decoded_dict:
        stat, count = await follow_utils.add_follow(toFollow, decoded_dict.get("id"), db)
        if stat == "FOLLOW":
            return {"follow": {"isFollowing": True, "count": count}}
        else:
            return {"follow": {"isFollowing": False, "count": count}}


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
