import time
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.copilot.service import CopilotService
from app.modules.copilot.schema import CopilotQueryRequest, HistoryItem
from app.modules.copilot.retriever import HybridRetriever
from app.modules.copilot.generator import CopilotGenerator, GEMINI_MODEL
from app.modules.embeddings.repository import chroma_repo
from app.modules.graph.builder import Neo4jConnection
from app.shared.responses import SuccessResponse
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/copilot", tags=["copilot"])


@router.post("/query", response_model=SuccessResponse[dict], summary="Query Copilot",
             description="Executes hybrid retrieval and generates an answer with citations.")
def query_copilot(request: CopilotQueryRequest, db: Session = Depends(get_db)):
    service = CopilotService(db)
    result = service.query(request)
    return SuccessResponse(message="Copilot answered successfully", data=result)


@router.get("/history", response_model=SuccessResponse[List[HistoryItem]], summary="Get Copilot History",
            description="Returns recent questions and answers.")
def get_copilot_history(db: Session = Depends(get_db)):
    service = CopilotService(db)
    result = service.get_history()
    return SuccessResponse(message="History retrieved successfully", data=result)


@router.get("/health", summary="Copilot Health Check",
            description="Checks connectivity to all AI pipeline components.")
def copilot_health(db: Session = Depends(get_db)):
    results = {
        "gemini_connected": False,
        "neo4j_connected": False,
        "chroma_connected": False,
        "knowledge_ready": False,
        "embeddings_ready": False,
        "copilot_ready": False,
        "model": GEMINI_MODEL,
        "chroma_chunk_count": 0,
    }

    # Check ChromaDB
    try:
        count = chroma_repo.collection.count()
        results["chroma_connected"] = True
        results["chroma_chunk_count"] = count
        results["embeddings_ready"] = count > 0
    except Exception as e:
        logger.warning(f"Chroma health check failed: {e}")

    # Check Neo4j
    try:
        conn = Neo4jConnection()
        conn.driver.verify_connectivity()
        results["neo4j_connected"] = True
        results["knowledge_ready"] = True
    except Exception as e:
        logger.warning(f"Neo4j health check failed: {e}")

    # Check Gemini (lightweight ping)
    try:
        gen = CopilotGenerator()
        text = gen.generate_text("Reply with exactly: OK")
        results["gemini_connected"] = "OK" in text or len(text) > 0
    except Exception as e:
        logger.warning(f"Gemini health check failed: {e}")

    results["copilot_ready"] = (
        results["gemini_connected"]
        and results["chroma_connected"]
        and results["embeddings_ready"]
    )

    return SuccessResponse(message="Health check complete", data=results)


@router.post("/debug", summary="Debug Copilot Pipeline",
             description="Runs the full pipeline and returns detailed diagnostics for a question.")
def debug_copilot(request: CopilotQueryRequest, db: Session = Depends(get_db)):
    """Debug endpoint — returns every intermediate stage of the pipeline."""
    t0 = time.time()

    debug_info = {
        "question": request.question,
        "detected_assets": [],
        "graph_nodes_retrieved": 0,
        "graph_relationships_retrieved": 0,
        "embedding_matches": 0,
        "prompt_length": 0,
        "gemini_status": "not_called",
        "retrieval_latency_ms": 0,
        "generation_latency_ms": 0,
        "total_latency_ms": 0,
        "final_answer": None,
        "error": None,
    }

    try:
        # Retrieval stage
        retriever = HybridRetriever(db)
        t_ret = time.time()
        context = retriever.retrieve_context(request.question)
        debug_info["retrieval_latency_ms"] = round((time.time() - t_ret) * 1000)
        debug_info["detected_assets"] = context["detected_assets"]

        graph_nodes = sum(len(sg.get("nodes", [])) for sg in context["graph_subgraphs"])
        graph_edges = sum(len(sg.get("edges", [])) for sg in context["graph_subgraphs"])
        debug_info["graph_nodes_retrieved"] = graph_nodes
        debug_info["graph_relationships_retrieved"] = graph_edges
        debug_info["embedding_matches"] = len(context["semantic_chunks"])

        # Generation stage
        from app.modules.copilot.citations import format_graph_context, format_semantic_context
        merged_graph = "".join(format_graph_context(sg) + "\n" for sg in context["graph_subgraphs"])
        merged_semantic = format_semantic_context(context["semantic_chunks"])
        prompt = merged_graph + "\n" + merged_semantic
        debug_info["prompt_length"] = len(prompt)

        gen = CopilotGenerator()
        confidence = gen.calculate_confidence(context["graph_subgraphs"], context["semantic_chunks"])

        t_gen = time.time()
        try:
            answer_obj = gen.generate_answer(
                question=request.question,
                formatted_graph=merged_graph,
                formatted_semantic=merged_semantic,
                confidence_score=confidence
            )
            debug_info["gemini_status"] = "success"
            debug_info["final_answer"] = answer_obj.answer
        except Exception as gen_err:
            debug_info["gemini_status"] = f"error: {str(gen_err)[:120]}"

        debug_info["generation_latency_ms"] = round((time.time() - t_gen) * 1000)

    except Exception as e:
        debug_info["error"] = str(e)

    debug_info["total_latency_ms"] = round((time.time() - t0) * 1000)
    return SuccessResponse(message="Debug complete", data=debug_info)

