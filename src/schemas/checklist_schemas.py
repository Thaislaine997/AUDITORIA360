"""
Schemas para checklist de folha de pagamento.
"""

from typing import Optional

from pydantic import BaseModel


class ChecklistFolhaSchema(BaseModel):
    id: str
    nome: str


class ChecklistItemResponseSchema(BaseModel):
    id: str
    descricao: str
    status: str
    usuario_responsavel: Optional[str] = None


class ChecklistItemUpdateSchema(BaseModel):
    status: str
    notas: Optional[str] = None
    usuario_responsavel: Optional[str] = None
