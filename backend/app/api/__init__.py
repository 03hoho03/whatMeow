from fastapi import APIRouter

from . import v1
from . import v2

router = APIRouter()
router.include_router(v1.router, prefix="/api")
router.include_router(v2.router, prefix="/api")
