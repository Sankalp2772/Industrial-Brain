import time
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.copilot.retriever import HybridRetriever
from app.modules.copilot.citations import format_graph_context, format_semantic_context
from app.modules.copilot.generator import CopilotGenerator
from app.modules.copilot.schema import CopilotQueryRequest, CopilotResponse
from app.modules.copilot.models import CopilotHistory

logger = logging.getLogger(__name__)

class CopilotService:
    def __init__(self, db: Session):
        self.db = db
        self.retriever = HybridRetriever(db)
        self.generator = CopilotGenerator()

    def query(self, request: CopilotQueryRequest) -> dict:
        start_time = time.time()
        
        # 1. Retrieve
        retrieval_start = time.time()
        context = self.retriever.retrieve_context(request.question)
        retrieval_time = time.time() - retrieval_start
        
        # 2. Format Context
        merged_graph = ""
        for subgraph in context["graph_subgraphs"]:
            merged_graph += format_graph_context(subgraph) + "\n"
            
        merged_semantic = format_semantic_context(context["semantic_chunks"])
        
        # 3. Calculate Base Confidence
        base_confidence = self.generator.calculate_confidence(
            context["graph_subgraphs"], 
            context["semantic_chunks"]
        )
        
        # 4. Generate
        gen_start = time.time()
        try:
            answer_obj: CopilotResponse = self.generator.generate_answer(
                question=request.question,
                formatted_graph=merged_graph,
                formatted_semantic=merged_semantic,
                confidence_score=base_confidence
            )
        except Exception as e:
            logger.error(f"Failed to generate copilot response: {e}")
            raise HTTPException(status_code=500, detail="AI generation failed.")
        gen_time = time.time() - gen_start
        
        total_time = time.time() - start_time
        
        # 5. Save History
        history_item = CopilotHistory(
            question=request.question,
            answer=answer_obj.answer,
            confidence=answer_obj.confidence
        )
        self.db.add(history_item)
        self.db.commit()
        
        logger.info(f"Copilot Query Complete. Total: {total_time:.2f}s (Retrieve: {retrieval_time:.2f}s, Generate: {gen_time:.2f}s)")
        
        return {
            "answer": answer_obj.answer,
            "confidence": answer_obj.confidence,
            "citations": [c.model_dump() for c in answer_obj.citations],
            "related_assets": answer_obj.related_assets,
            "reasoning_steps": answer_obj.reasoning_steps,
            "stats": {
                "total_time_sec": round(total_time, 2),
                "retrieval_time_sec": round(retrieval_time, 2),
                "generation_time_sec": round(gen_time, 2)
            }
        }
        
    def get_history(self) -> list:
        items = self.db.query(CopilotHistory).order_by(CopilotHistory.created_at.desc()).limit(50).all()
        return [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "confidence": item.confidence,
                "created_at": item.created_at.isoformat()
            } for item in items
        ]
