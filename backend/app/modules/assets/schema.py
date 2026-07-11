from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class AssetSummaryResponse(BaseModel):
    summary: str = Field(description="AI generated summary of the asset")

class AssetHealth(BaseModel):
    score: int
    classification: str
    reasons: List[str]

class TimelineEvent(BaseModel):
    date: str
    type: str
    description: str
    source_id: str

class AssetProfileResponse(BaseModel):
    asset_id: str
    type: str
    properties: Dict[str, Any]
    health: AssetHealth
    connected_documents: int
    connected_incidents: int
    connected_maintenance: int
    connected_sops: int

class AssetListResponse(BaseModel):
    assets: List[Dict[str, Any]]
