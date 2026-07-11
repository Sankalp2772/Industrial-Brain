import chromadb
from chromadb.config import Settings
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class ChromaRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaRepository, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        try:
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            # Create or get the main collection
            self.collection = self.client.get_or_create_collection(
                name="industrial_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Successfully initialized ChromaDB PersistentClient")
        except Exception as e:
            logger.error(f"ChromaDB initialization failed: {str(e)}")
            self.client = None
            self.collection = None

    def add_chunks(self, ids: list[str], embeddings: list[list[float]], documents: list[str], metadatas: list[dict]):
        if not self.collection:
            raise Exception("ChromaDB collection not available")
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query_semantic(self, query_embedding: list[float], top_k: int = 5):
        if not self.collection:
            raise Exception("ChromaDB collection not available")
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

chroma_repo = ChromaRepository()
