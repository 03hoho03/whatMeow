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
