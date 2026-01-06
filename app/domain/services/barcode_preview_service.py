# Barcode preview model
from app.schemas.barcode_preview import BarcodePreviewResponse
from app.domain.models import BarcodePreview

# Barcode generator core dependencies
from PIL import ImageOps # Image manipulation lib
import treepoem # Barcode Generator lib

# File management dependencies
import os # OS utilities library
import uuid

# Create previews directory if not exists
PREVIEW_DIR = "previews"
os.makedirs(PREVIEW_DIR, exist_ok=True)

DPI_MM = 23.622 # Conversion factor from px to mm at 600dpi

class BarcodePreviewService:
    
    @staticmethod
    def generate_preview(barcodePreview: BarcodePreview):

        # Convert mm to px
        height_px = barcodePreview.barcodeType.height * DPI_MM
        width_px = barcodePreview.barcodeType.width * DPI_MM
        
        # Generate a unique file UUID
        file_id = str(uuid.uuid4())
        file_path = os.path.join(PREVIEW_DIR, file_id + ".png")

        # Generate barcode image
        try:
            image = treepoem.generate_barcode(
                barcode_type = barcodePreview.barcodeType.encodeType,
                data = barcodePreview.data,
                options = {
                    "includetext" : bool(barcodePreview.barcodeType.showValue),
                    "scale": 5,
                    "size": (width_px, height_px),
                }
            )
        except Exception as e:
            raise Exception("Failed to generate barcode preview: " + str(e))
        
        # Save barcode image
        try:
            image = ImageOps.expand(image, fill="white").save(file_path)
        except Exception as e:
            raise Exception("Failed to save barcode preview: " + str(e))
        
        return file_id

    @staticmethod
    def get_preview_path(file_id: str) -> str:

        path = os.path.join(PREVIEW_DIR, file_id + ".png")

        if not os.path.exists(path):
            raise FileNotFoundError
        
        return path
