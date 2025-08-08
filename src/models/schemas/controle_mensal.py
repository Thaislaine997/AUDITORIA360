# /auditoria360/src/models/schemas/controle_mensal.py

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# --- Schemas para Tarefas ---
class TarefaBase(BaseModel):
    nome_tarefa: str
    concluido: bool = False


class Tarefa(TarefaBase):
    id: int
    controle_mensal_id: int
    data_conclusao: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Schemas para o Controle Mensal ---
class ControleMensalBase(BaseModel):
    mes: int = Field(..., ge=1, le=12)
    ano: int = Field(..., ge=2020)
    tipo_folha: Optional[str] = None
    status_dados: str = "AGUARD. DADOS"
    observacoes: Optional[str] = None


class ControleMensal(ControleMensalBase):
    id: int
    empresa_id: int
    tarefas: List[Tarefa] = []

    class Config:
        from_attributes = True


# --- Schema para a visualização completa, incluindo dados da empresa ---
class ControleMensalDetalhado(BaseModel):
    id_controle: int
    mes: int
    ano: int
    status_dados: str
    id_empresa: int
    nome_empresa: str
    tarefas: List[Tarefa]
