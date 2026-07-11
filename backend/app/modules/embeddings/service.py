import os
import time
import logging
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.modules.documents.repository import DocumentRepository
from app.modules.embeddings.chunker import chunk_text
from app.modules.embeddings.provider import GeminiEmbeddingProvider
from app.modules.embeddings.repository import chroma_repo
from app.modules.embeddings.utils import extract_knowledge_metadata

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, db: Session):
        self.repo = DocumentRepository(db)
        self.provider = GeminiEmbeddingProvider()

    def generate_embeddings(self, doc_id: str) -> dict:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        if not doc.text_extracted:
            raise HTTPException(status_code=400, detail="Cannot embed document. Text has not been extracted yet.")
            
        processed_path = os.path.join(settings.PROCESSED_DIR, f"{doc_id}.txt")
        if not os.path.exists(processed_path):
            raise HTTPException(status_code=404, detail="Extracted text file is missing.")
            
        with open(processed_path, "r", encoding="utf-8") as f:
            document_text = f.read()

        if not document_text.strip():
            raise HTTPException(status_code=400, detail="Document text is empty.")

        start_time = time.time()
        self.repo.update(doc_id, {"embedding_status": "Processing"})

        try:
            # 1. Chunking
            chunk_start = time.time()
            chunks = chunk_text(document_text, max_chunk_size=1000, overlap=150)
            chunk_time = time.time() - chunk_start
            
            if not chunks:
                raise Exception("Chunking resulted in 0 chunks.")

            # 2. Extract Metadata
            meta_start = time.time()
            doc_meta = extract_knowledge_metadata(doc_id)
            meta_time = time.time() - meta_start

            # Prepare metadata for ChromaDB
            metadatas = []
            for i in range(len(chunks)):
                metadatas.append({
                    "document_id": doc_id,
                    "document_type": doc_meta["document_type"],
                    "asset_ids": doc_meta["asset_ids"],
                    "chunk_index": i,
                    "upload_date": doc.created_at.isoformat() if hasattr(doc, 'created_at') else ""
                })
            ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

            # 3. Generating Embeddings
            embed_start = time.time()
            embeddings = self.provider.embed_texts(chunks)
            embed_time = time.time() - embed_start

            # 4. Storage
            store_start = time.time()
            chroma_repo.add_chunks(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            store_time = time.time() - store_start
            
            total_time = time.time() - start_time
            logger.info(f"Embedding complete for {doc_id}. Total: {total_time:.2f}s (Chunk: {chunk_time:.2f}s, Embed: {embed_time:.2f}s, Store: {store_time:.2f}s)")
            
            timestamp = datetime.now(timezone.utc)
            self.repo.update(doc_id, {
                "embedding_status": "Completed",
                "embedded_at": timestamp,
                "chunk_count": len(chunks)
            })
            
            return {
                "document_id": doc_id,
                "chunk_count": len(chunks),
                "status": "Completed",
                "embedded_at": timestamp.isoformat()
            }
        except Exception as e:
            self.repo.update(doc_id, {"embedding_status": "Failed"})
            logger.error(f"Embedding failed for {doc_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Embedding process failed: {str(e)}")

    def get_document_chunks(self, doc_id: str) -> list:
        doc = self.repo.get_by_id(doc_id)
        if not doc or doc.embedding_status != "Completed":
            raise HTTPException(status_code=404, detail="Embeddings not found or not ready.")
            
        # For simplicity, we can fetch them from Chroma
        # Using a dummy query vector (all zeros) to fetch by filtering metadata
        # However, it's easier to just re-chunk the text or use Chroma's get()
        try:
            results = chroma_repo.collection.get(
                where={"document_id": doc_id},
                include=["documents", "metadatas"]
            )
            return [{"id": id_, "text": doc_, "metadata": meta} for id_, doc_, meta in zip(results['ids'], results['documents'], results['metadatas'])]
        except Exception as e:
            logger.error(f"Failed to fetch chunks: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch chunks from Chroma.")

    def search_semantic(self, query: str, top_k: int = 5) -> list:
        start_time = time.time()
        try:
            query_embedding = self.provider.embed_query(query)
            if not query_embedding:
                raise Exception("Failed to generate embedding for query.")
                
            results = chroma_repo.query_semantic(query_embedding, top_k=top_k)
            
            search_results = []
            if results and results['documents'] and len(results['documents']) > 0:
                docs = results['documents'][0]
                metas = results['metadatas'][0]
                # Chroma uses cosine distance. Score = 1 - distance
                dists = results['distances'][0]
                
                for doc, meta, dist in zip(docs, metas, dists):
                    score = 1.0 - dist
                    search_results.append({
                        "chunk": doc,
                        "score": round(score, 4),
                        "document": meta.get("document_id", ""),
                        "asset": meta.get("asset_ids", "")
                    })
                    
            logger.info(f"Semantic search took {time.time() - start_time:.2f}s")
            return search_results
        except Exception as e:
            logger.error(f"Semantic search failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Semantic search failed.")
