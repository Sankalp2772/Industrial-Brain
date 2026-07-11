import re
from typing import List

def chunk_text(text: str, max_chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    """
    Splits text into chunks of approximately max_chunk_size characters.
    Attempts to break cleanly on double newlines (paragraphs) when possible.
    """
    # Simple double newline split
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If a single paragraph is too huge, we must brute force split it
        if len(para) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
                
            # Brute force split large paragraph with overlap
            start = 0
            while start < len(para):
                end = min(start + max_chunk_size, len(para))
                
                # If we're not at the very end, try to find a space to break at cleanly
                if end < len(para):
                    last_space = para.rfind(' ', start, end)
                    if last_space > start + (max_chunk_size // 2):
                        end = last_space
                        
                chunks.append(para[start:end].strip())
                start = end - overlap
                if start < 0:
                    start = 0
            continue
            
        # If adding this paragraph exceeds size, save current chunk and start new one
        if len(current_chunk) + len(para) + 2 > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # For overlap across paragraphs, take the last bit of the previous chunk
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            # Find the first space to make the overlap clean
            clean_overlap = overlap_text[overlap_text.find(' ')+1:] if ' ' in overlap_text else overlap_text
            current_chunk = clean_overlap + "\n\n" + para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
                
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks
