from fastapi import APIRouter, UploadFile, File, HTTPException

from app.infrastructure.database_storage import DatabaseStorage
from app.schemas.file import FileUploadResponse, GetStatsResponse
from app.domain.services.database_service import DatabaseService
from app.domain.models import DatabaseFile

router = APIRouter(prefix="/database", tags=["Database"])

@router.post("", response_model=FileUploadResponse)
async def upload_database(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    file_id, path = DatabaseStorage.save(content)

    return {
        "file_id": file_id,
        "file_name": file.filename,
    }

@router.get("/{file_id}", response_model=GetStatsResponse)
async def get_stats(file_id: str):
    try:
        path = DatabaseStorage.get_path(file_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")
    
    database_file = DatabaseFile(id=file_id, path=path)
    
    return DatabaseService.get_stats(database_file)