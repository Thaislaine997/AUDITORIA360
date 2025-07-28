"""
Portal Demandas Database Configuration
SQLAlchemy models and database connection for the demands portal module
Integrated with Neon PostgreSQL serverless database
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging

logger = logging.getLogger(__name__)

# Database URL configuration with fallback
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL")
if not DATABASE_URL:
    # Fallback to SQLite for development
    DATABASE_URL = "sqlite:///./portal_demandas.db"
    logger.warning("Using SQLite fallback for portal_demandas")

# Create engine optimized for Neon PostgreSQL serverless
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        poolclass=StaticPool,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "sslmode": "require",
            "connect_timeout": 10,
        },
        echo=False
    )
else:
    # SQLite configuration for development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for portal_demandas models
Base = declarative_base()

class TicketDB(Base):
    """
    Ticket model for the demands portal
    Represents a work ticket/task in the system
    """
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(200), nullable=False, index=True)
    descricao = Column(Text)
    etapa = Column(String(50), nullable=False, index=True)
    prazo = Column(DateTime, nullable=False)
    responsavel = Column(String(100), nullable=False, index=True)
    status = Column(String(20), default="pendente", nullable=False, index=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Additional fields for better tracking
    prioridade = Column(String(10), default="media")  # baixa, media, alta, critica
    categoria = Column(String(50), default="geral")
    tags = Column(String(200))  # Comma-separated tags
    arquivo_anexo = Column(String(500))  # Path to attached file
    comentarios_internos = Column(Text)
    tempo_estimado = Column(Integer)  # Estimated time in hours
    tempo_gasto = Column(Integer, default=0)  # Time spent in hours
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, titulo='{self.titulo}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'etapa': self.etapa,
            'prazo': self.prazo.isoformat() if self.prazo else None,
            'responsavel': self.responsavel,
            'status': self.status,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
            'prioridade': self.prioridade,
            'categoria': self.categoria,
            'tags': self.tags,
            'arquivo_anexo': self.arquivo_anexo,
            'comentarios_internos': self.comentarios_internos,
            'tempo_estimado': self.tempo_estimado,
            'tempo_gasto': self.tempo_gasto
        }

class TicketComment(Base):
    """
    Comments/history for tickets
    """
    __tablename__ = "ticket_comments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, nullable=False, index=True)  # Foreign key to tickets
    autor = Column(String(100), nullable=False)
    comentario = Column(Text, nullable=False)
    tipo = Column(String(20), default="comentario")  # comentario, status_change, system
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<TicketComment(id={self.id}, ticket_id={self.ticket_id}, autor='{self.autor}')>"

def get_db():
    """
    Database dependency for portal_demandas
    Provides a database session with proper cleanup
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_portal_db():
    """
    Initialize portal_demandas database tables
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Portal demandas database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create portal_demandas tables: {e}")
        return False

def test_db_connection():
    """
    Test database connection
    """
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return result.fetchone()[0] == 1
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

# Create tables on module import if they don't exist
try:
    init_portal_db()
except Exception as e:
    logger.warning(f"Could not initialize portal_demandas tables: {e}")

# Re-export for convenience
__all__ = ['TicketDB', 'TicketComment', 'get_db', 'init_portal_db', 'test_db_connection', 'Base', 'engine', 'SessionLocal']