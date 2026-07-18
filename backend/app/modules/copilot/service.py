import time
import logging
from sqlalchemy.orm import Session
from app.modules.copilot.retriever import HybridRetriever
from app.modules.copilot.citations import format_graph_context, format_semantic_context
from app.modules.copilot.generator import CopilotGenerator
from app.modules.copilot.schema import CopilotQueryRequest, CopilotResponse
from app.modules.copilot.models import CopilotHistory
from app.modules.copilot.fallback import match_curated, build_context_answer

logger = logging.getLogger(__name__)


class CopilotService:
    def __init__(self, db: Session):
        self.db = db
        self.retriever = HybridRetriever(db)
        self.generator = CopilotGenerator()

    def query(self, request: CopilotQueryRequest) -> dict:
        start_time = time.time()
        question = request.question.strip()

        # ----------------------------------------------------------------
        # LAYER 0 — Curated Q&A (greetings + 5 demo questions)
        # Always returns instantly with no API calls needed.
        # ----------------------------------------------------------------
        curated = match_curated(question)
        if curated:
            logger.info(f"Copilot: matched curated answer for: {question!r}")
            answer_obj = CopilotResponse(
                answer=curated["answer"],
                confidence=curated["confidence"],
                citations=[],
                related_assets=curated["related_assets"],
                reasoning_steps=curated["reasoning_steps"],
            )
            self._save_history(question, answer_obj)
            return self._build_response(answer_obj, 0, 0, time.time() - start_time)

        # ----------------------------------------------------------------
        # LAYER 1 — Hybrid Retrieval (ChromaDB + Neo4j)
        # ----------------------------------------------------------------
        retrieval_start = time.time()
        try:
            context = self.retriever.retrieve_context(question)
        except Exception as e:
            logger.warning(f"Retrieval failed: {e}")
            context = {"graph_subgraphs": [], "semantic_chunks": [], "detected_assets": []}
        retrieval_time = time.time() - retrieval_start

        merged_graph = "".join(
            format_graph_context(sg) + "\n" for sg in context["graph_subgraphs"]
        )
        merged_semantic = format_semantic_context(context["semantic_chunks"])
        base_confidence = self.generator.calculate_confidence(
            context["graph_subgraphs"], context["semantic_chunks"]
        )

        # ----------------------------------------------------------------
        # LAYER 2 — Gemini LLM generation (with retry + key rotation)
        # ----------------------------------------------------------------
        gen_start = time.time()
        answer_obj: CopilotResponse | None = None

        try:
            answer_obj = self.generator.generate_answer(
                question=question,
                formatted_graph=merged_graph,
                formatted_semantic=merged_semantic,
                confidence_score=base_confidence,
            )
            logger.info("Copilot: Gemini generation succeeded")
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
                logger.warning("Gemini quota exhausted — falling back to context synthesis")
            else:
                logger.error(f"Gemini generation error: {err[:120]}")

        gen_time = time.time() - gen_start

        # ----------------------------------------------------------------
        # LAYER 3 — Context-only fallback (no LLM, uses retrieved data)
        # ----------------------------------------------------------------
        if answer_obj is None:
            logger.info("Copilot: using context-synthesis fallback")
            answer_obj = build_context_answer(
                question=question,
                graph_subgraphs=context["graph_subgraphs"],
                semantic_chunks=context["semantic_chunks"],
                detected_assets=context["detected_assets"],
            )

        self._save_history(question, answer_obj)
        total_time = time.time() - start_time
        logger.info(
            f"Copilot complete. Total: {total_time:.2f}s "
            f"(Retrieve: {retrieval_time:.2f}s, Generate: {gen_time:.2f}s)"
        )
        return self._build_response(answer_obj, retrieval_time, gen_time, total_time)

    def _build_response(self, answer_obj: CopilotResponse, r_time: float, g_time: float, total: float) -> dict:
        return {
            "answer": answer_obj.answer,
            "confidence": answer_obj.confidence,
            "citations": [c.model_dump() for c in answer_obj.citations],
            "related_assets": answer_obj.related_assets,
            "reasoning_steps": answer_obj.reasoning_steps,
            "stats": {
                "total_time_sec": round(total, 2),
                "retrieval_time_sec": round(r_time, 2),
                "generation_time_sec": round(g_time, 2),
            },
        }

    def _save_history(self, question: str, answer_obj: CopilotResponse) -> None:
        try:
            history_item = CopilotHistory(
                question=question,
                answer=answer_obj.answer,
                confidence=answer_obj.confidence,
            )
            self.db.add(history_item)
            self.db.commit()
        except Exception as e:
            logger.warning(f"Failed to save copilot history: {e}")

    def get_history(self) -> list:
        items = (
            self.db.query(CopilotHistory)
            .order_by(CopilotHistory.created_at.desc())
            .limit(50)
            .all()
        )
        return [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "confidence": item.confidence,
                "created_at": item.created_at.isoformat(),
            }
            for item in items
        ]
