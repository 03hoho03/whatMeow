from fastapi import APIRouter, Depends, status, Request, UploadFile, File, Form
from typing import List
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService

router = APIRouter(tags=["CatV2"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.CatReturn)
async def create(
    request: Request,
    catName: str = Form(...),
    age: int = Form(None),
    gender: str = Form(None),
    explain: str = Form(None),
    breed: str = Form(None),
    hashtags: List[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    access_token = request.state.access_token

    return await writeService.createCat(
        access_token.get("id"), catName, age, gender, explain, breed, file, hashtags, db
    )
