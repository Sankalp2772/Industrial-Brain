from app.modules.assets.utils import sort_timeline

class AssetAggregator:
    def __init__(self, neighborhood: dict):
        self.neighborhood = neighborhood
        self.asset = neighborhood.get("asset", {})
        self.connected_nodes = neighborhood.get("connected_nodes", [])

    def extract_timeline(self) -> list:
        events = []
        for node in self.connected_nodes:
            labels = node.get("_labels", [])
            
            if "Incident" in labels:
                events.append({
                    "date": node.get("date", ""),
                    "type": "Incident",
                    "description": node.get("description", "Incident occurred"),
                    "source_id": node.get("id", "")
                })
            elif "MaintenanceLog" in labels:
                events.append({
                    "date": node.get("date", ""),
                    "type": "Maintenance",
                    "description": node.get("action", "Maintenance performed"),
                    "source_id": node.get("id", "")
                })
            elif "Inspection" in labels:
                events.append({
                    "date": node.get("date", ""),
                    "type": "Inspection",
                    "description": node.get("finding", "Inspection logged"),
                    "source_id": node.get("id", "")
                })
            elif "WorkOrder" in labels:
                events.append({
                    "date": node.get("date_created", ""),
                    "type": "WorkOrder",
                    "description": node.get("description", "Work order opened"),
                    "source_id": node.get("id", "")
                })
                
        return sort_timeline(events)

    def calculate_health(self) -> dict:
        score = 100
        reasons = []
        
        incidents = [n for n in self.connected_nodes if "Incident" in n.get("_labels", [])]
        inspections = [n for n in self.connected_nodes if "Inspection" in n.get("_labels", [])]
        work_orders = [n for n in self.connected_nodes if "WorkOrder" in n.get("_labels", [])]
        
        # Penalties
        if incidents:
            penalty = len(incidents) * 15
            score -= penalty
            reasons.append(f"Recent incidents detected (-{penalty} points).")
            
        actionable_inspections = [i for i in inspections if str(i.get("severity", "")).lower() in ["high", "critical"] or "action required" in str(i.get("status", "")).lower()]
        if actionable_inspections:
            penalty = len(actionable_inspections) * 10
            score -= penalty
            reasons.append(f"Actionable inspection findings (-{penalty} points).")
            
        open_work_orders = [w for w in work_orders if str(w.get("status", "")).lower() in ["open", "pending", "in progress"]]
        if open_work_orders:
            penalty = len(open_work_orders) * 5
            score -= penalty
            reasons.append(f"Open work orders (-{penalty} points).")
            
        if score == 100:
            reasons.append("Asset is operating optimally with no detected issues.")
            
        score = max(0, min(100, score))
        
        if score >= 80:
            classification = "Healthy"
        elif score >= 50:
            classification = "Warning"
        else:
            classification = "Critical"
            
        return {
            "score": score,
            "classification": classification,
            "reasons": reasons
        }

    def aggregate_counts(self) -> dict:
        counts = {
            "connected_documents": 0,
            "connected_incidents": 0,
            "connected_maintenance": 0,
            "connected_sops": 0
        }
        for node in self.connected_nodes:
            labels = node.get("_labels", [])
            if "Document" in labels:
                counts["connected_documents"] += 1
            elif "Incident" in labels:
                counts["connected_incidents"] += 1
            elif "MaintenanceLog" in labels:
                counts["connected_maintenance"] += 1
            elif "SOP" in labels:
                counts["connected_sops"] += 1
        return counts
