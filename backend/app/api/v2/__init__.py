from fastapi import APIRouter

from .user import controller as user

router = APIRouter()
router.include_router(user.router, prefix="/v2/users")
