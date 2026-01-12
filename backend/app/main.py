"""FastAPI application factory and setup."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.config import settings
from app.database import create_db_and_tables
from app.models.schemas import ErrorResponse

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up application...")
    create_db_and_tables()
    logger.info("Database tables created/verified")
    yield
    # Shutdown
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    app = FastAPI(
        title="Todo Backend API",
        description="Secure, RESTful API for multi-user task management with JWT authentication",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Frontend dev
            "https://frontend-alpha-two-87.vercel.app",  # Frontend prod (Vercel)
            "https://maryam-qaiser-mytodo-app.hf.space",  # HF Space
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router)

    # Include auth routes
    try:
        from app.api.auth_routes import auth_router
        app.include_router(auth_router)
    except ImportError as e:
        logger.warning(f"Could not import auth routes: {e}")

    # Global exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        """Handle Pydantic validation errors."""
        # Extract first validation error for detail
        errors = exc.errors()
        first_error = errors[0] if errors else {}
        field = first_error.get("loc", ["unknown"])[1] if len(first_error.get("loc", [])) > 1 else "unknown"
        msg = first_error.get("msg", "Validation error")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Validation error",
                "status": status.HTTP_400_BAD_REQUEST,
                "detail": f"{field}: {msg}",
            },
        )

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok"}

    logger.info("Application initialized")
    return app


# Create application instance
app = create_app()
