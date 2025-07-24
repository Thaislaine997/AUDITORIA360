from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TicketCreate(BaseModel):
    titulo: str
    descricao: str
    etapa: str
    prazo: str  # Aceita string ISO
    responsavel: str

class Ticket(BaseModel):
    id: Optional[int]
    titulo: str
    descricao: str
    etapa: str
    prazo: str
    responsavel: str
    status: str = "pendente"
    criado_em: Optional[str] = None
    atualizado_em: Optional[str] = None

    @field_validator('prazo', mode='before')
    def parse_prazo(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v
