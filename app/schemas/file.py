from pydantic import BaseModel

# File upload response
class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str

# Get stats response
class GetStatsResponse(BaseModel):
    rows: int
    columns: list[str]
