import json
import time
import logging
from google import genai
from google.genai import types
from google.genai import errors as genai_errors
from app.core.config import settings, get_gemini_key
from app.modules.copilot.schema import CopilotResponse

logger = logging.getLogger(__name__)

# The correct working model name to use
GEMINI_MODEL = "gemini-2.0-flash"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds between retries


class CopilotGenerator:
    def __init__(self):
        # Client will be recreated with key rotation on each call to handle 429s
        self._current_key = get_gemini_key()
        self.client = genai.Client(api_key=self._current_key)

    def _rotate_client(self):
        """Rotate to the next API key on quota exhaustion."""
        self._current_key = get_gemini_key()
        self.client = genai.Client(api_key=self._current_key)

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

    def _call_gemini_with_retry(self, prompt: str, question: str) -> str:
        """Call Gemini with automatic key rotation and retry on 429/503."""
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=[
                        types.Content(role="user", parts=[
                            types.Part.from_text(text=prompt),
                            types.Part.from_text(text=f"Question: {question}")
                        ])
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.0
                    ),
                )
                return response.text

            except genai_errors.ClientError as e:
                # 429 quota exhausted — rotate key and retry
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    logger.warning(f"Gemini 429 on attempt {attempt + 1}, rotating key...")
                    self._rotate_client()
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    last_error = e
                else:
                    raise e

            except genai_errors.ServerError as e:
                # 503 transient server error — retry
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    logger.warning(f"Gemini 503 on attempt {attempt + 1}, retrying...")
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    last_error = e
                else:
                    raise e

            except Exception as e:
                raise e

        raise Exception(f"Gemini failed after {MAX_RETRIES} retries: {last_error}")

    def generate_answer(self, question: str, formatted_graph: str, formatted_semantic: str, confidence_score: float) -> CopilotResponse:
        system_prompt = f"""
You are the Industrial Brain AI Copilot. You are an expert in industrial maintenance, failure analysis, and operations.
Your ONLY sources of knowledge are the provided GRAPH KNOWLEDGE and DOCUMENTATION EVIDENCE.
Do not use outside knowledge. Do not hallucinate.
If the provided context does not contain the answer, you MUST state: "No supporting evidence was found in the uploaded documents."

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
            raw_text = self._call_gemini_with_retry(system_prompt, question)

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

            # Blend LLM confidence with retrieval confidence
            if confidence_score == 0.0:
                validated_obj.confidence = 0.0
            else:
                validated_obj.confidence = round((validated_obj.confidence + confidence_score) / 2.0, 2)

            return validated_obj

        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise e

    def generate_text(self, prompt: str) -> str:
        """Simple text generation with retry — for non-copilot uses (e.g. asset summary)."""
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                )
                return response.text
            except (genai_errors.ClientError, genai_errors.ServerError) as e:
                err_str = str(e)
                if "429" in err_str or "503" in err_str or "RESOURCE_EXHAUSTED" in err_str or "UNAVAILABLE" in err_str:
                    logger.warning(f"Gemini transient error attempt {attempt + 1}: {err_str[:60]}")
                    self._rotate_client()
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    last_error = e
                else:
                    raise e
        raise Exception(f"Gemini text generation failed after {MAX_RETRIES} retries: {last_error}")
