"""Database engine, session management, and initialization."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
    pool_pre_ping=True,  # Verify connection before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_session() -> Session:
    """Dependency to get database session for API routes.

    Yields:
        Session: SQLAlchemy session object.
    """
    with SessionLocal() as session:
        yield session


def create_db_and_tables() -> None:
    """Create all database tables from SQLModel definitions.

    Should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)
