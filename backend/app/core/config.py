import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Industrial Brain API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./industrial_brain.db"
    
    # Uploads
    UPLOAD_DIR: str = "uploads/raw"
    PROCESSED_DIR: str = "uploads/processed"
    KNOWLEDGE_DIR: str = "uploads/knowledge"
    CHROMA_DIR: str = "uploads/chroma"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100 MB limit
    
    # AI Config
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "mock_key_for_now")
    
    # Graph Config
    NEO4J_URI: str = os.getenv("NEO4J_URI", "neo4j+s://placeholder.databases.neo4j.io")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "mock_neo4j_password")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
os.makedirs(settings.KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DIR, exist_ok=True)
