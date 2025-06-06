# src/schemas/checklist_schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Literal # Adicionado Literal
from datetime import datetime, date

class ChecklistItemBase(BaseModel):
    descricao_item_checklist: str
    ordem_item: int
    categoria_item: Optional[str] = None
    link_referencia_item: Optional[str] = None
    tipo_item: Literal["MANUAL", "AUTOMATICO", "BLOQUEADOR"] = "MANUAL"
    item_pai_id: Optional[str] = None
    # Campos que estavam no meu ChecklistItemBase original e que podem ser úteis aqui ou no Create/Response
    # id_folha_processada_fk: str
    # id_cliente: str
    # periodo_referencia: date
    # notas_observacoes_item: Optional[str] = None # Movido para Response e Update
    # usuario_responsavel_item: Optional[str] = None # Movido para Response e Update

class ChecklistItemCreateSchema(ChecklistItemBase):
    id_folha_processada_fk: str # Adicionado aqui conforme seu schema
    id_cliente: str # Adicionado aqui
    periodo_referencia: date # Adicionado aqui
    status_item_checklist: Literal["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "NAO_APLICAVEL", "BLOQUEADO"] = "PENDENTE"
    # id_item_checklist: str # O ID é geralmente gerado pelo backend antes da inserção, mas não faz parte do payload de criação da API.
                           # Se for gerado no controller antes de chamar um método de inserção que espera o ID, ok.
                           # O DDL tem id_item_checklist como NOT NULL.

class ChecklistItemResponseSchema(ChecklistItemBase): # Herda de ChecklistItemBase
    id_item_checklist: str
    id_folha_processada_fk: str # Adicionando campos que identificam o item completamente
    id_cliente: str
    periodo_referencia: date
    status_item_checklist: Literal["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "NAO_APLICAVEL", "BLOQUEADO"]
    data_conclusao_item: Optional[datetime] = None
    usuario_responsavel_item: Optional[str] = None
    notas_observacoes_item: Optional[str] = None
    data_criacao_registro: Optional[datetime] = None
    data_ultima_modificacao: Optional[datetime] = None

    class Config:
        orm_mode = True # Se for usar com ORM, mas para BigQuery pode não ser necessário.
                      # Mantido por compatibilidade se os dados vierem de um objeto com atributos.

class ChecklistItemUpdateSchema(BaseModel):
    status_item_checklist: Optional[Literal["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "NAO_APLICAVEL"]] = None
    notas_observacoes_item: Optional[str] = None
    usuario_responsavel_item: Optional[str] = None # Quem está atualizando

# Este schema pode ser útil se a rota GET retornar um objeto encapsulando a lista
# class ChecklistResponse(BaseModel):
# items: List[ChecklistItemResponseSchema]
