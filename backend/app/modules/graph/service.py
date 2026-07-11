import os
import time
import json
import logging
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.modules.documents.repository import DocumentRepository
from app.modules.graph.builder import neo4j_conn
from app.modules.graph.utils import normalize_entity_id, normalize_property
from app.modules.graph.queries import (
    MERGE_DOCUMENT, MERGE_ASSET, MERGE_ENGINEER, MERGE_INSPECTION,
    MERGE_INCIDENT, MERGE_MAINTENANCE_LOG, MERGE_SOP, MERGE_WORK_ORDER,
    MERGE_OEM_MANUAL, MERGE_DEPARTMENT, get_merge_relationship_query,
    GET_GRAPH_STATS, GET_ASSET_SUBGRAPH
)

logger = logging.getLogger(__name__)

# Map node types to their corresponding MERGE queries
NODE_QUERY_MAP = {
    "Document": MERGE_DOCUMENT,
    "Asset": MERGE_ASSET,
    "Engineer": MERGE_ENGINEER,
    "Inspection": MERGE_INSPECTION,
    "Incident": MERGE_INCIDENT,
    "MaintenanceLog": MERGE_MAINTENANCE_LOG,
    "SOP": MERGE_SOP,
    "WorkOrder": MERGE_WORK_ORDER,
    "OEMManual": MERGE_OEM_MANUAL,
    "Department": MERGE_DEPARTMENT
}

class GraphService:
    def __init__(self, db: Session):
        self.repo = DocumentRepository(db)

    def _process_knowledge_object(self, data: dict, session) -> dict:
        """
        Parses a knowledge object and runs MERGE queries via a Neo4j session.
        Returns counts of created entities.
        """
        nodes_created = 0
        relationships_created = 0
        
        # 1. Process Document Node
        doc_data = data.get("document", {})
        if doc_data and "id" in doc_data:
            doc_id = normalize_entity_id(doc_data["id"])
            doc_type = normalize_property(doc_data.get("type", "Document"))
            session.run(MERGE_DOCUMENT, id=doc_id, properties={"type": doc_type})
            nodes_created += 1

        # 2. Process Lists of Nodes
        node_lists = [
            ("Asset", data.get("assets", [])),
            ("Engineer", data.get("engineers", [])),
            ("MaintenanceLog", data.get("maintenance_actions", [])),
            ("Inspection", data.get("inspection_findings", [])),
            ("Incident", data.get("incidents", []))
        ]

        for node_type, items in node_lists:
            query = NODE_QUERY_MAP.get(node_type)
            if not query:
                continue
                
            for item in items:
                if "id" not in item:
                    continue
                item_id = normalize_entity_id(item.pop("id"))
                # Normalize remaining properties
                properties = {k: normalize_property(v) for k, v in item.items()}
                session.run(query, id=item_id, properties=properties)
                nodes_created += 1

        # 3. Process Relationships
        for rel in data.get("relationships", []):
            source_id = normalize_entity_id(rel.get("source_id"))
            target_id = normalize_entity_id(rel.get("target_id"))
            rel_type = normalize_property(rel.get("relationship_type"))
            
            if not source_id or not target_id or not rel_type:
                continue
                
            query = get_merge_relationship_query(rel_type)
            session.run(query, source_id=source_id, target_id=target_id)
            relationships_created += 1

        return {
            "nodes_created": nodes_created,
            "relationships_created": relationships_created
        }

    def build_graph_for_document(self, doc_id: str) -> dict:
        doc = self.repo.get_by_id(doc_id)
        if not doc or doc.knowledge_status != "Completed":
            raise HTTPException(status_code=404, detail="Knowledge Object not found or not ready.")

        knowledge_path = os.path.join(settings.KNOWLEDGE_DIR, f"{doc_id}.json")
        if not os.path.exists(knowledge_path):
            raise HTTPException(status_code=404, detail="Knowledge Object JSON file is missing.")
            
        with open(knowledge_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not neo4j_conn.driver:
            raise HTTPException(status_code=503, detail="Neo4j driver is not initialized or unavailable.")

        start_time = time.time()
        self.repo.update(doc_id, {"graph_status": "Processing"})

        try:
            with neo4j_conn.driver.session() as session:
                counts = self._process_knowledge_object(data, session)
            
            duration = time.time() - start_time
            logger.info(f"Graph built for {doc_id} in {duration:.2f}s. Nodes: {counts['nodes_created']}, Edges: {counts['relationships_created']}")

            self.repo.update(doc_id, {
                "graph_status": "Completed",
                "graph_synced_at": datetime.now(timezone.utc)
            })

            return {
                "document_id": doc_id,
                "nodes_created": counts["nodes_created"],
                "relationships_created": counts["relationships_created"],
                # We count everything processed, but MERGE inherently ignores duplicates
                "duplicates_ignored": 0,
                "status": "Completed"
            }
        except Exception as e:
            self.repo.update(doc_id, {"graph_status": "Failed"})
            logger.error(f"Graph build failed for {doc_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Neo4j transaction failed: {str(e)}")

    def rebuild_entire_graph(self) -> dict:
        if not neo4j_conn.driver:
            raise HTTPException(status_code=503, detail="Neo4j driver is not available.")
            
        docs = self.repo.get_all()
        total_nodes = 0
        total_edges = 0
        processed_docs = 0

        for doc in docs:
            if doc.knowledge_status == "Completed":
                try:
                    res = self.build_graph_for_document(doc.id)
                    total_nodes += res["nodes_created"]
                    total_edges += res["relationships_created"]
                    processed_docs += 1
                except Exception as e:
                    logger.error(f"Failed to process {doc.id} during rebuild: {str(e)}")

        return {
            "documents_processed": processed_docs,
            "total_nodes_processed": total_nodes,
            "total_relationships_processed": total_edges,
            "status": "Rebuild Complete"
        }

    def get_stats(self) -> dict:
        if not neo4j_conn.driver:
            raise HTTPException(status_code=503, detail="Neo4j driver is not available.")
            
        try:
            with neo4j_conn.driver.session() as session:
                result = session.run(GET_GRAPH_STATS).single()
                nodes = result["total_nodes"] if result else 0
                rels = result["total_relationships"] if result else 0
                density = (rels / (nodes * (nodes - 1))) if nodes > 1 else 0
                
            return {
                "total_nodes": nodes,
                "total_relationships": rels,
                "graph_density": density
            }
        except Exception as e:
            logger.error(f"Failed to fetch stats: {str(e)}")
            raise HTTPException(status_code=500, detail="Neo4j query failed.")

    def get_asset_subgraph(self, asset_id: str) -> dict:
        if not neo4j_conn.driver:
            raise HTTPException(status_code=503, detail="Neo4j driver is not available.")
            
        clean_id = normalize_entity_id(asset_id)
        nodes_dict = {}
        edges_list = []
        
        try:
            with neo4j_conn.driver.session() as session:
                result = session.run(GET_ASSET_SUBGRAPH, asset_id=clean_id)
                for record in result:
                    a = record["a"]
                    r = record["r"]
                    c = record["connected"]
                    
                    if a and a.get("id") not in nodes_dict:
                        nodes_dict[a.get("id")] = dict(a)
                    if c and isinstance(c, list):
                        # Connected nodes might be a path depending on depth, but we set depth to 1
                        for node in c:
                            if node.get("id") not in nodes_dict:
                                nodes_dict[node.get("id")] = dict(node)
                    elif c and hasattr(c, 'get') and c.get("id") not in nodes_dict:
                        nodes_dict[c.get("id")] = dict(c)
                        
                    if r:
                        if isinstance(r, list):
                            for rel in r:
                                edges_list.append({
                                    "source": rel.start_node.get("id"),
                                    "target": rel.end_node.get("id"),
                                    "type": rel.type
                                })
                        else:
                            edges_list.append({
                                "source": r.start_node.get("id"),
                                "target": r.end_node.get("id"),
                                "type": r.type
                            })
                            
            # Deduplicate edges
            unique_edges = [dict(t) for t in {tuple(d.items()) for d in edges_list}]
            
            return {
                "nodes": list(nodes_dict.values()),
                "edges": unique_edges
            }
        except Exception as e:
            logger.error(f"Failed to fetch subgraph for {asset_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Neo4j query failed.")
