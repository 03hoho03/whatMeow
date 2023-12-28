from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService

router = APIRouter(tags=["CommentV2"])


@router.post("/{postId}", status_code=status.HTTP_201_CREATED, response_model=schema.CommentReturn)
async def create(request: Request, data: schema.CommentAdd, postId: int, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await writeService.createComment(access_token.get("id"), postId, data, db)


@router.delete("/{commentId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(request: Request, commentId, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await writeService.deleteComment(access_token.get("id"), commentId, db)


@router.put("/{commentId}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.CommentReturn)
async def update(request: Request, data: schema.CommentAdd, commentId: int, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await writeService.updateComment(access_token.get("id"), commentId, data, db)
