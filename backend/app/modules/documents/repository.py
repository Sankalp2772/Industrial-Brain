from sqlalchemy.orm import Session
from app.modules.documents.models import Document
from typing import List, Optional

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, doc_data: dict) -> Document:
        db_doc = Document(**doc_data)
        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)
        return db_doc

    def get_by_id(self, doc_id: str) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == doc_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Document]:
        return self.db.query(Document).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Document).count()

    def delete(self, doc_id: str) -> bool:
        db_doc = self.get_by_id(doc_id)
        if db_doc:
            self.db.delete(db_doc)
            self.db.commit()
            return True
        return False

    def update(self, doc_id: str, update_data: dict) -> Optional[Document]:
        db_doc = self.get_by_id(doc_id)
        if db_doc:
            for key, value in update_data.items():
                setattr(db_doc, key, value)
            self.db.commit()
            self.db.refresh(db_doc)
            return db_doc
        return None
