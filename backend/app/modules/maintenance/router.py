from fastapi import APIRouter
from app.modules.maintenance.service import MaintenanceService
from app.modules.maintenance.schema import (
    MaintenanceAnalysisResponse,
    MaintenanceRCAResponse,
    MaintenanceRecommendationResponse,
    MaintenanceRiskResponse
)
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.post("/analyze/{asset_id}", response_model=SuccessResponse[MaintenanceAnalysisResponse], summary="Run Full Maintenance Analysis")
def run_maintenance_analysis(asset_id: str):
    service = MaintenanceService()
    analysis = service.analyze_asset(asset_id)
    return SuccessResponse(message="Analysis complete", data=analysis)

@router.get("/recommendations/{asset_id}", response_model=SuccessResponse[MaintenanceRecommendationResponse], summary="Get Maintenance Recommendations")
def get_recommendations(asset_id: str):
    service = MaintenanceService()
    recs = service.get_recommendations(asset_id)
    return SuccessResponse(message="Recommendations retrieved", data=recs)

@router.get("/rca/{asset_id}", response_model=SuccessResponse[MaintenanceRCAResponse], summary="Get Root Cause Analysis")
def get_rca(asset_id: str):
    service = MaintenanceService()
    rca = service.get_rca(asset_id)
    return SuccessResponse(message="RCA retrieved", data=rca)

@router.get("/risk/{asset_id}", response_model=SuccessResponse[MaintenanceRiskResponse], summary="Get Asset Risk Score")
def get_risk(asset_id: str):
    service = MaintenanceService()
    risk = service.get_risk(asset_id)
    return SuccessResponse(message="Risk score retrieved", data=risk)
