from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date, datetime

class SindicatoInfo(BaseModel):
    nome: str
    cnpj: Optional[str] = None

class CCTDocumentoCreateRequest(BaseModel):
    nome_documento_original: str = Field(...)
    data_inicio_vigencia_cct: date = Field(...)
    data_fim_vigencia_cct: Optional[date] = None
    sindicatos_laborais_json_str: Optional[str] = None
    sindicatos_patronais_json_str: Optional[str] = None
    numero_registro_mte: Optional[str] = None
    link_fonte_oficial: Optional[str] = None
    id_cct_base_fk: Optional[str] = None
    id_cliente_principal_associado: Optional[str] = None
    ids_clientes_afetados_lista_str: Optional[str] = None

class CCTDocumentoResponse(BaseModel):
    id_cct_documento: str
    nome_documento_original: str
    gcs_uri_documento: str
    data_inicio_vigencia_cct: date
    data_fim_vigencia_cct: Optional[date] = None
    sindicatos_laborais: Optional[List[SindicatoInfo]] = None
    sindicatos_patronais: Optional[List[SindicatoInfo]] = None
    status_processamento_ia: str

    class Config:
        from_attributes = True

class AlertaCCTResponse(BaseModel):
    id_alerta_cct: str
    numero_registro_mte_detectado: Optional[str] = None
    sindicatos_partes_detectados: Optional[str] = None
    vigencia_inicio_detectada: Optional[date] = None
    vigencia_fim_detectada: Optional[date] = None
    link_documento_fonte: Optional[str] = None
    texto_descricao_curta_cct: Optional[str] = None
    status_alerta: str
    data_deteccao: datetime
    id_cct_documento_importado_fk: Optional[str] = None
    admin_revisor_id: Optional[str] = None
    data_revisao_admin: Optional[datetime] = None
    notas_admin: Optional[str] = None

class UpdateAlertaStatusRequest(BaseModel):
    status_alerta: str
    notas_admin: Optional[str] = None

class ClausulaExtraidaResponse(BaseModel):
    id_clausula_extraida: str
    id_cct_documento_fk: str
    tipo_clausula_identificada: Optional[str] = None
    texto_clausula_extraido: str
    pagina_aproximada_documento: Optional[int] = None
    palavras_chave_clausula: Optional[List[str]] = None
    confianca_extracao_ia: Optional[float] = None
    status_revisao_humana: str
    usuario_revisao_humana: Optional[str] = None
    data_revisao_humana: Optional[datetime] = None
    notas_revisao_humana: Optional[str] = None
    timestamp_extracao_clausula: Optional[datetime] = None

class UpdateClausulaRevisaoRequest(BaseModel):
    status_revisao_humana: str
    usuario_revisao_humana: Optional[str] = None
    notas_revisao_humana: Optional[str] = None

class ProcessarSugestaoCCTRequest(BaseModel):
    acao_usuario: Literal["APROVAR_APLICAR", "REJEITAR"]
    dados_sugestao_atualizados_json: Optional[str] = Field(None, description="JSON string da sugestão como foi aprovada/editada pelo usuário. O backend usará isso para aplicar.")
    notas_revisao_usuario: Optional[str] = None
    usuario_revisao: str
