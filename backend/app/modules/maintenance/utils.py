from app.modules.graph.builder import neo4j_conn
from fastapi import HTTPException

def fetch_asset_context(asset_id: str) -> dict:
    if not neo4j_conn.driver:
        raise HTTPException(status_code=503, detail="Neo4j driver is not available.")
        
    query = """
    MATCH (a:Asset {id: $asset_id})-[r]-(connected)
    RETURN a, r, connected
    """
    
    context = {
        "asset": None,
        "incidents": [],
        "inspections": [],
        "work_orders": [],
        "maintenance_logs": [],
        "documents": []
    }
    
    try:
        with neo4j_conn.driver.session() as session:
            result = session.run(query, asset_id=asset_id)
            for record in result:
                if not context["asset"]:
                    context["asset"] = dict(record["a"])
                
                node = dict(record["connected"])
                labels = list(record["connected"].labels)
                
                if "Incident" in labels:
                    context["incidents"].append(node)
                elif "Inspection" in labels:
                    context["inspections"].append(node)
                elif "WorkOrder" in labels:
                    context["work_orders"].append(node)
                elif "MaintenanceLog" in labels:
                    context["maintenance_logs"].append(node)
                elif "Document" in labels or "SOP" in labels or "OEMManual" in labels:
                    context["documents"].append(node)
                    
        if not context["asset"]:
            raise HTTPException(status_code=404, detail="Asset not found in graph.")
            
        return context
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch asset context: {str(e)}")
