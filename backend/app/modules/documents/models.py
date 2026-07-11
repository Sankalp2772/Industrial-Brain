import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime
from app.database.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, unique=True, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=False)
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="Uploaded")
    processing_status = Column(String, default="Pending")
    storage_path = Column(String, nullable=False)
    
    # Sprint 2 Extraction Fields
    page_count = Column(Integer, default=0)
    text_extracted = Column(Integer, default=0) # SQLite doesn't natively support boolean in some drivers, but Integer 0/1 works perfectly for boolean logic
    
    # Sprint 3 Knowledge Fields
    knowledge_status = Column(String, default="Pending")
    knowledge_generated_at = Column(DateTime, nullable=True)
    
    # Sprint 4 Graph Fields
    graph_status = Column(String, default="Pending")
    graph_synced_at = Column(DateTime, nullable=True)
    
    # Sprint 5 Embedding Fields
    embedding_status = Column(String, default="Pending")
    embedded_at = Column(DateTime, nullable=True)
    chunk_count = Column(Integer, default=0)
