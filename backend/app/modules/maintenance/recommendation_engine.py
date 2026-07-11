import json
import logging
from google import genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
    def generate_recommendations(self, context: dict, rca: dict) -> list:
        prompt = f"""
You are an expert Industrial Maintenance Planner.
Based on the following asset data and Root Cause Analysis, generate a list of actionable maintenance recommendations.
DO NOT hallucinate. Recommendations must be grounded in the provided data.

You MUST return your response as a valid JSON object matching this structure EXACTLY:
{{
  "recommendations": [
    {{
      "recommended_action": "Action to take",
      "priority": "Critical|High|Medium|Low",
      "reason": "Why this is recommended",
      "evidence": ["Evidence string 1", "Evidence string 2"],
      "expected_benefit": "Expected outcome"
    }}
  ]
}}

RCA:
{json.dumps(rca, indent=2)}

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
            
            parsed = json.loads(raw_text)
            return parsed.get("recommendations", [])
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return []
