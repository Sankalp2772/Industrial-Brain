import os
import psutil
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.core.dependencies import get_db
from app.modules.graph.builder import neo4j_conn
from app.modules.embeddings.repository import chroma_repo
from app.shared.responses import SuccessResponse

router = APIRouter(prefix="/system", tags=["system"])

def get_dir_size(path):
    total_size = 0
    if os.path.exists(path):
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    return total_size

@router.get("/status", summary="Get overall system status")
def get_system_status(db: Session = Depends(get_db)):
    status = {
        "sqlite": "Disconnected",
        "neo4j": "Disconnected",
        "chroma": "Disconnected",
        "gemini": "Configured" if settings.GEMINI_API_KEY else "Missing API Key",
        "disk_usage": {}
    }
    
    # Check SQLite
    try:
        db.execute(text("SELECT 1"))
        status["sqlite"] = "Connected"
    except Exception:
        pass
        
    # Check Neo4j
    try:
        if neo4j_conn.driver:
            with neo4j_conn.driver.session() as session:
                session.run("RETURN 1")
            status["neo4j"] = "Connected"
    except Exception:
        pass
        
    # Check Chroma
    try:
        if chroma_repo.client:
            chroma_repo.client.heartbeat()
            status["chroma"] = "Connected"
    except Exception:
        pass
        
    # Disk Usage
    uploads_size = get_dir_size(settings.UPLOAD_DIR)
    status["disk_usage"] = {
        "uploads_bytes": uploads_size,
        "uploads_mb": round(uploads_size / (1024 * 1024), 2),
        "system_cpu_percent": psutil.cpu_percent(),
        "system_memory_percent": psutil.virtual_memory().percent
    }
    
    return SuccessResponse(message="System status retrieved", data=status)

@router.get("/version", summary="Get API Version")
def get_version():
    return SuccessResponse(message="Version retrieved", data={"version": settings.VERSION, "project": settings.PROJECT_NAME})

@router.get("/readiness", summary="Readiness Probe")
def get_readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        if not neo4j_conn.driver:
            raise Exception("Neo4j driver not initialized")
    except Exception as e:
        return {"status": "error", "message": str(e)}
    return {"status": "ready"}

@router.post("/reset", summary="DANGEROUS: Reset Demo Database")
def reset_system(db: Session = Depends(get_db)):
    # 1. Clear SQLite tables
    try:
        db.execute(text("DELETE FROM documents"))
        db.commit()
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"SQLite reset failed: {e}"}
        
    # 2. Clear Neo4j
    try:
        if neo4j_conn.driver:
            with neo4j_conn.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
    except Exception as e:
        return {"success": False, "message": f"Neo4j reset failed: {e}"}
        
    # 3. Clear ChromaDB
    try:
        if chroma_repo.client:
            try:
                chroma_repo.client.delete_collection("industrial_knowledge")
            except:
                pass
    except Exception as e:
        return {"success": False, "message": f"Chroma reset failed: {e}"}
        
    # 4. Clear physical files
    for directory in [settings.UPLOAD_DIR, settings.PROCESSED_DIR, settings.KNOWLEDGE_DIR]:
        if os.path.exists(directory):
            for f in os.listdir(directory):
                try:
                    os.remove(os.path.join(directory, f))
                except:
                    pass
                    
    return SuccessResponse(message="System successfully reset to factory defaults", data=None)
