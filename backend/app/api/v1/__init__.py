from fastapi import APIRouter
from .auth import kakao, general, google

router = APIRouter()
router.include_router(kakao.router, prefix="/auth")
router.include_router(general.router, prefix="/auth")
router.include_router(google.router, prefix="/auth")
