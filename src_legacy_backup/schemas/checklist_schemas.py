# Schemas placeholder para checklist folha
from pydantic import BaseModel
from typing import Optional

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
