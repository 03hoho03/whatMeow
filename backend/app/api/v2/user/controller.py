from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService

router = APIRouter(tags=["UserV2"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.GeneralUserReturn)
async def register(data: schema.GeneralUserAdd, db: Session = Depends(get_db)):
    return await writeService.userRegister(data, db)
