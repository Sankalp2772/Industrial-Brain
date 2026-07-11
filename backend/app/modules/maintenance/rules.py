# Risk scoring constants
INCIDENT_PENALTY = 25
CRITICAL_INSPECTION_PENALTY = 15
OPEN_WORK_ORDER_PENALTY = 10

# Risk Classifications
RISK_CLASSIFICATIONS = {
    "LOW": {"min": 0, "max": 20, "label": "Low"},
    "MEDIUM": {"min": 21, "max": 50, "label": "Medium"},
    "HIGH": {"min": 51, "max": 80, "label": "High"},
    "CRITICAL": {"min": 81, "max": 9999, "label": "Critical"}
}

def get_risk_classification(score: int) -> str:
    for cls in RISK_CLASSIFICATIONS.values():
        if cls["min"] <= score <= cls["max"]:
            return cls["label"]
    return "Critical"
