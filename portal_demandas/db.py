"""
Portal Demandas Database Configuration
SQLAlchemy models and database connection for the demands portal module
Uses centralized database configuration from src.models.database
"""

import logging
import os
import sys
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey, Date, JSON, DECIMAL, ARRAY
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
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


# =====================================================================
# GRAND TOMO ARCHITECTURE - NEW DATABASE MODELS
# =====================================================================

class LogOperacoesDB(Base):
    """
    Audit Trail System - The "immutable memory" of the system
    Every write operation in the system is logged here
    """
    
    __tablename__ = "LOGOPERACOES"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID, nullable=True)  # References auth.users(id)
    contabilidade_id = Column(Integer, ForeignKey("Contabilidades.id"), nullable=True)
    operacao = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, etc.
    tabela_afetada = Column(String(100), nullable=False)  # Which table was affected
    registro_id = Column(String(100), nullable=True)  # ID of the affected record
    detalhes_operacao = Column(JSONB, nullable=False)  # Complete details of the operation
    timestamp_operacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_origem = Column(INET, nullable=True)  # IP address of the operation origin
    user_agent = Column(Text, nullable=True)  # Browser/client information
    session_id = Column(String(255), nullable=True)  # Session identifier
    resultado = Column(String(20), default='SUCCESS', nullable=False)  # SUCCESS, ERROR, WARNING


class DeclaracoesFiscaisDB(Base):
    """
    Tax Declarations Integration - For cross-referencing payroll calculations
    with official declarations (DCTFWeb, DIRF, GFIP, eSocial, etc.)
    """
    
    __tablename__ = "DeclaracoesFiscais"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    tipo_declaracao = Column(String(50), nullable=False)  # DCTFWeb, DIRF, GFIP, eSocial
    periodo_competencia = Column(Date, nullable=False)  # Competency period
    numero_recibo = Column(String(100), nullable=True)  # Receipt number from tax authority
    data_transmissao = Column(DateTime, nullable=True)  # When it was transmitted
    status_declaracao = Column(String(20), default='PENDENTE', nullable=False)  # PENDENTE, TRANSMITIDA, HOMOLOGADA, REJEITADA
    valores_declarados = Column(JSONB, nullable=False)  # All declared values in structured format
    arquivo_original = Column(String(500), nullable=True)  # Path to original file
    hash_arquivo = Column(String(255), nullable=True)  # File hash for integrity verification
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class PlanosContasDB(Base):
    """
    Chart of Accounts - For automatic accounting entry drafts
    """
    
    __tablename__ = "PlanosContas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    codigo_conta = Column(String(50), nullable=False)  # Account code (e.g., "1.1.1.01.001")
    nome_conta = Column(String(200), nullable=False)  # Account name
    tipo_conta = Column(String(30), nullable=False)  # ATIVO, PASSIVO, PATRIMONIO_LIQUIDO, RECEITA, DESPESA
    conta_pai_id = Column(Integer, ForeignKey("PlanosContas.id"), nullable=True)  # Parent account
    nivel = Column(Integer, default=1, nullable=False)  # Hierarchy level
    aceita_lancamento = Column(Boolean, default=True, nullable=False)  # Whether this account accepts entries
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LancamentosContabeisDB(Base):
    """
    Accounting Entries - Automatically generated drafts from audit processes
    """
    
    __tablename__ = "LancamentosContabeis"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    numero_lancamento = Column(String(50), nullable=False)  # Entry number
    data_lancamento = Column(Date, nullable=False)
    historico = Column(Text, nullable=False)  # Entry description
    valor_total = Column(DECIMAL(15,2), nullable=False)
    origem_lancamento = Column(String(50), nullable=False)  # FOLHA_PAGAMENTO, AUDITORIA_IA, MANUAL
    referencia_origem_id = Column(Integer, nullable=True)  # ID of the source record
    status_lancamento = Column(String(20), default='RASCUNHO', nullable=False)  # RASCUNHO, APROVADO, CONTABILIZADO, CANCELADO
    aprovado_por = Column(UUID, nullable=True)  # References auth.users(id)
    aprovado_em = Column(DateTime, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LancamentosContabeisItensDB(Base):
    """
    Individual debit/credit items for each accounting entry
    """
    
    __tablename__ = "LancamentosContabeisItens"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lancamento_id = Column(Integer, ForeignKey("LancamentosContabeis.id"), nullable=False)
    conta_id = Column(Integer, ForeignKey("PlanosContas.id"), nullable=False)
    tipo_movimentacao = Column(String(10), nullable=False)  # DEBITO or CREDITO
    valor = Column(DECIMAL(15,2), nullable=False)
    historico_item = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class NotificacoesDB(Base):
    """
    Notification System - Proactive communication with users
    """
    
    __tablename__ = "Notificacoes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(UUID, nullable=True)  # References auth.users(id)
    contabilidade_id = Column(Integer, ForeignKey("Contabilidades.id"), nullable=True)
    tipo_notificacao = Column(String(20), nullable=False)  # INFO, ALERTA, ERRO, SUCESSO
    titulo = Column(String(200), nullable=False)
    mensagem = Column(Text, nullable=False)
    link_acao = Column(String(500), nullable=True)  # URL to take action
    prioridade = Column(String(20), default='MEDIA', nullable=False)  # BAIXA, MEDIA, ALTA, CRITICA
    lida = Column(Boolean, default=False, nullable=False)
    data_leitura = Column(DateTime, nullable=True)
    origem_notificacao = Column(String(50), nullable=True)  # Which system generated this
    dados_contexto = Column(JSONB, nullable=True)  # Additional context data
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    expira_em = Column(DateTime, nullable=True)  # Expiration date


class AlertasPrazosDB(Base):
    """
    Deadline Alerts - Automated monitoring of important dates
    """
    
    __tablename__ = "AlertasPrazos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("Empresas.id"), nullable=False)
    tipo_prazo = Column(String(50), nullable=False)  # CCT_VENCIMENTO, DECLARACAO_FISCAL, AUDITORIA_MENSAL
    descricao = Column(Text, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    dias_antecedencia = Column(Integer, default=7, nullable=False)  # Days before deadline
    status_alerta = Column(String(20), default='ATIVO', nullable=False)  # ATIVO, DISPARADO, CONCLUIDO, CANCELADO
    ultimo_disparo = Column(DateTime, nullable=True)
    configuracao_disparo = Column(JSONB, nullable=True)  # Alert configuration
    referencia_id = Column(Integer, nullable=True)  # Reference to related record
    tipo_referencia = Column(String(50), nullable=True)  # Type of referenced record
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AtendimentosSuporteDB(Base):
    """
    Integrated Support Ticket System
    """
    
    __tablename__ = "AtendimentosSuporte"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contabilidade_id = Column(Integer, ForeignKey("Contabilidades.id"), nullable=False)
    usuario_solicitante = Column(UUID, nullable=True)  # References auth.users(id)
    numero_ticket = Column(String(20), nullable=False, unique=True)  # Formatted ticket number
    assunto = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    categoria = Column(String(30), nullable=False)  # TECNICO, FUNCIONAL, DUVIDA, BUG, MELHORIA
    prioridade = Column(String(20), default='MEDIA', nullable=False)  # BAIXA, MEDIA, ALTA, CRITICA
    status = Column(String(30), default='ABERTO', nullable=False)  # ABERTO, EM_ANDAMENTO, AGUARDANDO_CLIENTE, RESOLVIDO, FECHADO
    atribuido_para = Column(UUID, nullable=True)  # References auth.users(id)
    data_resolucao = Column(DateTime, nullable=True)
    tempo_primeira_resposta = Column(Integer, nullable=True)  # Minutes until first response
    tempo_resolucao = Column(Integer, nullable=True)  # Minutes until resolution
    satisfacao_cliente = Column(Integer, nullable=True)  # 1-5 scale
    tags = Column(ARRAY(String), nullable=True)  # Array of tags
    dados_contexto = Column(JSONB, nullable=True)  # Additional context
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AtendimentosSuporteInteracoesDB(Base):
    """
    All interactions/history for support tickets
    """
    
    __tablename__ = "AtendimentosSuporteInteracoes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    atendimento_id = Column(Integer, ForeignKey("AtendimentosSuporte.id"), nullable=False)
    usuario_id = Column(UUID, nullable=True)  # References auth.users(id)
    tipo_interacao = Column(String(30), nullable=False)  # COMENTARIO, STATUS_CHANGE, ASSIGNMENT, ATTACHMENT
    conteudo = Column(Text, nullable=True)
    arquivo_anexo = Column(String(500), nullable=True)  # Path to attached file
    visivel_cliente = Column(Boolean, default=True, nullable=False)
    dados_adiciais = Column(JSONB, nullable=True)  # Additional structured data
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


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
    # Grand Tomo Architecture Models
    "LogOperacoesDB",
    "DeclaracoesFiscaisDB", 
    "PlanosContasDB",
    "LancamentosContabeisDB",
    "LancamentosContabeisItensDB",
    "NotificacoesDB",
    "AlertasPrazosDB",
    "AtendimentosSuporteDB",
    "AtendimentosSuporteInteracoesDB",
    # Functions
    "get_db",
    "init_portal_db",
    "test_db_connection",
    "Base",
    "engine",
    "SessionLocal",
]
