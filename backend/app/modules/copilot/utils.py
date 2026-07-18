import re
from typing import List

# Common asset ID aliases to handle natural language references
_KEYWORD_TO_ASSET = {
    "pump p-101": "P-101",
    "pump p101": "P-101",
    "pump 101": "P-101",
    "p-101": "P-101",
    "pump a-42": "A-42",
    "pump a42": "A-42",
    "motor m-22": "M-22",
    "motor m22": "M-22",
    "valve v-505": "V-505",
    "valve v505": "V-505",
    "compressor c-301": "C-301",
}

def detect_assets_in_query(query: str) -> List[str]:
    """
    Detects asset IDs in natural language queries.
    Combines strict regex (P-101) with keyword mapping for natural language
    like 'pump 101', 'pump p101', 'why pump 101 failed'.
    """
    found = set()
    query_lower = query.lower()

    # 1. Regex: match patterns like P-101, M-22, V-505, A-42, C-301
    matches = re.findall(r'\b([A-Za-z])-(\d{2,4})\b', query)
    for letter, number in matches:
        found.add(f"{letter.upper()}-{number}")

    # 2. Keyword mapping for natural language references
    for keyword, asset_id in _KEYWORD_TO_ASSET.items():
        if keyword in query_lower:
            found.add(asset_id)

    return list(found)

