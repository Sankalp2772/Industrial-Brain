from app.modules.maintenance.rules import (
    INCIDENT_PENALTY,
    CRITICAL_INSPECTION_PENALTY,
    OPEN_WORK_ORDER_PENALTY,
    get_risk_classification
)

class RiskEngine:
    def calculate_risk(self, context: dict) -> dict:
        score = 0
        factors = []
        
        incidents = context.get("incidents", [])
        if incidents:
            penalty = len(incidents) * INCIDENT_PENALTY
            score += penalty
            factors.append(f"{len(incidents)} repeated incidents/failures (+{penalty} risk points)")
            
        inspections = context.get("inspections", [])
        critical_inspections = [i for i in inspections if str(i.get("severity", "")).lower() in ["high", "critical"] or "action required" in str(i.get("status", "")).lower()]
        if critical_inspections:
            penalty = len(critical_inspections) * CRITICAL_INSPECTION_PENALTY
            score += penalty
            factors.append(f"{len(critical_inspections)} critical inspection findings (+{penalty} risk points)")
            
        work_orders = context.get("work_orders", [])
        open_wo = [w for w in work_orders if str(w.get("status", "")).lower() in ["open", "pending", "in progress"]]
        if open_wo:
            penalty = len(open_wo) * OPEN_WORK_ORDER_PENALTY
            score += penalty
            factors.append(f"{len(open_wo)} skipped/open work orders (+{penalty} risk points)")
            
        if score == 0:
            factors.append("No historical risk factors detected.")
            
        return {
            "risk_score": score,
            "classification": get_risk_classification(score),
            "factors": factors
        }
