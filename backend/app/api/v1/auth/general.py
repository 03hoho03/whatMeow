from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
import bcrypt
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError


from app.api.schemas import user_schema, default
from app import model
from app.database import get_db
from app.api.v1.auth import auth_utils


router = APIRouter(tags=["Basic Auth"])


@router.post("/register", response_model=default.ResourceId, status_code=status.HTTP_201_CREATED)
async def add_user(data: user_schema.GeneralUserAdd, db: Session = Depends(get_db)):
    row = model.User(**{"email": data.email, "username": data.username, "name": data.name})
    salt_value = bcrypt.gensalt()
    row.password = bcrypt.hashpw(data.password.encode(), salt_value)
    try:
        db.add(row)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email Duplicated")

    return row


@router.post("/login")
async def issue_token(response: Response, data: user_schema.LoginUser, db: Session = Depends(get_db)):
    print(data.email)
    print(data.password)
    user = db.query(model.User).filter(model.User.email == data.email).first()
    if bcrypt.checkpw(data.password.encode(), user.password.encode()):  # bcrypt.checkpw가 자동으로 salt값 추출 후 서로 비교해줌
        token_info = await auth_utils.social_create_access_token(user, db, exp=timedelta(minutes=720))
        response = JSONResponse(content=token_info.get("user"))
        response = await auth_utils.set_cookie_response(response, token_info)

        return response
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong Information")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, db: Session = Depends(get_db)):
    """
    refresh_token을 db에서 삭제 -> 더 이상 access_token 갱신 불가
    front 쪽에서도 access_token과 refresh_token 정보를 제거 후 로그인 화면으로 redirect해야함
    """
    access_token = request.cookies.get("accessToken")
    row = db.query(model.RefreshToken).filter_by(refresh_token=access_token).first()
    if row:
        db.delete(row)
        db.commit()
        return row.user_id
    else:
        raise HTTPException(status_cod=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Item Not Found")


@router.get("/check_refresh_token")
async def check_refresh_token(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("accessToken")
    return {"new_token": await auth_utils.verify_refesh_token(refresh_token, db)}
