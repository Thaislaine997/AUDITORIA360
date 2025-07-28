"""
Portal Demandas Pydantic Models
Data validation and serialization models for the demands portal
"""

from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

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
    titulo: str = Field(..., min_length=3, max_length=200, description="Título do ticket")
    descricao: Optional[str] = Field(None, max_length=5000, description="Descrição detalhada")
    etapa: str = Field(..., min_length=2, max_length=50, description="Etapa do processo")
    responsavel: str = Field(..., min_length=2, max_length=100, description="Responsável pelo ticket")
    prioridade: TicketPrioridade = Field(default=TicketPrioridade.MEDIA, description="Prioridade do ticket")
    categoria: TicketCategoria = Field(default=TicketCategoria.GERAL, description="Categoria do ticket")
    tags: Optional[str] = Field(None, max_length=200, description="Tags separadas por vírgula")
    tempo_estimado: Optional[int] = Field(None, ge=0, le=1000, description="Tempo estimado em horas")

class TicketCreate(TicketBase):
    """Model for creating a new ticket"""
    prazo: datetime = Field(..., description="Prazo para conclusão")
    
    @field_validator('prazo')
    @classmethod
    def validate_prazo(cls, v):
        """Validate that deadline is in the future"""
        if v <= datetime.now():
            raise ValueError('Prazo deve ser uma data futura')
        return v
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        """Validate tags format"""
        if v and len(v.split(',')) > 10:
            raise ValueError('Máximo de 10 tags permitidas')
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
    
    @field_validator('prazo')
    @classmethod
    def validate_prazo(cls, v):
        """Validate that deadline is in the future"""
        if v and v <= datetime.now():
            raise ValueError('Prazo deve ser uma data futura')
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
        
    @field_validator('prazo', 'criado_em', 'atualizado_em', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string if needed"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
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
    def create(cls, tickets: List[Ticket], total: int, page: int = 1, per_page: int = 10):
        """Create paginated response"""
        pages = (total + per_page - 1) // per_page
        return cls(
            tickets=tickets,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages
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
