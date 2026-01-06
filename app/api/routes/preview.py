from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.schemas.barcode_preview import BarcodePreviewResponse
from app.domain.services.barcode_preview_service import BarcodePreviewService
from app.domain.models import BarcodePreview

router = APIRouter(prefix="/preview", tags=["Preview"])

@router.put("", response_model=BarcodePreviewResponse)
async def generate_preview(barcodePreview: BarcodePreview):
    try:
        file_id = BarcodePreviewService.generate_preview(barcodePreview)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate barcode preview: " + str(e))
    return {"file_id": file_id}

@router.get("/{file_id}")
async def get_preview(file_id: str):
    try:
        path = BarcodePreviewService.get_preview_path(file_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)
