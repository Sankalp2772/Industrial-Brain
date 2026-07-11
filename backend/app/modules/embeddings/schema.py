from pydantic import BaseModel, Field
from typing import List, Optional

class EmbedResponse(BaseModel):
    document_id: str
    chunk_count: int
    status: str
    embedded_at: str

class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="The query to search for")
    top_k: int = Field(5, description="Number of results to return")

class SearchResult(BaseModel):
    chunk: str
    score: float
    document: str
    asset: Optional[str] = None
    page: Optional[int] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
