from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ClausulaExtraidaResponse(BaseModel):
    id_clausula: Optional[str] = None
    texto_clausula: str
    tipo_clausula: str
    relevancia: Optional[float] = None
    # Adicione outros campos conforme necessário com base na sua lógica de negócios


class UpdateClausulaRevisaoRequest(BaseModel):
    revisado: bool
    texto_revisado: Optional[str] = None
    comentarios: Optional[str] = None
    # Adicione outros campos conforme necessário


# Schemas para CCT (Convenção Coletiva de Trabalho)
class CCTIdentificacaoResponse(BaseModel):
    id_cct: str
    numero_registro_mte: Optional[str] = None
    sindicatos_representados: Optional[List[str]] = None
    vigencia_inicio: Optional[date] = None
    vigencia_fim: Optional[date] = None
    # Adicione outros campos identificadores relevantes


class CCTDetalheResponse(CCTIdentificacaoResponse):
    texto_integral: Optional[str] = None
    clausulas: Optional[List[ClausulaExtraidaResponse]] = []
    status_processamento: Optional[str] = None
    # Adicione outros detalhes da CCT


class CCTStatusResponse(BaseModel):
    id_cct: str
    status_atual: str
    mensagem: Optional[str] = None


class CCTUpdateStatusRequest(BaseModel):
    novo_status: str
    detalhes: Optional[str] = None


class CCTDocumentoCreateRequest(BaseModel):
    nome_documento_original: str
    data_inicio_vigencia_cct: date
    data_fim_vigencia_cct: Optional[date] = None
    sindicatos_laborais: Optional[List[str]] = None
    sindicatos_patronais: Optional[List[str]] = None
    numero_registro_mte: Optional[str] = None
    link_fonte_oficial: Optional[str] = None
    id_cct_base_fk: Optional[str] = None
    id_cliente_principal_associado: Optional[str] = None
    ids_clientes_afetados_lista: Optional[List[str]] = None


class CCTDocumentoResponse(BaseModel):
    _id: str
    nome_documento_original: str
    data_inicio_vigencia_cct: date
    data_fim_vigencia_cct: Optional[date] = None
    sindicatos_laborais: Optional[List[str]] = None
    sindicatos_patronais: Optional[List[str]] = None
    numero_registro_mte: Optional[str] = None
    link_fonte_oficial: Optional[str] = None
    id_cct_base_fk: Optional[str] = None
    id_cliente_principal_associado: Optional[str] = None
    ids_clientes_afetados_lista: Optional[List[str]] = None
    status_documento: Optional[str] = None
    status_processamento_ia: Optional[str] = None
    gcs_uri_documento: Optional[str] = None


class AlertaCCTResponse(BaseModel):
    id_alerta: str
    id_cct: str
    status: str
    notas: Optional[str] = None


class UpdateAlertaStatusRequest(BaseModel):
    status: str
    notas: Optional[str] = None
