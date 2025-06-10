from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date # Adicionado date

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
    sindicatos_representados: Optional[List[str]] = None # Exemplo
    vigencia_inicio: Optional[date] = None # Alterado para date
    vigencia_fim: Optional[date] = None # Alterado para date
    # Adicione outros campos identificadores relevantes

class CCTDetalheResponse(CCTIdentificacaoResponse): # Herda da identificação
    texto_integral: Optional[str] = None
    clausulas: Optional[List[ClausulaExtraidaResponse]] = [] # Lista de cláusulas associadas
    status_processamento: Optional[str] = None # Ex: "Pendente", "Em Processamento", "Processado", "Erro"
    # Adicione outros detalhes da CCT

class CCTStatusResponse(BaseModel):
    id_cct: str
    status_atual: str
    mensagem: Optional[str] = None

class CCTUpdateStatusRequest(BaseModel):
    novo_status: str
    detalhes: Optional[str] = None

# Adicione aqui outros schemas que possam ser necessários para CCT, como CCTCreateRequest
class CCTCreateRequest(BaseModel):
    numero_registro_mte: str
    sindicatos_representados: List[str]
    vigencia_inicio: date # Alterado para date
    vigencia_fim: date    # Alterado para date
    dados_adicionais: Optional[Dict[str, Any]] = None

# --- Schemas para CCTDocumento e Alertas --- #

class Sindicato(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    natureza: Optional[str] = None # Ex: "Laboral", "Patronal"

class CCTDocumentoBase(BaseModel):
    nome_documento_original: str
    data_inicio_vigencia_cct: date
    data_fim_vigencia_cct: Optional[date] = None
    sindicatos_laborais: Optional[List[Sindicato]] = []
    sindicatos_patronais: Optional[List[Sindicato]] = []
    numero_registro_mte: Optional[str] = None
    link_fonte_oficial: Optional[str] = None
    id_cct_base_fk: Optional[str] = None # Para aditivos ou CCTs que substituem outras
    id_cliente_principal_associado: Optional[str] = None
    ids_clientes_afetados_lista: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    status_documento: str = "Recebido"
    # Campos de auditoria
    criado_em: Optional[Any] = None # Idealmente datetime, mas Any para simplicidade inicial
    modificado_em: Optional[Any] = None
    usuario_criacao: Optional[str] = None

class CCTDocumentoCreateRequest(CCTDocumentoBase):
    # Este schema é usado para criar/atualizar. Pode ser igual ao Base ou ter campos específicos.
    pass

class CCTDocumentoResponse(CCTDocumentoBase):
    id_documento_cct: str = Field(..., alias="_id") # Mapeia _id do MongoDB para id_documento_cct
    url_documento_gcs: Optional[str] = None
    hash_sha256_documento: Optional[str] = None
    data_upload: Optional[Any] = None # Idealmente datetime
    status_ocr: Optional[str] = "Pendente"
    status_extracao_clausulas: Optional[str] = "Pendente"

    class Config:
        from_attributes = True # Necessário para Pydantic V2 se estiver usando orm_mode
        populate_by_name = True # Permite usar alias como "_id"
        json_encoders = {
            # date: lambda v: v.isoformat(), # Exemplo se precisar de formatação customizada
        }

class AlertaCCTResponse(BaseModel):
    id_alerta: str = Field(..., alias="_id")
    tipo_alerta: str # Ex: "Nova CCT Publicada", "Vigência Expirando"
    id_cct_associada: Optional[str] = None
    mensagem: str
    data_criacao: Any # Idealmente datetime
    status_alerta: str = "Pendente" # Ex: "Pendente", "Visualizado", "Resolvido"
    notas_admin: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class UpdateAlertaStatusRequest(BaseModel):
    novo_status: str
    notas_admin: Optional[str] = None

class ProcessarSugestaoCCTRequest(BaseModel):
    acao: str # Ex: "aprovar", "rejeitar", "editar"
    justificativa: Optional[str] = None
    # Outros campos conforme necessário para o processamento da sugestão
