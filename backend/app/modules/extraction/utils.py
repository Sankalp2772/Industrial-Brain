import re

def normalize_text(text: str) -> str:
    """
    Normalizes whitespace and cleans extracted text.
    - Replaces multiple newlines with a single newline.
    - Removes trailing/leading whitespace.
    """
    if not text:
        return ""
    
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    
    # Replace 3 or more newlines with exactly 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()
