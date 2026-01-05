# FastAPI dependencies
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Barcode generator core dependecies
from PIL import ImageOps
import treepoem # Barcode generator library

# CSV treatment dependencies
import pandas as pd # CSV utilities library

# File management dependencies
import uuid # UUID utilities library
import os # OS utilities library

# Class definition
class BarcodeType(BaseModel):
    encodeType: str
    height: float
    width: float
    showValue: bool

class BarcodePreview(BaseModel):
    barcodeType: BarcodeType
    data: str

app = FastAPI()

# Create working directories if not exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

PREVIEW_DIR = "previews"
os.makedirs(PREVIEW_DIR, exist_ok=True)

# Px to mm conversion at 600dpi
DPI_MM = 23.622

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Generate a unique file ID
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + ".csv")

    try:
        # Save the uploaded file in the temporary folder
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
        except Exception:
            # Remove the temporary file if reading failed
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Invalid CSV file")

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to upload file")
    
    return {
        "file_id": file_id,
        "rows": len(df),
        "columns": list(df.columns),
    }

@app.put("/barcode-preview")
async def barcode_preview(barcodePreview: BarcodePreview):

    # TODO: Check if the barcode type is supported

    # Convert mm to px
    height_px = int(barcodePreview.barcodeType.height * DPI_MM)
    width_px = int(barcodePreview.barcodeType.width * DPI_MM)

    # Generate a unique file ID
    file_id = str(uuid.uuid4())
    file_path = os.path.join(PREVIEW_DIR, file_id + ".png")

    # Generate a barcode image
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
        raise HTTPException(status_code=500, detail="Failed to generate barcode preview: " + str(e))

    # Save the barcode image
    try:
        image = ImageOps.expand(image, fill="white").save(file_path)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate barcode preview")

    # Return the barcode image file path
    return {"file_id": file_id}

@app.get("/barcode-preview/{file_id}")
async def get_barcode_preview(file_id: str):
    file_path = os.path.join(PREVIEW_DIR, file_id + ".png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)