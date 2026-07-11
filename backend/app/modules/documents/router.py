from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.documents.service import DocumentService
from app.modules.documents.schema import DocumentUploadResponse, DocumentResponse, DocumentListResponse
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=SuccessResponse[DocumentUploadResponse], summary="Upload a document", description="Uploads a PDF or DOCX file, saves it to disk, and records metadata.")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    service = DocumentService(db)
    doc = service.upload_document(file)
    return SuccessResponse(message="Document uploaded successfully", data=doc)

@router.get("", response_model=SuccessResponse[DocumentListResponse], summary="List documents", description="Returns a list of all uploaded documents.")
def list_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = DocumentService(db)
    result = service.list_documents(skip=skip, limit=limit)
    return SuccessResponse(message="Documents retrieved successfully", data=result)

@router.get("/{doc_id}", response_model=SuccessResponse[DocumentResponse], summary="Get document details", description="Returns metadata for a specific document.")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    service = DocumentService(db)
    doc = service.get_document(doc_id)
    return SuccessResponse(message="Document retrieved successfully", data=doc)

@router.delete("/{doc_id}", response_model=SuccessResponse[None], summary="Delete document", description="Deletes a document file and its metadata.")
def delete_document(doc_id: str, db: Session = Depends(get_db)):
    service = DocumentService(db)
    service.delete_document(doc_id)
    return SuccessResponse(message="Document deleted successfully")
