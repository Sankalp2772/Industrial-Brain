import re

def normalize_entity_id(entity_id: str) -> str:
    """
    Normalizes a node ID to ensure it is clean and consistently formatted.
    Removes leading/trailing whitespaces and standardizes internal spaces.
    """
    if not entity_id:
        return ""
    # Trim and normalize internal spaces
    clean = re.sub(r'\s+', ' ', str(entity_id)).strip()
    return clean

def normalize_property(value: str) -> str:
    """
    Normalizes string properties.
    """
    if not isinstance(value, str):
        return value
    return value.strip()
