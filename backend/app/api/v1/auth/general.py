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


router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=default.ResourceId, status_code=status.HTTP_201_CREATED)
async def add_user(data: user_schema.GeneralUserAdd, db: Session = Depends(get_db)):
    username = await auth_utils.get_random_username(db)
    try:
        url = await auth_utils.upload_default_image(username)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="An Error Occured while Uploading default Image",
        )
    row = model.User(
        **{
            "email": data.email,
            "nickname": data.nickname,
            "name": data.name,
            "username": username,
            "profile_image": url,
        }
    )
    salt_value = bcrypt.gensalt()
    row.password = bcrypt.hashpw(data.password.encode(), salt_value)
    try:
        db.add(row)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email Duplicated")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="An Error Occured while registering"
        )

    return row


@router.post("/login")
async def issue_token(response: Response, data: user_schema.LoginUser, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == data.email).first()
    if bcrypt.checkpw(data.password.encode(), user.password.encode()):  # bcrypt.checkpw가 자동으로 salt값 추출 후 서로 비교해줌
        token_info = await auth_utils.social_create_access_token(user, db, exp=timedelta(minutes=720))
        response = JSONResponse(content=token_info.get("user"))
        response = await auth_utils.set_cookie_response(response, token_info)

        return response
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong Information")


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    로그인 화면으로 redirect해야함
    """
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        try:
            row = db.query(model.RefreshToken).filter_by(user_id=decoded_dict.get("id")).first()
            db.delete(row)
            db.commit()
            response = JSONResponse(content=row.user_id)
            response = await auth_utils.set_cookie_expzero(response)
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"An Error {e} occured")
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.get("/token/refresh")
async def check_refresh_token(request: Request, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        return {"new_token": await auth_utils.verify_refesh_token(decoded_dict.get("id"), db)}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")
