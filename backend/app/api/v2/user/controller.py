from fastapi import APIRouter, Depends, status
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