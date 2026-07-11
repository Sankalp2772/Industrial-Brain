from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.copilot.service import CopilotService
from app.modules.copilot.schema import CopilotQueryRequest, HistoryItem
from app.shared.responses import SuccessResponse
from typing import List

router = APIRouter(prefix="/copilot", tags=["copilot"])

@router.post("/query", response_model=SuccessResponse[dict], summary="Query Copilot", description="Executes hybrid retrieval and generates an answer with citations.")
def query_copilot(request: CopilotQueryRequest, db: Session = Depends(get_db)):
    service = CopilotService(db)
    result = service.query(request)
    return SuccessResponse(message="Copilot answered successfully", data=result)

@router.get("/history", response_model=SuccessResponse[List[HistoryItem]], summary="Get Copilot History", description="Returns recent questions and answers.")
def get_copilot_history(db: Session = Depends(get_db)):
    service = CopilotService(db)
    result = service.get_history()
    return SuccessResponse(message="History retrieved successfully", data=result)
