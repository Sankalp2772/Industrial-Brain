import re
from typing import List

def detect_assets_in_query(query: str) -> List[str]:
    """
    Naively detects potential Asset IDs in a query using a regex.
    For Industrial Brain, assume IDs like P-101, M-22, Pump-1, etc.
    """
    # Matches patterns like P-101, M-22, V-505
    matches = re.findall(r'\b[A-Z]-\d{2,4}\b', query.upper())
    # You could expand this list or query Neo4j directly for a fuzzy match if needed
    return list(set(matches))
