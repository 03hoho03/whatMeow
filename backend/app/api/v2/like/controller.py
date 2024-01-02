from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm.session import Session

from app.database import get_db
from . import schema
from .service import writeService

router = APIRouter(tags=["LikeV2"])


@router.post("/{postId}", status_code=status.HTTP_202_ACCEPTED)
async def apply(request: Request, postId: int, data: schema.ApplyLike, db: Session = Depends(get_db)):
    access_token = request.state.access_token

    return await writeService.applyLike(access_token.get("id"), postId, data, db)
