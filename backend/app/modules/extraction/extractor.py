import fitz  # PyMuPDF
from docx import Document as DocxDocument
from typing import Tuple
from fastapi import HTTPException

def extract_pdf(file_path: str) -> Tuple[str, int]:
    """
    Extracts text from a PDF file using PyMuPDF.
    Returns (extracted_text, page_count).
    """
    text = []
    try:
        doc = fitz.open(file_path)
        
        if doc.is_encrypted:
            raise HTTPException(status_code=422, detail="Cannot extract text from password-protected PDF.")
            
        page_count = doc.page_count
        
        for page_num in range(page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text.append(page_text)
                
        doc.close()
        return "\n\n".join(text), page_count
        
    except fitz.FileDataError:
        raise HTTPException(status_code=422, detail="PDF file is corrupted or unreadable.")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {str(e)}")

def extract_docx(file_path: str) -> Tuple[str, int]:
    """
    Extracts text from a DOCX file using python-docx.
    Returns (extracted_text, page_count). Note: DOCX doesn't have a fixed page count, so we return 1.
    """
    text = []
    try:
        doc = DocxDocument(file_path)
        
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text)
                
        return "\n\n".join(text), 1
        
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"DOCX extraction failed. File may be corrupted: {str(e)}")
