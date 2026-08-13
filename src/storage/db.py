import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.storage.models import Base

# Default to SQLite for local testing if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Creates all tables in the database engine based on the SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """
    Generator that yields a database session and ensures it is safely closed
    after use. Useful for context managers or dependency injection.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
