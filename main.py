from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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