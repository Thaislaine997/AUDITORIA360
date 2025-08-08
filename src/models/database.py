"""
Database configuration and connection for AUDITORIA360
Using Neon PostgreSQL serverless database
"""

import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Database URL for Neon PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auditoria360_dev.db")

# Create engine with proper connection pooling for serverless
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,  # Set to True for SQL debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all models with common functionality
class BaseModel:
    """Base model class with common functionality for all SQLAlchemy models."""

    def __repr__(self):
        """
        Standard representation for all models.
        Uses class name and attempts to find a meaningful identifier.
        """
        class_name = self.__class__.__name__

        # Try common identifier fields in order of preference
        identifier_fields = [
            "name",
            "title",
            "username",
            "email",
            "code",
            "number",
            "id",
        ]
        identifier = None

        for field in identifier_fields:
            if hasattr(self, field):
                value = getattr(self, field)
                if value is not None:
                    identifier = str(value)
                    break

        # If no common identifier found, use id
        if identifier is None and hasattr(self, "id"):
            identifier = f"id={self.id}"

        return f"<{class_name} {identifier or 'Unknown'}>"


# Base class for all models
Base = declarative_base(cls=BaseModel)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
