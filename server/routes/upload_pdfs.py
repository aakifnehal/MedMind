from fastapi import UploadFile, APIRouter, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger


router = APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info("Received files for upload")
        load_vectorstore(files)  # Ensure vectorstore is loaded before processing
        logger.info("Vectorstore loaded successfully")
        return {"message": "Files uploaded successfully", "file_count": len(files)}


    except Exception as e:
        logger.exception("Error uploading PDFs")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})