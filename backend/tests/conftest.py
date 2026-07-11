import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

os.environ["SQLITE_URL"] = "sqlite:///./test_industrial_brain.db"
os.environ["UPLOAD_DIR"] = "./test_uploads"
os.environ["PROCESSED_DIR"] = "./test_processed"
os.environ["KNOWLEDGE_DIR"] = "./test_knowledge"

from app.main import app
from app.core.dependencies import get_db
from app.database.base import Base

engine = create_engine(os.environ["SQLITE_URL"], connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Setup test directories
    for d in ["./test_uploads", "./test_processed", "./test_knowledge"]:
        os.makedirs(d, exist_ok=True)
    with TestClient(app) as c:
        yield c
    # Teardown logic can be added here
