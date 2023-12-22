from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService, readService

router = APIRouter(tags=["UserV2"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.GeneralUserReturn)
async def register(data: schema.GeneralUserAdd, db: Session = Depends(get_db)):
    return await writeService.userRegister(data, db)


@router.get("/duplicated", status_code=status.HTTP_200_OK)
async def checkDup(nickname: str, db: Session = Depends(get_db)):
    return await readService.nicknameDup(nickname, db)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(response: Response, data: schema.GeneralUserLogin, db: Session = Depends(get_db)):
    return await readService.userLogin(data, response, db)


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    access_token = request.state.access_token
    return await readService.userLogout(response, access_token.get("id"), db)
