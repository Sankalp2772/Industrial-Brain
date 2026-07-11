from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.embeddings.service import EmbeddingService
from app.modules.embeddings.schema import EmbedResponse, SemanticSearchRequest, SearchResponse
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/embeddings", tags=["embeddings"])

@router.post("/documents/{doc_id}/embed", response_model=SuccessResponse[EmbedResponse], summary="Generate Embeddings", description="Chunks text, generates embeddings via Gemini, and stores in ChromaDB.")
def generate_embeddings(doc_id: str, db: Session = Depends(get_db)):
    service = EmbeddingService(db)
    result = service.generate_embeddings(doc_id)
    return SuccessResponse(message="Embeddings generated successfully", data=result)

@router.get("/documents/{doc_id}/chunks", response_model=SuccessResponse[list], summary="Get Document Chunks", description="Returns the generated chunks from ChromaDB for a specific document.")
def get_chunks(doc_id: str, db: Session = Depends(get_db)):
    service = EmbeddingService(db)
    result = service.get_document_chunks(doc_id)
    return SuccessResponse(message="Chunks retrieved successfully", data=result)

@router.post("/search/semantic", response_model=SuccessResponse[SearchResponse], summary="Semantic Search", description="Retrieves top K most relevant chunks based on a semantic query.")
def semantic_search(request: SemanticSearchRequest, db: Session = Depends(get_db)):
    service = EmbeddingService(db)
    results = service.search_semantic(request.query, request.top_k)
    return SuccessResponse(message="Semantic search completed", data={"results": results})
