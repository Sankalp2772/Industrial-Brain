import re
from typing import List, Dict, Any

def chunk_text(text: str, max_chunk_size: int = 1000, overlap: int = 150) -> List[Dict[str, Any]]:
    """
    Splits text into chunks of approximately max_chunk_size characters using semantic boundaries.
    Returns a list of dicts containing text and metadata.
    """
    chunks = []
    
    # Semantic split by markdown headings or double newlines
    blocks = re.split(r'\n\s*\n', text)
    
    current_chunk = ""
    current_heading = ""
    current_section = ""
    paragraph_index = 0
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Detect headings
        heading_match = re.match(r'^(#+)\s+(.*)', block)
        if heading_match:
            level = len(heading_match.group(1))
            current_heading = heading_match.group(2).strip()
            if level == 1 or level == 2:
                current_section = current_heading
                
        # Handle huge single blocks
        if len(block) > max_chunk_size:
            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "heading": current_heading,
                    "section": current_section,
                    "paragraph_index": paragraph_index
                })
                paragraph_index += 1
                current_chunk = ""
            
            # Brute force split with overlap
            start = 0
            while start < len(block):
                end = min(start + max_chunk_size, len(block))
                chunk_text_str = block[start:end]
                chunks.append({
                    "text": chunk_text_str.strip(),
                    "heading": current_heading,
                    "section": current_section,
                    "paragraph_index": paragraph_index
                })
                paragraph_index += 1
                start += max_chunk_size - overlap
            continue
            
        # Normal block aggregation
        if len(current_chunk) + len(block) > max_chunk_size and current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "heading": current_heading,
                "section": current_section,
                "paragraph_index": paragraph_index
            })
            paragraph_index += 1
            # Add overlap logic
            current_chunk = current_chunk[-overlap:] + "\n\n" + block
        else:
            if current_chunk:
                current_chunk += "\n\n" + block
            else:
                current_chunk = block
                
    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "heading": current_heading,
            "section": current_section,
            "paragraph_index": paragraph_index
        })
        
    return chunks
