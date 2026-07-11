from pydantic import BaseModel, Field
from typing import List, Optional

class CopilotQueryRequest(BaseModel):
    question: str = Field(..., description="The user's industrial question")

class Citation(BaseModel):
    document: str = Field(description="The source document ID")
    asset: Optional[str] = Field(None, description="The associated asset ID if applicable")
    chunk: Optional[str] = Field(None, description="The specific text chunk used as evidence")
    page: Optional[int] = Field(None, description="The page number if applicable")

class CopilotResponse(BaseModel):
    answer: str = Field(description="The generated answer")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    citations: List[Citation] = Field(default_factory=list, description="Verifiable sources used")
    related_assets: List[str] = Field(default_factory=list, description="Assets related to the answer")
    reasoning_steps: List[str] = Field(default_factory=list, description="Step-by-step logic used to arrive at the answer")

class HistoryItem(BaseModel):
    id: str
    question: str
    answer: str
    confidence: float
    created_at: str
