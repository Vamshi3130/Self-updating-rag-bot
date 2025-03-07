from fastapi import APIRouter
from app.router.v1 import file_upload, query_api

router = APIRouter()

router.include_router(file_upload.router)
router.include_router(query_api.router)