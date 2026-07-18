import os
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000/api/v1"
SAMPLE_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample-data"))

def reset_system():
    logger.info("Resetting system databases and files...")
    response = requests.post(f"{API_URL}/system/reset")
    if response.status_code == 200:
        logger.info("System reset successful.")
    else:
        logger.error(f"Failed to reset system: {response.text}")
        exit(1)

def upload_document(filepath):
    logger.info(f"Uploading {os.path.basename(filepath)}...")
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f, 'application/pdf')}
        response = requests.post(f"{API_URL}/documents/upload", files=files)
        
    if response.status_code == 200:
        doc_id = response.json()["data"]["id"]
        logger.info(f"Uploaded successfully. ID: {doc_id}")
        return doc_id
    else:
        logger.error(f"Upload failed: {response.text}")
        return None

def process_document(doc_id):
    # Extraction
    logger.info(f"Extracting text for {doc_id}...")
    requests.post(f"{API_URL}/extraction/document/{doc_id}/extract")
    
    # Knowledge Generation
    logger.info(f"Generating knowledge graph for {doc_id}...")
    requests.post(f"{API_URL}/extraction/document/{doc_id}/knowledge")
    
    # Graph Build
    logger.info(f"Building Neo4j graph for {doc_id}...")
    requests.post(f"{API_URL}/graph/documents/{doc_id}/graph")
    
    # Embeddings
    logger.info(f"Generating vector embeddings for {doc_id}...")
    requests.post(f"{API_URL}/embeddings/documents/{doc_id}/embeddings")
    
    logger.info(f"Finished processing {doc_id}")

def run():
    reset_system()
    
    if not os.path.exists(SAMPLE_DATA_DIR):
        logger.error(f"Sample data directory not found at {SAMPLE_DATA_DIR}")
        return
        
    for filename in os.listdir(SAMPLE_DATA_DIR):
        if filename.endswith(".pdf") or filename.endswith(".docx"):
            filepath = os.path.join(SAMPLE_DATA_DIR, filename)
            doc_id = upload_document(filepath)
            if doc_id:
                process_document(doc_id)
                time.sleep(2)  # Give APIs a breathing room
                
    logger.info("Demo environment is now fully seeded and ready!")

if __name__ == "__main__":
    run()
