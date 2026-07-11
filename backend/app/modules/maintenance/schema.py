from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Recommendation(BaseModel):
    recommended_action: str
    priority: str
    reason: str
    evidence: List[str]
    expected_benefit: str

class RootCause(BaseModel):
    possible_cause: str
    confidence: str
    evidence: List[str]

class RiskAssessment(BaseModel):
    risk_score: int
    classification: str
    factors: List[str]

class MaintenanceAnalysisResponse(BaseModel):
    risk_score: int
    priority: str
    recommendations: List[Recommendation]
    root_causes: List[RootCause]
    evidence: List[str]
    confidence: str

class MaintenanceRecommendationResponse(BaseModel):
    recommendations: List[Recommendation]

class MaintenanceRCAResponse(BaseModel):
    root_causes: List[RootCause]
    confidence: str

class MaintenanceRiskResponse(BaseModel):
    risk_score: int
    classification: str
    factors: List[str]
