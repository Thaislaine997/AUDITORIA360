# Import only essential components from main database module to avoid duplication
# while keeping portal_demandas isolated from complex model relationships
from src.models.database import engine, SessionLocal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

# Create isolated Base for portal_demandas to avoid model conflicts
Base = declarative_base()

class TicketDB(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String)
    etapa = Column(String)
    prazo = Column(DateTime)
    responsavel = Column(String)
    status = Column(String, default="pendente")
    criado_em = Column(DateTime)
    atualizado_em = Column(DateTime)

def get_db():
    """Database dependency for portal_demandas using shared connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Re-export for convenience
__all__ = ['TicketDB', 'get_db']