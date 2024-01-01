from fastapi import APIRouter

from .user import controller as user
from .post import controller as post
from .comment import controller as comment
from .cat import controller as cat

router = APIRouter()
router.include_router(user.router, prefix="/v2/users")
router.include_router(post.router, prefix="/v2/post")
router.include_router(comment.router, prefix="/v2/comment")
router.include_router(cat.router, prefix="/v2/cat")
