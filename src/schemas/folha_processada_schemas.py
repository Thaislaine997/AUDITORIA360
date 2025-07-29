"""
Schemas para folha processada.
"""

from typing import Optional

from pydantic import BaseModel


class FolhaProcessadaSelecaoSchema(BaseModel):
    id_folha_processada: str
    descricao_display: Optional[str] = None
    periodo_referencia: Optional[str] = None
    status_geral_folha: Optional[str] = None
    # Outros campos podem ser adicionados conforme necessário
