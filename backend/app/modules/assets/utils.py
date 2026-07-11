from datetime import datetime

def parse_date(date_str: str) -> datetime:
    """Attempt to parse various date formats into a datetime object for sorting."""
    if not date_str:
        return datetime.min
    try:
        # Try ISO format
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        try:
            # Try basic YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return datetime.min

def sort_timeline(events: list) -> list:
    """Sorts a list of timeline event dicts chronologically descending."""
    return sorted(
        events, 
        key=lambda x: parse_date(x.get("date", "")), 
        reverse=True
    )
