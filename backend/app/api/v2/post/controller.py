from fastapi import APIRouter, status, Depends, Request, Form, File, UploadFile
from sqlalchemy.orm.session import Session
from typing import List

from app.database import get_db
from . import schema
from .service import writeService, readService

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
    return await writeService.createPost(access_token.get("id"), content, tags, cat_ids, files, db)


@router.get("/{postId}", status_code=status.HTTP_200_OK)
async def find(request: Request, postId: int, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await readService.findDetailedPost(access_token.get("id") if access_token else None, postId, db)


@router.delete("/{postId}", status_code=status.HTTP_204_NO_CONTENT)
async def post_delete(request: Request, postId: int, db: Session = Depends(get_db)):
    access_token = request.state.access_token
    return await writeService.deletePost(access_token.get("id") if access_token else None, postId, db)


@router.get("/search/main", status_code=status.HTTP_200_OK)
async def cursorMain(request: Request, key: int = None, db: Session = Depends(get_db)):
    access_token = request.state.access_token
    return await readService.searchMainFeed(access_token.get("id") if access_token else None, key, db)
