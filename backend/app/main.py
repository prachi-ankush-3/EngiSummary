"""
Main Application Module
FastAPI application initialization and configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core import logger, settings
from app.api.routes import upload, processing, status, download


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(
    upload.router,
    prefix="/api",
    tags=["Upload"]
)

app.include_router(
    processing.router,
    prefix="/api",
    tags=["Processing"]
)

app.include_router(
    status.router,
    prefix="/api",
    tags=["Status"]
)

app.include_router(
    download.router,
    prefix="/api",
    tags=["Download"]
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "title": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EngiSummary Backend"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup():
    """Application startup"""
    logger.info("=" * 60)
    logger.info(f"EngiSummary Backend Starting")
    logger.info(f"Version: {settings.API_VERSION}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"Gemini Model: {settings.GEMINI_MODEL}")
    logger.info(f"Frontend URL: {settings.FRONTEND_URL}")
    logger.info("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown():
    """Application shutdown"""
    logger.info("=" * 60)
    logger.info("EngiSummary Backend Shutting Down")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
