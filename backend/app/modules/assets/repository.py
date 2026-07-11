import logging
from fastapi import HTTPException
from app.modules.graph.builder import neo4j_conn
from app.modules.graph.utils import normalize_entity_id

logger = logging.getLogger(__name__)

class AssetRepository:
    def get_all_assets(self) -> list:
        if not neo4j_conn.driver:
            raise HTTPException(status_code=503, detail="Neo4j driver is not available.")
            
        query = "MATCH (a:Asset) RETURN a"
        assets = []
        try:
            with neo4j_conn.driver.session() as session:
                result = session.run(query)
                for record in result:
                    node = record["a"]
                    assets.append(dict(node))
            return assets
        except Exception as e:
            logger.error(f"Failed to fetch assets: {e}")
            raise HTTPException(status_code=500, detail="Database query failed.")

    def get_asset_neighborhood(self, asset_id: str) -> dict:
        if not neo4j_conn.driver:
            raise HTTPException(status_code=503, detail="Neo4j driver is not available.")
            
        clean_id = normalize_entity_id(asset_id)
        # Pull all nodes up to depth 1
        query = """
        MATCH (a:Asset {id: $asset_id})-[r]-(connected)
        RETURN a, r, connected
        """
        
        neighborhood = {
            "asset": None,
            "relationships": [],
            "connected_nodes": []
        }
        
        try:
            with neo4j_conn.driver.session() as session:
                result = session.run(query, asset_id=clean_id)
                for record in result:
                    if not neighborhood["asset"]:
                        neighborhood["asset"] = dict(record["a"])
                    
                    neighborhood["relationships"].append({
                        "type": record["r"].type,
                        "source": record["r"].start_node.get("id"),
                        "target": record["r"].end_node.get("id")
                    })
                    
                    node_data = dict(record["connected"])
                    node_data["_labels"] = list(record["connected"].labels)
                    neighborhood["connected_nodes"].append(node_data)
                    
            return neighborhood
        except Exception as e:
            logger.error(f"Failed to fetch asset neighborhood for {asset_id}: {e}")
            raise HTTPException(status_code=500, detail="Database query failed.")
