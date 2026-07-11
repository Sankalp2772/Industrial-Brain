import time
import logging
from typing import Dict, Any
from app.modules.embeddings.service import EmbeddingService
from app.modules.graph.service import GraphService
from app.modules.copilot.utils import detect_assets_in_query

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self, db_session):
        self.embedding_service = EmbeddingService(db_session)
        self.graph_service = GraphService(db_session)
        
    def retrieve_context(self, question: str) -> Dict[str, Any]:
        """
        Executes parallel-ish retrieval from Chroma and Neo4j.
        """
        results = {
            "semantic_chunks": [],
            "graph_subgraphs": [],
            "detected_assets": [],
            "stats": {}
        }
        
        # 1. Detect Assets
        assets = detect_assets_in_query(question)
        results["detected_assets"] = assets
        
        # 2. Graph Retrieval
        graph_start = time.time()
        for asset in assets:
            try:
                subgraph = self.graph_service.get_asset_subgraph(asset)
                if subgraph and subgraph.get("nodes"):
                    results["graph_subgraphs"].append(subgraph)
            except Exception as e:
                logger.warning(f"Graph retrieval failed for {asset}: {e}")
        results["stats"]["graph_time"] = time.time() - graph_start
        
        # 3. Semantic Retrieval
        embed_start = time.time()
        try:
            chunks = self.embedding_service.search_semantic(question, top_k=5)
            results["semantic_chunks"] = chunks
        except Exception as e:
            logger.warning(f"Semantic retrieval failed: {e}")
        results["stats"]["embed_time"] = time.time() - embed_start
        
        return results
