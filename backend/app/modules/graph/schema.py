from pydantic import BaseModel
from typing import List, Dict, Any

class GraphBuildResponse(BaseModel):
    document_id: str
    nodes_created: int
    relationships_created: int
    duplicates_ignored: int
    status: str

class GraphStatsResponse(BaseModel):
    total_nodes: int
    total_relationships: int
    graph_density: float

class SubgraphResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
