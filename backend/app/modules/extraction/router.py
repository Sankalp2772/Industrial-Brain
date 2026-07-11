from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.extraction.service import ExtractionService
from app.modules.extraction.schema import ExtractionResponse, TextResponse
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/documents", tags=["extraction"])

@router.post("/{doc_id}/extract", response_model=SuccessResponse[ExtractionResponse], summary="Extract document text", description="Runs the extraction pipeline on a specific document.")
def trigger_extraction(doc_id: str, db: Session = Depends(get_db)):
    service = ExtractionService(db)
    result = service.extract_document(doc_id)
    return SuccessResponse(message="Extraction pipeline completed successfully", data=result)

@router.get("/{doc_id}/text", response_model=SuccessResponse[TextResponse], summary="Get extracted text", description="Returns the full extracted text for a document.")
def get_text(doc_id: str, db: Session = Depends(get_db)):
    service = ExtractionService(db)
    text = service.get_extracted_text(doc_id, preview=False)
    return SuccessResponse(message="Text retrieved successfully", data={"document_id": doc_id, "text": text})

@router.get("/{doc_id}/preview", response_model=SuccessResponse[TextResponse], summary="Get text preview", description="Returns the first 1000 characters of the extracted text.")
def get_preview(doc_id: str, db: Session = Depends(get_db)):
    service = ExtractionService(db)
    text = service.get_extracted_text(doc_id, preview=True)
    return SuccessResponse(message="Text preview retrieved successfully", data={"document_id": doc_id, "text": text})

@router.post("/{doc_id}/knowledge", response_model=SuccessResponse[dict], summary="Generate Knowledge Object", description="Transforms text into structured JSON Knowledge using Gemini.")
def trigger_knowledge_generation(doc_id: str, db: Session = Depends(get_db)):
    service = ExtractionService(db)
    result = service.generate_knowledge_object(doc_id)
    return SuccessResponse(message="Knowledge Object generated successfully", data=result)

@router.get("/{doc_id}/knowledge", response_model=SuccessResponse[dict], summary="Get validated Knowledge Object", description="Returns the structured JSON Knowledge Object.")
def get_knowledge(doc_id: str, db: Session = Depends(get_db)):
    service = ExtractionService(db)
    result = service.get_knowledge_object(doc_id)
    return SuccessResponse(message="Knowledge Object retrieved successfully", data={"document_id": doc_id, "knowledge": result})

@router.get("/{doc_id}/knowledge/raw", response_model=SuccessResponse[TextResponse], summary="Get raw Knowledge generation output", description="Returns the raw Gemini output for debugging.")
def get_knowledge_raw(doc_id: str, db: Session = Depends(get_db)):
    service = ExtractionService(db)
    result = service.get_raw_knowledge(doc_id)
    return SuccessResponse(message="Raw Knowledge retrieved successfully", data={"document_id": doc_id, "text": result})
