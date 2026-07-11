import json
import logging
from google import genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class RCAGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
    def generate_rca(self, context: dict) -> dict:
        prompt = f"""
You are an expert Industrial Reliability Engineer.
Analyze the following asset historical data (Incidents, Inspections, Maintenance Logs, Work Orders).
Generate a Root Cause Analysis (RCA) determining the likely causes of any historical failures or degradation.
DO NOT hallucinate. You must explicitly cite evidence from the provided JSON.

You MUST return your response as a valid JSON object matching this structure EXACTLY:
{{
  "root_causes": [
    {{
      "possible_cause": "Description of the cause",
      "confidence": "High|Medium|Low",
      "evidence": ["Evidence string 1", "Evidence string 2"]
    }}
  ],
  "confidence": "High|Medium|Low"
}}

DATA:
{json.dumps(context, indent=2)}
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0
                )
            )
            
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()
            
            return json.loads(raw_text)
        except Exception as e:
            logger.error(f"Failed to generate RCA: {e}")
            return {"root_causes": [], "confidence": "Low"}
