from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

from app.api.schemas import user_schema, default
from app import model
from app.database import get_db
from app.api.v1.auth import auth_utils


router = APIRouter()


@router.post("/register", response_model=default.ResourceId, status_code=status.HTTP_201_CREATED)
async def add_user(data: user_schema.GeneralUserAdd, db: Session = Depends(get_db)):
    row = model.User(**{"email": data.email, "username": data.username, "name": data.name})
    salt_value = bcrypt.gensalt()
    row.password = bcrypt.hashpw(data.password.encode(), salt_value)
    try:
        db.add(row)
        db.commit()
    except IntegrityError:
        return {"error": "Email Duplicated."}

    return row


@router.post("/login")
async def issue_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == data.username).first()
    if bcrypt.checkpw(data.password.encode(), user.password.encode()):  # bcrypt.checkpw가 자동으로 salt값 추출 후 서로 비교해줌
        return await auth_utils.general_create_access_token(user, db, exp=timedelta(minutes=720))
    raise HTTPException(401)
