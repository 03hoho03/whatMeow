from fastapi import APIRouter, status, Depends, Request, Form, File, UploadFile
from sqlalchemy.orm.session import Session
from typing import List

from app.database import get_db
from . import schema
from .service import writeService

router = APIRouter(tags=["PostV2"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.PostReturn)
async def create(
    request: Request,
    content: str = Form(...),
    tags: List[str] = Form(None),
    cat_ids: List[int] = Form(None),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    access_token = request.state.access_token
    return await writeService.createPost(
        access_token.get("id"), access_token.get("username"), content, tags, cat_ids, files, db
    )
