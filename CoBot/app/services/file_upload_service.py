from app.repository.filr_processing_repo import fileProcessingRepository
from app.config.config import mongo
from fastapi import  UploadFile, HTTPException




class file_p_services:
    def __init__(self):
        self.repo = fileProcessingRepository()
        self.data_insert=mongo
    async def upload_file(self, file: UploadFile, collection_name:str):
        if not file or not file.filename:
              raise HTTPException(status_code=400, detail="No file uploaded or empty filename")
        
        try:
            result = {}
            result["text"] = await self.repo.file_convert(file=file)
            
        except Exception as e:
              print(str(e))
              raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
                )
        collection = self.data_insert.get_collection(collection_name)
        if self.data_insert.insert_data(result, collection):
            return {"detail": "File processed successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail="Error uploading file"
                )