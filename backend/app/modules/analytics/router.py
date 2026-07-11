from fastapi import APIRouter
from app.modules.analytics.service import AnalyticsService
from app.modules.analytics.schema import DashboardAnalyticsResponse, DocumentAnalyticsResponse
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard", response_model=SuccessResponse[DashboardAnalyticsResponse], summary="Get Dashboard Analytics")
def get_dashboard():
    service = AnalyticsService()
    data = service.get_dashboard()
    return SuccessResponse(message="Dashboard analytics retrieved", data=data)

@router.get("/documents", response_model=SuccessResponse[DocumentAnalyticsResponse], summary="Get Document Analytics")
def get_documents():
    service = AnalyticsService()
    data = service.get_documents()
    return SuccessResponse(message="Document analytics retrieved", data=data)

# Placeholder routes
@router.get("/assets")
def get_assets():
    return SuccessResponse(message="Assets analytics", data={})

@router.get("/incidents")
def get_incidents():
    return SuccessResponse(message="Incident analytics", data={})

@router.get("/maintenance")
def get_maintenance():
    return SuccessResponse(message="Maintenance analytics", data={})

@router.get("/copilot")
def get_copilot():
    return SuccessResponse(message="Copilot analytics", data={})

@router.get("/performance")
def get_performance():
    return SuccessResponse(message="Performance analytics", data={})
