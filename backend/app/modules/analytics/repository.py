import sqlite3
import logging
from app.modules.graph.builder import neo4j_conn
from app.core.config import settings

logger = logging.getLogger(__name__)

class AnalyticsRepository:
    def get_sqlite_stats(self) -> dict:
        try:
            conn = sqlite3.connect("industrial_brain.db")
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM documents")
            total_docs = c.fetchone()[0]
            
            # Additional SQLite stats (Copilot logs, processing times) would go here
            # Assuming tables `copilot_history` and processing metrics exist
            
            conn.close()
            return {
                "total_documents": total_docs,
            }
        except Exception as e:
            logger.error(f"Failed to fetch SQLite stats: {e}")
            return {"total_documents": 0}

    def get_neo4j_stats(self) -> dict:
        if not neo4j_conn.driver:
            return {}
            
        stats = {
            "total_assets": 0,
            "total_nodes": 0,
            "total_relationships": 0,
            "health_distribution": {"Healthy": 0, "Warning": 0, "Critical": 0},
            "risk_distribution": {"Low": 0, "Medium": 0, "High": 0, "Critical": 0},
            "incident_count": 0,
            "maintenance_count": 0
        }
        
        try:
            with neo4j_conn.driver.session() as session:
                stats["total_nodes"] = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
                stats["total_relationships"] = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
                stats["total_assets"] = session.run("MATCH (a:Asset) RETURN count(a) AS c").single()["c"]
                stats["incident_count"] = session.run("MATCH (i:Incident) RETURN count(i) AS c").single()["c"]
                stats["maintenance_count"] = session.run("MATCH (m:MaintenanceLog) RETURN count(m) AS c").single()["c"]
                
                # In a real scenario, you might aggregate dynamic health scores here.
                # Since health is computed on the fly in Sprint 7, we'd either cache it in Neo4j, 
                # or compute an approximation. We'll simulate fetching cached distributions.
                stats["health_distribution"] = {"Healthy": 45, "Warning": 12, "Critical": 3}
                stats["risk_distribution"] = {"Low": 40, "Medium": 10, "High": 7, "Critical": 3}
                
        except Exception as e:
            logger.error(f"Failed to fetch Neo4j stats: {e}")
            
        return stats

    def get_chroma_stats(self) -> dict:
        # Since Chroma PersistentClient is a singleton in repository, 
        # we can fetch collection count if needed.
        # Returning mock static for now to avoid cross-module dependency complexites.
        return {"total_embeddings": 2450}
