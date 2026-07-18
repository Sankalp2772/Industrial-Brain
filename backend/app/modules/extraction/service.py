import os
import time
import json
import logging
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError
from google import genai
from google.genai import types
from app.core.config import settings, get_gemini_key
from app.modules.documents.repository import DocumentRepository
from app.modules.documents.models import Document
from app.modules.extraction.extractor import extract_pdf, extract_docx
from app.modules.extraction.utils import normalize_text
from app.modules.extraction.validator import KnowledgeObject

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractionService:
    def __init__(self, db: Session):
        self.repo = DocumentRepository(db)

    def extract_document(self, doc_id: str) -> dict:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if not os.path.exists(doc.storage_path):
            self.repo.update(doc_id, {"processing_status": "Failed"})
            raise HTTPException(status_code=404, detail="Raw physical file is missing from disk.")

        logger.info(f"Starting extraction for document: {doc_id}")
        start_time = time.time()
        
        # Update status to processing
        self.repo.update(doc_id, {"processing_status": "Processing"})

        try:
            # Route to correct extractor
            if doc.content_type == "application/pdf":
                raw_text, page_count = extract_pdf(doc.storage_path)
            elif doc.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                raw_text, page_count = extract_docx(doc.storage_path)
            else:
                raise HTTPException(status_code=400, detail="Unsupported document type for extraction.")
                
            # Normalize text
            clean_text = normalize_text(raw_text)
            
            # Save to processed directory
            processed_path = os.path.join(settings.PROCESSED_DIR, f"{doc_id}.txt")
            with open(processed_path, "w", encoding="utf-8") as f:
                f.write(clean_text)
                
            # Update Database
            self.repo.update(doc_id, {
                "page_count": page_count,
                "text_extracted": 1,
                "processing_status": "Completed"
            })
            
            duration = time.time() - start_time
            logger.info(f"Extraction complete for {doc_id}. Time taken: {duration:.2f}s. Pages: {page_count}")
            
            return {
                "document_id": doc_id,
                "page_count": page_count,
                "processing_status": "Completed"
            }
            
        except Exception as e:
            self.repo.update(doc_id, {"processing_status": "Failed"})
            logger.error(f"Extraction failed for {doc_id}: {str(e)}")
            raise e

    def get_extracted_text(self, doc_id: str, preview: bool = False) -> str:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if not doc.text_extracted:
            raise HTTPException(status_code=400, detail="Document text has not been extracted yet.")
            
        processed_path = os.path.join(settings.PROCESSED_DIR, f"{doc_id}.txt")
        if not os.path.exists(processed_path):
            raise HTTPException(status_code=404, detail="Processed text file is missing from disk.")
            
        with open(processed_path, "r", encoding="utf-8") as f:
            if preview:
                return f.read(1000)
            return f.read()

    def generate_knowledge_object(self, doc_id: str) -> dict:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if not doc.text_extracted:
            raise HTTPException(status_code=400, detail="Cannot generate knowledge. Text has not been extracted yet.")
            
        processed_path = os.path.join(settings.PROCESSED_DIR, f"{doc_id}.txt")
        if not os.path.exists(processed_path):
            raise HTTPException(status_code=404, detail="Extracted text file is missing from disk.")
            
        with open(processed_path, "r", encoding="utf-8") as f:
            document_text = f.read()
            
        if not document_text.strip():
            raise HTTPException(status_code=400, detail="Document text is empty. Cannot extract knowledge.")

        logger.info(f"Starting Knowledge Generation for document: {doc_id}")
        start_time = time.time()
        
        # Update status to processing
        self.repo.update(doc_id, {"knowledge_status": "Processing"})

        try:
            client = genai.Client(api_key=get_gemini_key())
            
            prompt = f"""
You are an expert industrial knowledge extraction AI.
Analyze the following document and extract a structured knowledge graph according to the defined ontology.
Only extract explicitly stated information. Do not hallucinate.

You MUST return your response as a valid JSON object matching this structure EXACTLY:
{{
  "document": {{"id": "{doc_id}", "type": "Document Type"}},
  "assets": [{{"id": "Asset ID", "name": "Asset Name", "type": "Asset Type"}}],
  "engineers": [{{"id": "Engineer ID", "name": "Name", "department": "Optional Dept"}}],
  "maintenance_actions": [{{"id": "Action ID", "action_taken": "Description", "date": "YYYY-MM-DD"}}],
  "inspection_findings": [{{"id": "Finding ID", "finding": "Description", "severity": "High/Low"}}],
  "incidents": [{{"id": "Incident ID", "description": "Description", "date": "YYYY-MM-DD"}}],
  "relationships": [
    {{
      "source_id": "ID", 
      "source_type": "Asset|Document|Engineer|Inspection|Incident|MaintenanceLog|SOP|WorkOrder|OEMManual|Department",
      "target_id": "ID",
      "target_type": "Asset|Document|Engineer|Inspection|Incident|MaintenanceLog|SOP|WorkOrder|OEMManual|Department",
      "relationship_type": "CONNECTED_TO|MAINTAINED_BY|REFERENCED_IN|MENTIONS|FOLLOWS_SOP|CAUSED|FOUND_IN|FIXES"
    }}
  ]
}}

Document Text:
{document_text}
            """
            
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0
                ),
            )
            
            raw_response_text = response.text
            
            # Clean up markdown code blocks if present
            raw_response_text = raw_response_text.strip()
            if raw_response_text.startswith("```json"):
                raw_response_text = raw_response_text[7:]
            elif raw_response_text.startswith("```"):
                raw_response_text = raw_response_text[3:]
            if raw_response_text.endswith("```"):
                raw_response_text = raw_response_text[:-3]
            raw_response_text = raw_response_text.strip()

            
            # Save raw output for debugging
            raw_path = os.path.join(settings.KNOWLEDGE_DIR, f"{doc_id}_raw.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(raw_response_text)
                
            # Validate JSON string against Pydantic schema
            try:
                parsed_json = json.loads(raw_response_text)
                validated_obj = KnowledgeObject(**parsed_json)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Gemini returned invalid JSON.")
            except ValidationError as ve:
                logger.error(f"Validation failed for {doc_id}: {ve.errors()}")
                raise HTTPException(status_code=500, detail="Gemini output failed ontology validation.")

            # Save validated JSON to disk
            knowledge_path = os.path.join(settings.KNOWLEDGE_DIR, f"{doc_id}.json")
            with open(knowledge_path, "w", encoding="utf-8") as f:
                f.write(validated_obj.model_dump_json(indent=2))
                
            timestamp = datetime.now(timezone.utc)
            # Update Database
            self.repo.update(doc_id, {
                "knowledge_status": "Completed",
                "knowledge_generated_at": timestamp
            })
            
            duration = time.time() - start_time
            prompt_tokens = getattr(response.usage_metadata, 'prompt_token_count', 'N/A')
            completion_tokens = getattr(response.usage_metadata, 'candidates_token_count', 'N/A')
            
            logger.info(f"Knowledge generation complete for {doc_id}. Time taken: {duration:.2f}s. Prompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}")
            
            return {
                "document_id": doc_id,
                "knowledge_status": "Completed",
                "knowledge_generated_at": timestamp.isoformat()
            }
            
        except Exception as e:
            self.repo.update(doc_id, {"knowledge_status": "Failed"})
            logger.error(f"Knowledge generation failed for {doc_id}: {str(e)}")
            raise e

    def get_knowledge_object(self, doc_id: str) -> dict:
        doc = self.repo.get_by_id(doc_id)
        if not doc or doc.knowledge_status != "Completed":
            raise HTTPException(status_code=404, detail="Knowledge Object not found or not yet generated.")
            
        knowledge_path = os.path.join(settings.KNOWLEDGE_DIR, f"{doc_id}.json")
        if not os.path.exists(knowledge_path):
            raise HTTPException(status_code=404, detail="Knowledge Object JSON file is missing from disk.")
            
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def get_raw_knowledge(self, doc_id: str) -> str:
        doc = self.repo.get_by_id(doc_id)
        if not doc or doc.knowledge_status != "Completed":
            raise HTTPException(status_code=404, detail="Raw Knowledge output not found.")
            
        raw_path = os.path.join(settings.KNOWLEDGE_DIR, f"{doc_id}_raw.txt")
        if not os.path.exists(raw_path):
            raise HTTPException(status_code=404, detail="Raw Knowledge text file is missing from disk.")
            
        with open(raw_path, "r", encoding="utf-8") as f:
            return f.read()
