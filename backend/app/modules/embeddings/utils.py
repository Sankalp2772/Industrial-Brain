import json
import os
from app.core.config import settings

def extract_knowledge_metadata(doc_id: str) -> dict:
    """
    Attempts to read the generated Knowledge JSON for a document.
    Extracts asset IDs and document type to inject as metadata into vector chunks.
    """
    knowledge_path = os.path.join(settings.KNOWLEDGE_DIR, f"{doc_id}.json")
    if not os.path.exists(knowledge_path):
        return {"document_type": "Unknown", "asset_ids": ""}
        
    try:
        with open(knowledge_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        doc_type = data.get("document", {}).get("type", "Unknown")
        assets = data.get("assets", [])
        asset_ids = ",".join([a.get("id") for a in assets if "id" in a])
        
        return {
            "document_type": doc_type,
            "asset_ids": asset_ids
        }
    except Exception:
        return {"document_type": "Unknown", "asset_ids": ""}
