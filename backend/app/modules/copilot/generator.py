import json
import logging
from google import genai
from google.genai import types
from pydantic import ValidationError
from app.core.config import settings
from app.modules.copilot.schema import CopilotResponse

logger = logging.getLogger(__name__)

class CopilotGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
    def calculate_confidence(self, graph_subgraphs: list, semantic_chunks: list) -> float:
        has_graph = len(graph_subgraphs) > 0
        has_semantic = len(semantic_chunks) > 0
        
        if has_graph and len(semantic_chunks) > 2:
            return 0.95
        elif has_graph and has_semantic:
            return 0.85
        elif has_graph or len(semantic_chunks) > 1:
            return 0.65
        elif has_semantic:
            return 0.45
        return 0.0

    def generate_answer(self, question: str, formatted_graph: str, formatted_semantic: str, confidence_score: float) -> CopilotResponse:
        system_prompt = f"""
You are the Industrial Brain AI Copilot. You are an expert in industrial maintenance, failure analysis, and operations.
Your ONLY sources of knowledge are the provided GRAPH KNOWLEDGE and DOCUMENTATION EVIDENCE.
Do not use outside knowledge. Do not hallucinate.
If the provided context does not contain the answer, you MUST state: "No supporting evidence was found."

You MUST return your response as a valid JSON object with the following exact structure:
{{
  "answer": "The generated answer string",
  "confidence": 0.95,
  "citations": [
    {{"document": "doc_id", "asset": "asset_id", "chunk": "text snippet", "page": 1}}
  ],
  "related_assets": ["list", "of", "asset", "ids"],
  "reasoning_steps": ["step 1", "step 2"]
}}

{formatted_graph}

{formatted_semantic}
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-3.5-flash',
                contents=[
                    types.Content(role="user", parts=[
                        types.Part.from_text(text=system_prompt),
                        types.Part.from_text(text=f"Question: {question}")
                    ])
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0
                ),
            )
            
            raw_text = response.text
            
            # Clean up markdown code blocks if present
            raw_text = raw_text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()
            
            parsed_json = json.loads(raw_text)
            validated_obj = CopilotResponse(**parsed_json)
            
            # Override confidence with our rule-based score if it's high
            # We can trust the LLM's confidence if we want, but we should cap it based on retrieval success
            if confidence_score == 0.0:
                validated_obj.confidence = 0.0
            else:
                # Average LLM confidence with our retrieval confidence
                validated_obj.confidence = round((validated_obj.confidence + confidence_score) / 2.0, 2)
                
            return validated_obj

        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise e
