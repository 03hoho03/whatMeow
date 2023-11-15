from fastapi import Depends, APIRouter, status
from sqlalchemy.orm.session import Session

from app.database import get_db

# from app.api.v1.auth import auth_utils
from app.api.v1.user import user_utils

router = APIRouter(tags=["User"])


@router.get("/duplicated", status_code=status.HTTP_200_OK)
async def is_duplicated(nickname: str, db: Session = Depends(get_db)):
    if await user_utils.check_duplication(nickname, db):
        return True
    else:
        return False
