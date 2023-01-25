from fastapi import APIRouter

from .magic.api import router as magic_router


router = APIRouter()

router.include_router(magic_router, prefix="/v1")