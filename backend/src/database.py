from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_db")

# Engine configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Maintain 5 connections
    max_overflow=10,       # Allow 10 additional connections
    pool_pre_ping=True,    # Verify connections before use
    pool_recycle=3600,     # Recycle connections after 1 hour
    echo=False             # Set True for SQL logging (debugging)
)


def init_db():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for database session"""
    with Session(engine) as session:
        yield session