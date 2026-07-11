from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.graph.service import GraphService
from app.modules.graph.schema import GraphBuildResponse, GraphStatsResponse, SubgraphResponse
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/graph", tags=["graph"])

@router.post("/documents/{doc_id}/graph", response_model=SuccessResponse[GraphBuildResponse], summary="Build graph from document", description="Reads a validated Knowledge Object and MERGEs it into the Neo4j graph.")
def build_document_graph(doc_id: str, db: Session = Depends(get_db)):
    service = GraphService(db)
    result = service.build_graph_for_document(doc_id)
    return SuccessResponse(message="Graph built successfully", data=result)

@router.post("/rebuild", response_model=SuccessResponse[dict], summary="Rebuild entire graph", description="Batch processes all Completed Knowledge Objects into the graph.")
def rebuild_graph(db: Session = Depends(get_db)):
    service = GraphService(db)
    result = service.rebuild_entire_graph()
    return SuccessResponse(message="Graph rebuilt successfully", data=result)

@router.get("/stats", response_model=SuccessResponse[GraphStatsResponse], summary="Get Graph Stats", description="Returns total nodes, relationships, and density.")
def get_graph_stats(db: Session = Depends(get_db)):
    service = GraphService(db)
    result = service.get_stats()
    return SuccessResponse(message="Graph stats retrieved successfully", data=result)

@router.get("/asset/{asset_id}", response_model=SuccessResponse[SubgraphResponse], summary="Get Asset Subgraph", description="Returns the local connected graph (depth=1) for a specific asset.")
def get_asset_subgraph(asset_id: str, db: Session = Depends(get_db)):
    service = GraphService(db)
    result = service.get_asset_subgraph(asset_id)
    return SuccessResponse(message="Asset subgraph retrieved successfully", data=result)
