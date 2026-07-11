import json
import logging
from google import genai
from fastapi import HTTPException
from app.core.config import settings
from app.modules.assets.repository import AssetRepository
from app.modules.assets.aggregator import AssetAggregator

logger = logging.getLogger(__name__)

class AssetService:
    def __init__(self):
        self.repo = AssetRepository()
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
    def get_all_assets(self) -> list:
        return self.repo.get_all_assets()

    def get_asset_profile(self, asset_id: str) -> dict:
        neighborhood = self.repo.get_asset_neighborhood(asset_id)
        if not neighborhood or not neighborhood.get("asset"):
            raise HTTPException(status_code=404, detail="Asset not found in graph database.")
            
        agg = AssetAggregator(neighborhood)
        health = agg.calculate_health()
        counts = agg.aggregate_counts()
        
        asset_props = neighborhood["asset"]
        asset_type = asset_props.pop("type", "Unknown")
        
        return {
            "asset_id": asset_id,
            "type": asset_type,
            "properties": asset_props,
            "health": health,
            **counts
        }

    def get_asset_timeline(self, asset_id: str) -> list:
        neighborhood = self.repo.get_asset_neighborhood(asset_id)
        if not neighborhood or not neighborhood.get("asset"):
            raise HTTPException(status_code=404, detail="Asset not found.")
            
        agg = AssetAggregator(neighborhood)
        return agg.extract_timeline()

    def get_asset_documents(self, asset_id: str) -> list:
        neighborhood = self.repo.get_asset_neighborhood(asset_id)
        docs = []
        for node in neighborhood.get("connected_nodes", []):
            labels = node.get("_labels", [])
            if "Document" in labels or "SOP" in labels or "OEMManual" in labels:
                docs.append(node)
        return docs

    def get_asset_relationships(self, asset_id: str) -> dict:
        return self.repo.get_asset_neighborhood(asset_id)

    def generate_ai_summary(self, asset_id: str) -> str:
        # Fetch full profile and timeline to feed to Gemini
        try:
            profile = self.get_asset_profile(asset_id)
            timeline = self.get_asset_timeline(asset_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Asset not found.")
            
        # Format payload
        payload = {
            "asset": profile,
            "recent_events": timeline[:10]  # Only need latest 10 events for summary
        }
        
        prompt = f"""
You are an expert Industrial Asset Manager.
Review the following JSON data for Asset {asset_id}.
Write a concise, professional summary of the asset's current health, recent issues, and overall status.
Maximum 200 words.
DO NOT hallucinate external information. Only use the provided JSON.

DATA:
{json.dumps(payload, indent=2)}
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Failed to generate asset summary: {e}")
            raise HTTPException(status_code=500, detail="AI generation failed.")
