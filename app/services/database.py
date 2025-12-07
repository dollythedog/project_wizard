"""
Database utilities for Project Wizard v3.0.

Handles SQLite connection, session management, and database initialization.
"""

from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from typing import Generator

# Database location
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_PATH = DB_DIR / "project_wizard.db"
DB_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})


def init_database() -> None:
    """
    Initialize the database by creating all tables.
    
    Safe to call multiple times - only creates tables if they don't exist.
    """
    # Ensure data directory exists
    DB_DIR.mkdir(exist_ok=True)
    
    # Import all models to register them with SQLModel
    from app.models.database import (
        Project, 
        ProjectNote, 
        SupportingFile, 
        DocumentRun, 
        MemoryEntry
    )
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    print(f"Database initialized at {DB_PATH}")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Usage:
        with get_session() as session:
            project = session.get(Project, 1)
            ...
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection in FastAPI.
    
    Usage in FastAPI route:
        @app.get("/projects")
        def list_projects(session: Session = Depends(get_db_session)):
            ...
    """
    with get_session() as session:
        yield session

def get_engine():
    """
    Get the database engine.
    """
    return engine
