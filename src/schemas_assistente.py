from pydantic import BaseModel, Field
from typing import Optional, Any, Literal
from datetime import datetime

class SugestaoAtualizacaoParametros(BaseModel):
    id_sugestao: str
    tipo_parametro: str
    dados_sugeridos_json: Any
    nome_documento_fonte: str
    texto_documento_fonte_hash: str
    status_sugestao: Literal["pendente", "aprovada", "rejeitada"]
    data_sugestao: datetime
    resumo_ia_sugestao: Optional[str]
    usuario_solicitante: str
    justificativa_rejeicao: Optional[str]
    data_aprovacao: Optional[datetime]
    usuario_aprovador: Optional[str]

class AprovarSugestaoPayload(BaseModel):
    usuario_aprovador: str

class RejeitarSugestaoPayload(BaseModel):
    usuario_aprovador: str
    justificativa_rejeicao: str
