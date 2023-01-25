from fastapi import APIRouter

from .v1.magic import router as magic_router


router = APIRouter()

router.include_router(magic_router, prefix="/magic")