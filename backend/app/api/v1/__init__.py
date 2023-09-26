from fastapi import APIRouter
from .auth import kakao, general, google
from .post import post

router = APIRouter()
router.include_router(kakao.router, prefix="/auth")
router.include_router(general.router, prefix="/auth")
router.include_router(google.router, prefix="/auth")
router.include_router(post.router, prefix="/post")
