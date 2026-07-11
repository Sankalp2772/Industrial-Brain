from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class DocumentBase(BaseModel):
    original_filename: str
    file_size: int
    content_type: str

class DocumentResponse(DocumentBase):
    id: str
    filename: str
    upload_time: datetime
    status: str
    processing_status: str
    storage_path: str

    model_config = ConfigDict(from_attributes=True)

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int

class DocumentUploadResponse(DocumentResponse):
    pass
