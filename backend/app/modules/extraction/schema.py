from pydantic import BaseModel
from typing import Optional

class ExtractionResponse(BaseModel):
    document_id: str
    page_count: int
    processing_status: str

class TextResponse(BaseModel):
    document_id: str
    text: str

class KnowledgeGenerationResponse(BaseModel):
    document_id: str
    knowledge_status: str
    knowledge_generated_at: str

class KnowledgeResponse(BaseModel):
    document_id: str
    knowledge: dict

