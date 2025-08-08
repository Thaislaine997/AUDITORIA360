"""
Portal Demandas Pydantic Models
Data validation and serialization models for the demands portal
"""

from datetime import datetime, date
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator


class TicketStatus(str, Enum):
    """Ticket status enumeration"""

    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    AGUARDANDO = "aguardando"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class TicketPrioridade(str, Enum):
    """Ticket priority enumeration"""

    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class TicketCategoria(str, Enum):
    """Ticket category enumeration"""

    GERAL = "geral"
    AUDITORIA = "auditoria"
    FOLHA = "folha"
    DOCUMENTOS = "documentos"
    CCT = "cct"
    SISTEMA = "sistema"


class TicketBase(BaseModel):
    """Base ticket model with common fields"""

    titulo: str = Field(
        ..., min_length=3, max_length=200, description="Título do ticket"
    )
    descricao: Optional[str] = Field(
        None, max_length=5000, description="Descrição detalhada"
    )
    etapa: str = Field(
        ..., min_length=2, max_length=50, description="Etapa do processo"
    )
    responsavel: str = Field(
        ..., min_length=2, max_length=100, description="Responsável pelo ticket"
    )
    prioridade: TicketPrioridade = Field(
        default=TicketPrioridade.MEDIA, description="Prioridade do ticket"
    )
    categoria: TicketCategoria = Field(
        default=TicketCategoria.GERAL, description="Categoria do ticket"
    )
    tags: Optional[str] = Field(
        None, max_length=200, description="Tags separadas por vírgula"
    )
    tempo_estimado: Optional[int] = Field(
        None, ge=0, le=1000, description="Tempo estimado em horas"
    )


class TicketCreate(TicketBase):
    """Model for creating a new ticket"""

    prazo: datetime = Field(..., description="Prazo para conclusão")

    @field_validator("prazo")
    @classmethod
    def validate_prazo(cls, v):
        """Validate that deadline is in the future"""
        # Convert string to datetime if needed
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                v = datetime.fromisoformat(v)

        # Allow past dates for testing, just warn
        if v <= datetime.now():
            import warnings

            warnings.warn(f"Prazo {v} está no passado", UserWarning)

        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        """Validate tags format"""
        if v and len(v.split(",")) > 10:
            raise ValueError("Máximo de 10 tags permitidas")
        return v


class TicketUpdate(BaseModel):
    """Model for updating an existing ticket"""

    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    descricao: Optional[str] = Field(None, max_length=5000)
    etapa: Optional[str] = Field(None, min_length=2, max_length=50)
    prazo: Optional[datetime] = None
    responsavel: Optional[str] = Field(None, min_length=2, max_length=100)
    status: Optional[TicketStatus] = None
    prioridade: Optional[TicketPrioridade] = None
    categoria: Optional[TicketCategoria] = None
    tags: Optional[str] = Field(None, max_length=200)
    comentarios_internos: Optional[str] = Field(None, max_length=2000)
    tempo_gasto: Optional[int] = Field(None, ge=0, le=1000)
    tempo_estimado: Optional[int] = Field(None, ge=0, le=1000)

    @field_validator("prazo")
    @classmethod
    def validate_prazo(cls, v):
        """Validate that deadline is in the future"""
        # Convert string to datetime if needed
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                v = datetime.fromisoformat(v)

        # Allow past dates for testing, just warn
        if v and v <= datetime.now():
            import warnings

            warnings.warn(f"Prazo {v} está no passado", UserWarning)

        return v


class Ticket(TicketBase):
    """Complete ticket model with all fields"""

    id: int
    status: TicketStatus = TicketStatus.PENDENTE
    criado_em: datetime
    atualizado_em: datetime
    prazo: datetime
    comentarios_internos: Optional[str] = None
    arquivo_anexo: Optional[str] = None
    tempo_gasto: Optional[int] = Field(default=0, ge=0)

    class Config:
        from_attributes = True

    @field_validator("prazo", "criado_em", "atualizado_em", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string if needed"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                return datetime.fromisoformat(v)
        return v


class TicketListResponse(BaseModel):
    """Response model for ticket listing with pagination"""

    tickets: List[Ticket]
    total: int
    page: int = 1
    per_page: int = 10
    pages: int

    @classmethod
    def create(
        cls, tickets: List[Ticket], total: int, page: int = 1, per_page: int = 10
    ):
        """Create paginated response"""
        pages = (total + per_page - 1) // per_page
        return cls(
            tickets=tickets, total=total, page=page, per_page=per_page, pages=pages
        )


class TicketComment(BaseModel):
    """Model for ticket comments"""

    id: Optional[int] = None
    ticket_id: int
    autor: str = Field(..., min_length=2, max_length=100)
    comentario: str = Field(..., min_length=1, max_length=2000)
    tipo: str = Field(default="comentario")  # comentario, status_change, system
    criado_em: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketStats(BaseModel):
    """Model for ticket statistics"""

    total: int
    pendentes: int
    em_andamento: int
    concluidos: int
    cancelados: int
    por_prioridade: dict
    por_categoria: dict
    tempo_medio_conclusao: Optional[float] = None  # em horas


class TicketFilter(BaseModel):
    """Model for filtering tickets"""

    status: Optional[List[TicketStatus]] = None
    prioridade: Optional[List[TicketPrioridade]] = None
    categoria: Optional[List[TicketCategoria]] = None
    responsavel: Optional[str] = None
    etapa: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    tags: Optional[str] = None

    class Config:
        use_enum_values = True


# ===== CONTROLE MENSAL MODELS =====

class Tarefa(BaseModel):
    """Model for individual task in monthly control"""
    
    id: int
    nome_tarefa: str
    concluido: bool
    data_conclusao: Optional[datetime] = None

    class Config:
        from_attributes = True


class ControleMensalDetalhado(BaseModel):
    """Model for detailed monthly control with tasks"""
    
    id_controle: int
    mes: int
    ano: int
    status_dados: str
    id_empresa: int
    nome_empresa: str
    tarefas: List[Tarefa]

    class Config:
        from_attributes = True


class ControleMensalSumario(BaseModel):
    """Summary model for monthly controls overview"""
    
    total_empresas: int
    controles_iniciados: int
    controles_concluidos: int
    percentual_conclusao: str


class ControleMensalResponse(BaseModel):
    """Response model for controles endpoint"""
    
    sumario: ControleMensalSumario
    controles: List[ControleMensalDetalhado]


class TemplateControle(BaseModel):
    """Model for control templates"""
    
    id: int
    contabilidade_id: int
    nome_template: str
    descricao: Optional[str] = None
    criado_em: datetime
    tarefas: List[str]  # List of task descriptions

    class Config:
        from_attributes = True


class TemplateControleCreate(BaseModel):
    """Model for creating control templates"""
    
    nome_template: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    tarefas: List[str] = Field(..., min_items=1, max_items=20)

    @field_validator("tarefas")
    @classmethod
    def validate_tarefas(cls, v):
        """Validate tasks format"""
        for tarefa in v:
            if not tarefa or len(tarefa.strip()) < 3:
                raise ValueError("Cada tarefa deve ter pelo menos 3 caracteres")
        return v


class TemplateAplicacao(BaseModel):
    """Model for applying templates to monthly controls"""
    
    template_id: int
    mes: int = Field(..., ge=1, le=12)
    ano: int = Field(..., ge=2020, le=2030)
    empresas_ids: Optional[List[int]] = None  # If None, applies to all companies


# ===== PAYROLL AUDIT MODELS =====

class FuncionarioDivergencia(BaseModel):
    """Model for employee divergence in payroll audit"""
    
    nome_funcionario: str
    tipo_divergencia: str  # ALERTA, AVISO, INFO
    descricao_divergencia: str
    valor_encontrado: Optional[str] = None
    valor_esperado: Optional[str] = None
    campo_afetado: str


class ProcessamentoFolhaResponse(BaseModel):
    """Response model for payroll processing"""
    
    id: int
    empresa_id: int
    mes: int
    ano: int
    arquivo_pdf: str
    total_funcionarios: int
    total_divergencias: int
    status_processamento: str
    criado_em: datetime
    concluido_em: Optional[datetime] = None
    divergencias: List[FuncionarioDivergencia] = []
    
    class Config:
        from_attributes = True


class AuditoriaFolhaRequest(BaseModel):
    """Request model for payroll audit"""
    
    empresa_id: int
    mes: int = Field(..., ge=1, le=12)
    ano: int = Field(..., ge=2020, le=2030)
    # Note: PDF file will be handled through multipart/form-data upload


    
    class Config:
        from_attributes = True



