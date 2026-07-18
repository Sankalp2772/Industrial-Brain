from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from app.modules.documents.router import router as documents_router
from app.modules.extraction.router import router as extraction_router
from app.modules.graph.router import router as graph_router
from app.modules.embeddings.router import router as embeddings_router
from app.modules.copilot.router import router as copilot_router
from app.modules.assets.router import router as assets_router
from app.modules.maintenance.router import router as maintenance_router
from app.modules.analytics.router import router as analytics_router
from app.modules.system.router import router as system_router
from app.shared.responses import ErrorResponse
from app.modules.auth.models import User  # Must be imported before create_all so the users table is registered
import time
import logging

logger = logging.getLogger("api_latency")
logger.setLevel(logging.INFO)
Base.metadata.create_all(bind=engine)  # Creates all tables including users

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for Industrial Brain - Industrial Knowledge Intelligence Platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response

# Health endpoint
@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

@app.get("/", tags=["system"])
def root_check():
    return {"success": True, "message": "Industrial Brain API is running. Go to /docs for Swagger UI.", "data": None}

@app.get(settings.API_V1_STR, tags=["system"])
def api_v1_check():
    return {"success": True, "message": "Industrial Brain API v1 is running.", "data": None}

# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(success=False, message="Validation Error", data=exc.errors()).model_dump()
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(success=False, message=str(exc.detail)).model_dump()
    )

from fastapi import Depends
from app.modules.auth.router import router as auth_router
from app.modules.auth.dependencies import get_current_active_user  # noqa: E402

# Include Auth Router (Public)
app.include_router(auth_router, prefix=settings.API_V1_STR)

# Define protected dependencies
protected = [Depends(get_current_active_user)]

# Include Protected Routers
app.include_router(documents_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(extraction_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(graph_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(embeddings_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(copilot_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(assets_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(maintenance_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(analytics_router, prefix=settings.API_V1_STR, dependencies=protected)
app.include_router(system_router, prefix=settings.API_V1_STR, dependencies=protected)

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Override the HTTPValidationError schema globally
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        if "HTTPValidationError" in openapi_schema["components"]["schemas"]:
            openapi_schema["components"]["schemas"]["HTTPValidationError"] = {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "default": False},
                    "message": {"type": "string", "default": "Validation Error"},
                    "data": {
                        "type": "array",
                        "items": {"type": "object"}
                    }
                }
            }
            
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)