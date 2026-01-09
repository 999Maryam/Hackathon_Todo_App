from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .database import init_db
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Todo API with Authentication",
    description="API for managing todo tasks with JWT-based authentication and user isolation",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend dev
        "https://your-app.vercel.app"  # Frontend prod
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Skipping database initialization for now...")
    # init_db()
    # logger.info("Database initialized successfully")

# Include routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Todo API with Authentication is running"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {"detail": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)