from pydantic import BaseModel

# Barcode preview response
class BarcodePreviewResponse(BaseModel):
    file_id: str