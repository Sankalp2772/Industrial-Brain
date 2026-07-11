import os
import json
import logging
from fastapi import HTTPException
from app.core.config import settings
from app.modules.maintenance.utils import fetch_asset_context
from app.modules.maintenance.risk import RiskEngine
from app.modules.maintenance.rca import RCAGenerator
from app.modules.maintenance.recommendation_engine import RecommendationEngine

logger = logging.getLogger(__name__)

class MaintenanceService:
    def __init__(self):
        self.risk_engine = RiskEngine()
        self.rca_generator = RCAGenerator()
        self.rec_engine = RecommendationEngine()
        
    def _get_analysis_path(self, asset_id: str) -> str:
        # We store analysis JSON files in the processed dir for persistence
        return os.path.join(settings.PROCESSED_DIR, f"maintenance_analysis_{asset_id}.json")

    def analyze_asset(self, asset_id: str) -> dict:
        context = fetch_asset_context(asset_id)
        
        # 1. Risk Score
        risk_data = self.risk_engine.calculate_risk(context)
        
        # 2. RCA
        rca_data = self.rca_generator.generate_rca(context)
        
        # 3. Recommendations
        recommendations = self.rec_engine.generate_recommendations(context, rca_data)
        
        # Assemble payload
        analysis = {
            "risk_score": risk_data["risk_score"],
            "classification": risk_data["classification"],
            "factors": risk_data["factors"],
            "root_causes": rca_data.get("root_causes", []),
            "confidence": rca_data.get("confidence", "Low"),
            "recommendations": recommendations,
            # We aggregate evidence from RCA and Recs for the top-level
            "evidence": [] 
        }
        
        # Aggregate all evidence
        evidence_set = set()
        for rca in analysis["root_causes"]:
            for e in rca.get("evidence", []):
                evidence_set.add(e)
        for rec in analysis["recommendations"]:
            for e in rec.get("evidence", []):
                evidence_set.add(e)
                
        analysis["evidence"] = list(evidence_set)
        
        # Derive highest priority from recommendations
        priorities = [r.get("priority", "Low").upper() for r in analysis["recommendations"]]
        if "CRITICAL" in priorities:
            analysis["priority"] = "Critical"
        elif "HIGH" in priorities:
            analysis["priority"] = "High"
        elif "MEDIUM" in priorities:
            analysis["priority"] = "Medium"
        else:
            analysis["priority"] = "Low"
            
        # Persist to disk
        path = self._get_analysis_path(asset_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)
            
        return analysis

    def get_analysis(self, asset_id: str) -> dict:
        path = self._get_analysis_path(asset_id)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Analysis not found. Run POST /maintenance/analyze/{asset_id} first.")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_risk(self, asset_id: str) -> dict:
        try:
            analysis = self.get_analysis(asset_id)
            return {
                "risk_score": analysis["risk_score"],
                "classification": analysis["classification"],
                "factors": analysis.get("factors", [])
            }
        except HTTPException:
            # Calculate dynamically if not persisted
            context = fetch_asset_context(asset_id)
            return self.risk_engine.calculate_risk(context)

    def get_rca(self, asset_id: str) -> dict:
        analysis = self.get_analysis(asset_id)
        return {
            "root_causes": analysis.get("root_causes", []),
            "confidence": analysis.get("confidence", "Low")
        }

    def get_recommendations(self, asset_id: str) -> dict:
        analysis = self.get_analysis(asset_id)
        return {
            "recommendations": analysis.get("recommendations", [])
        }
