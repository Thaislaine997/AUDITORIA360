"""
Portal Demandas Database Configuration
SQLAlchemy models and database connection for the demands portal module
Uses centralized database configuration from src.models.database
"""

import logging
import os
import sys
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import declarative_base, relationship
import json

logger = logging.getLogger(__name__)

# Add project root to path to import centralized database config
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import centralized database configuration
from src.models.database import SessionLocal, engine

# Use the centralized database engine and session
# Create a local Base for portal-specific models if needed
Base = declarative_base()

# Session factory using centralized config
PortalSessionLocal = SessionLocal


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
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

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
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "etapa": self.etapa,
            "prazo": self.prazo.isoformat() if self.prazo else None,
            "responsavel": self.responsavel,
            "status": self.status,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": (
                self.atualizado_em.isoformat() if self.atualizado_em else None
            ),
            "prioridade": self.prioridade,
            "categoria": self.categoria,
            "tags": self.tags,
            "arquivo_anexo": self.arquivo_anexo,
            "comentarios_internos": self.comentarios_internos,
            "tempo_estimado": self.tempo_estimado,
            "tempo_gasto": self.tempo_gasto,
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


# ===== CONTROLE MENSAL DATABASE MODELS =====

class ContabilidadeDB(Base):
    """
    Accounting firms (tenants) - mirrors the existing Contabilidades table
    """
    
    __tablename__ = "Contabilidades"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_contabilidade = Column(String(200), nullable=False)
    cnpj = Column(String(20), nullable=False, unique=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class EmpresaDB(Base):
    """
    Client companies - mirrors the existing Empresas table
    """
    
    __tablename__ = "Empresas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    contabilidade_id = Column(Integer, ForeignKey("Contabilidades.id"), nullable=False)
    sindicato_id = Column(Integer, ForeignKey("Sindicatos.id"), nullable=True)  # Added for CCT module
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class SindicatoDB(Base):
    """
    Labor unions/syndicates - for CCT management module
    """
    
    __tablename__ = "Sindicatos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_sindicato = Column(String(200), nullable=False)
    cnpj = Column(String(20), nullable=True, unique=True)
    base_territorial = Column(String(100), nullable=True)  # Ex: "São Paulo - SP"
    categoria_representada = Column(String(200), nullable=True)  # Ex: "Trabalhadores no Comércio"
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class ConvencaoColetivaCCTDB(Base):
    """
    Collective Bargaining Agreements (CCTs) - for CCT management module
    """
    
    __tablename__ = "ConvencoesColetivas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sindicato_id = Column(Integer, ForeignKey("Sindicatos.id"), nullable=False)
    numero_registro_mte = Column(String(50), nullable=True, unique=True)  # MTE registry code
    vigencia_inicio = Column(Date, nullable=False)
    vigencia_fim = Column(Date, nullable=False)
    link_documento_oficial = Column(String(500), nullable=True)  # URL to official PDF
    dados_cct = Column(JSON, nullable=True)  # Flexible JSON field for extracted CCT data
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LegislacaoDocumentoDB(Base):
    """
    Legislation documents - for legislation management module
    """
    
    __tablename__ = "DocumentosLegislacao"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(300), nullable=False)
    tipo_documento = Column(String(50), nullable=False)  # LEI, DECRETO, CCT, MEDIDA_PROVISORIA
    numero_documento = Column(String(100), nullable=True)  # Ex: "Lei 13.467/2017"
    data_publicacao = Column(Date, nullable=True)
    orgao_emissor = Column(String(200), nullable=True)  # Ex: "Ministério do Trabalho"
    arquivo_pdf = Column(String(500), nullable=True)  # Path to uploaded PDF
    dados_extraidos = Column(JSON, nullable=True)  # AI-extracted structured data
    status_processamento = Column(String(50), default="pendente", nullable=False)  # pendente, processando, concluido, erro
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    processado_em = Column(DateTime, nullable=True)


class ControleMensalDB(Base):
    """
    Monthly controls - mirrors the existing ControlesMensais table
    """
    
    __tablename__ = "ControlesMensais"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    status = Column(String(50), default="PENDENTE", nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class TarefaControleDB(Base):
    """
    Control tasks - mirrors the existing TarefasControle table
    """
    
    __tablename__ = "TarefasControle"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    controle_mensal_id = Column(Integer, ForeignKey("ControlesMensais.id"), nullable=False)
    descricao_tarefa = Column(String(200), nullable=False)
    concluida = Column(Boolean, default=False, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_conclusao = Column(DateTime, nullable=True)


class TemplateControleDB(Base):
    """
    Control templates for different types of companies
    """
    
    __tablename__ = "TemplatesControle"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contabilidade_id = Column(Integer, ForeignKey("Contabilidades.id"), nullable=False)
    nome_template = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class TemplateControleTarefaDB(Base):
    """
    Template tasks for control templates
    """
    
    __tablename__ = "TemplatesControle_Tarefas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey("TemplatesControle.id"), nullable=False)
    descricao_tarefa = Column(String(200), nullable=False)


class ProcessamentosFolhaDB(Base):
    """
    Payroll processing audit records - stores results of AI-powered auditing
    """
    
    __tablename__ = "ProcessamentosFolha"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    arquivo_pdf = Column(String(500), nullable=False)  # Path or name of the uploaded PDF
    dados_extraidos = Column(Text, nullable=True)  # JSON with extracted payroll data
    relatorio_divergencias = Column(Text, nullable=True)  # JSON with audit results
    total_funcionarios = Column(Integer, default=0)
    total_divergencias = Column(Integer, default=0)
    status_processamento = Column(String(50), default="PROCESSANDO", nullable=False)  # PROCESSANDO, CONCLUIDO, ERRO
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    concluido_em = Column(DateTime, nullable=True)


class HistoricoAnalisesRiscoDB(Base):
    """
    Risk analysis history - stores the complete risk analysis results for companies
    Allows tracking evolution of risk scores and provides business intelligence
    """
    
    __tablename__ = "HistoricoAnalisesRisco"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    contabilidade_id = Column(Integer, ForeignKey("Contabilidades.id"), nullable=False)
    score_risco = Column(Integer, nullable=False)  # Risk score from 0 to 100
    relatorio_completo = Column(Text, nullable=True)  # JSON stored as text for SQLite compatibility
    analisado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    analisado_por_user_id = Column(String(50), nullable=True)  # User who triggered the analysis
    
    def __repr__(self):
        return f"<HistoricoAnalisesRisco(id={self.id}, empresa_id={self.empresa_id}, score_risco={self.score_risco})>"


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
    Note: Using checkfirst=True to avoid recreating existing tables
    """
    try:
        # Create tables but don't overwrite existing ones
        Base.metadata.create_all(bind=engine, checkfirst=True)
        logger.info("Portal demandas database tables initialized (checkfirst=True)")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize portal_demandas tables: {e}")
        # Continue even if there are table creation issues (tables might already exist)
        return True


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
__all__ = [
    "TicketDB",
    "TicketComment",
    "ContabilidadeDB", 
    "EmpresaDB",
    "SindicatoDB",
    "ConvencaoColetivaCCTDB", 
    "LegislacaoDocumentoDB",
    "ControleMensalDB",
    "TarefaControleDB", 
    "TemplateControleDB",
    "TemplateControleTarefaDB",
    "ProcessamentosFolhaDB",
    "HistoricoAnalisesRiscoDB",
    "get_db",
    "init_portal_db",
    "test_db_connection",
    "Base",
    "engine",
    "SessionLocal",
]
