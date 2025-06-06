from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Rubricas Mestre ---
class RubricaMestreCreateSchema(BaseModel):
    id_rubrica_mestre: Optional[str] = None
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = True

class RubricaMestreUpdateSchema(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = None

class RubricaMestreResponseSchema(BaseModel):
    id_rubrica_mestre: str
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

# --- Rubricas Cliente Config ---
class RubricaClienteConfigCreateSchema(BaseModel):
    id_rubrica_cliente: Optional[str] = None
    id_rubrica_mestre: str
    nome_personalizado: Optional[str] = None
    ativo: Optional[bool] = True

class RubricaClienteConfigUpdateSchema(BaseModel):
    nome_personalizado: Optional[str] = None
    ativo: Optional[bool] = None

class RubricaClienteConfigResponseSchema(BaseModel):
    id_rubrica_cliente: str
    id_rubrica_mestre: str
    nome_personalizado: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
