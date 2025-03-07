from fastapi import APIRouter,UploadFile
from app.services.file_upload_service import file_p_services

router=APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    _services=file_p_services()
    return await _services.upload_file(file=file, collection_name='Docs')

@router.post("/salesupload")
async def upload_file(file: UploadFile):
    _services=file_p_services()
    return await _services.upload_file(file=file,collection_name= 'SalesDocs')

@router.post("/operationsupload")
async def upload_file(file: UploadFile):
    _services=file_p_services()
    return await _services.upload_file(file=file,collection_name= 'OperationsDocs')