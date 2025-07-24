from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://auditoria:auditoria@localhost/auditoria360_test")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

Base.metadata.create_all(bind=engine)
