from fastapi import APIRouter
from .auth import kakao, general, google
from .post import post
from .search import search
from .follow import follow

router = APIRouter()


router.include_router(kakao.router, prefix="/auth")
router.include_router(general.router, prefix="/auth")
router.include_router(google.router, prefix="/auth")
router.include_router(post.router, prefix="/post")
router.include_router(search.router, prefix="/search")
router.include_router(follow.router, prefix="/follow")
