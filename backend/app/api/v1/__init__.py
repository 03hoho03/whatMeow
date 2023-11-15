from fastapi import APIRouter
from .auth import kakao, general, google
from .post import post
from .search import search
from .follow import follow
from .comment import comment
from .like import like
from .user import user

router = APIRouter()

router.include_router(kakao.router, prefix="/v1/auth")
router.include_router(general.router, prefix="/v1/auth")
router.include_router(google.router, prefix="/v1/auth")
router.include_router(post.router, prefix="/v1/post")
router.include_router(search.router, prefix="/v1/search")
router.include_router(follow.router, prefix="/v1/follow")
router.include_router(comment.router, prefix="/v1/comment")
router.include_router(like.router, prefix="/v1/like")
router.include_router(user.router, prefix="/v1/user")
