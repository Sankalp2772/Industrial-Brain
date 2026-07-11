import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.modules.documents.repository import DocumentRepository
from app.modules.documents.models import Document

ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

class DocumentService:
    def __init__(self, db: Session):
        self.repo = DocumentRepository(db)

    def upload_document(self, file: UploadFile) -> Document:
        # Validate content type
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and DOCX are allowed.")
        
        # Read file to check size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE / (1024*1024):.0f}MB.")

        # Generate unique filename
        ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        storage_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Save file to disk
        try:
            with open(storage_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

        # Create DB record
        doc_data = {
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_size": file_size,
            "content_type": file.content_type,
            "storage_path": storage_path,
        }
        
        return self.repo.create(doc_data)

    def get_document(self, doc_id: str) -> Document:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc

    def list_documents(self, skip: int = 0, limit: int = 100):
        docs = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count()
        return {"documents": docs, "total": total}

    def delete_document(self, doc_id: str):
        doc = self.get_document(doc_id)
        
        # Delete file from disk
        if os.path.exists(doc.storage_path):
            try:
                os.remove(doc.storage_path)
            except Exception as e:
                pass # Log error in a real app, proceed to DB deletion
                
        # Delete DB record
        self.repo.delete(doc_id)
        return True
