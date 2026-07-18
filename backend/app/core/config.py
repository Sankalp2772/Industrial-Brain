import os
import itertools
import logging
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


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
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100 MB

    # AI Config — loaded from environment variables only (never hardcoded)
    GEMINI_API_KEY_1: str = ""
    GEMINI_API_KEY_2: str = ""
    GEMINI_API_KEY_3: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Graph Config
    NEO4J_URI: str = "neo4j+s://your-instance.databases.neo4j.io"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    # Auth Config
    SECRET_KEY: str = "CHANGE_THIS_TO_A_STRONG_RANDOM_SECRET_KEY_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def gemini_api_keys(self) -> list[str]:
        """Returns only non-empty Gemini API keys from environment."""
        keys = [
            self.GEMINI_API_KEY_1,
            self.GEMINI_API_KEY_2,
            self.GEMINI_API_KEY_3,
        ]
        active = [k for k in keys if k.strip()]
        if not active:
            logger.warning(
                "No Gemini API keys configured. "
                "Set GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3 in .env"
            )
        return active or [""]


settings = Settings()

# Setup key rotator using only configured keys
_key_rotator = itertools.cycle(settings.gemini_api_keys)


def get_gemini_key() -> str:
    """Returns the next Gemini API key in rotation."""
    return next(_key_rotator)


# Ensure upload directories exist on startup
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
os.makedirs(settings.KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DIR, exist_ok=True)
