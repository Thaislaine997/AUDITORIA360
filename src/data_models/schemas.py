from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class RiscoPrevistoDetalheSchema(BaseModel):
    tipo_risco: str
    descricao_risco: str # Mantido, parece correto
    probabilidade: float # Mantido
    impacto: str # Mantido
    detalhes_adicionais: Optional[str] = None
    # Campos adicionados/corrigidos com base no uso em 1_📈_Dashboard_Folha.py
    severidade_estimada: Optional[str] = None
    probabilidade_estimada: Optional[float] = None
    fator_principal: Optional[str] = None
    id_risco_detalhe: Optional[str] = None # ou int, dependendo da origem

class FatorContribuinteTecnicoSchema(BaseModel):
    fator: str
    descricao: str
    origem_dado: str
    valor_referencia: Optional[Any] = None

class DadosSuporteVisualizacaoSchema(BaseModel):
    tipo_grafico: str # e.g., 'bar', 'line', 'pie'
    titulo: str # Mantido, mas o erro indicava visualizacao.titulo_grafico
    titulo_grafico: Optional[str] = None # Adicionado para corresponder ao uso
    dados: Dict[str, Any] # Formato dos dados dependerá do tipo de gráfico
    configuracoes_layout: Optional[Dict[str, Any]] = None

class PredicaoRiscoDashboardResponse(BaseModel):
    total_colaboradores: int
    media_risco_contratual: float
    media_risco_conformidade: float
    media_risco_operacional: float
    media_risco_financeiro: float
    distribuicao_risco_departamento: Dict[str, float]
    distribuicao_risco_cargo: Dict[str, float]
    tendencia_risco_mensal: Dict[str, float]
    score_saude_folha: Optional[float] = None
    classe_risco_geral: Optional[str] = None
    explicacao_geral_ia: Optional[str] = None
    principais_riscos_previstos: Optional[List[RiscoPrevistoDetalheSchema]] = None # Alterado para usar o schema definido acima

class DetalhePredicaoRiscoResponse(BaseModel):
    id_colaborador: str
    nome_colaborador: str
    cargo: str
    departamento: str
    data_admissao: date
    risco_total_calculado: float
    fatores_risco: Dict[str, Any]
    sugestoes_mitigacao: List[str]
    risco_selecionado: Optional[RiscoPrevistoDetalheSchema] = None
    explicacao_detalhada_ia: Optional[str] = None
    fatores_contribuintes_tecnicos: Optional[List[FatorContribuinteTecnicoSchema]] = None
    dados_suporte_visualizacao: Optional[List[DadosSuporteVisualizacaoSchema]] = None
    recomendacoes_ia: Optional[List[str]] = None

class ControleFolhaResponse(BaseModel):
    id_folha: str
    mes_referencia: str
    ano_referencia: int
    total_colaboradores: int
    valor_total_folha: float
    status_processamento: str
    data_upload: datetime
    data_processamento: Optional[datetime] = None
    erros_importacao: Optional[List[str]] = None

class UploadResponse(BaseModel):
    message: str
    file_id: Optional[str] = None
    filename: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None

class ObrigacoesMensaisResponse(BaseModel):
    id_obrigacao: str
    nome_obrigacao: str
    prazo_entrega: date
    status: str # Ex: "Pendente", "Em Atraso", "Concluído"
    detalhes: Optional[str] = None
    link_referencia: Optional[str] = None

class AnaliseCCTResponse(BaseModel):
    id_cct: str
    sindicato_laboral: str
    sindicato_patronal: str
    data_assinatura: date
    vigencia_inicio: date
    vigencia_fim: date
    clausulas_relevantes: List[Dict[str, Any]] # Ex: {"numero_clausula": "10", "resumo": "...", "impacto_risco": "Alto"}
    pontos_atencao: List[str]

class ChecklistResponse(BaseModel):
    id_checklist: str
    nome_checklist: str
    area_auditoria: str # Ex: "Folha de Pagamento", "Contratos", "CCTs"
    itens_verificacao: List[Dict[str, Any]] # Ex: {"item": "...", "status": "Conforme/Não Conforme/N/A", "observacao": "..."} 
    data_conclusao: Optional[date] = None
    responsavel: Optional[str] = None

class ParametroLegalResponse(BaseModel):
    id_parametro: str
    nome_parametro: str
    descricao: str
    fonte_legal: str # Ex: "CLT Art. X", "NR Y"
    data_ultima_atualizacao: date
    aplicabilidade: List[str] # Ex: ["Todos os Colaboradores", "Apenas Gestantes"]

class SugestaoCCTResponse(BaseModel):
    id_sugestao: str
    clausula_original: str
    sugestao_melhoria: str
    justificativa: str
    impacto_esperado: str # Ex: "Redução de Risco Trabalhista", "Melhoria de Benefícios"
    status_implementacao: Optional[str] = None # Ex: "Sugerido", "Em Análise", "Implementado"

class UserResponse(BaseModel):
    id_usuario: str
    nome_completo: str
    email: EmailStr
    perfil_acesso: str # Ex: "Administrador", "Gestor RH", "Auditor"
    ativo: bool
    ultimo_login: Optional[datetime] = None

class ClientResponse(BaseModel):
    id_cliente: str
    nome_empresa: str
    cnpj: str
    setor_atuacao: str
    data_cadastro: datetime
    ativo: bool

class AuthRequest(BaseModel):
    username: str = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: Optional[UserResponse] = None

# Schemas de Dados para interações internas ou cargas, podem ser mais granulares
class ClientData(BaseModel):
    client_id: str
    name: str
    # Outros campos relevantes do cliente

class FolhaData(BaseModel):
    id_colaborador: str
    mes: int
    ano: int
    salario_bruto: float
    # Outros campos da folha

class CCTData(BaseModel):
    id_cct: str
    descricao_clausula: str
    # Outros campos da CCT

class ParametroLegalData(BaseModel):
    id_parametro: str
    descricao_parametro: str
    # Outros campos de parâmetros legais

class ChecklistData(BaseModel):
    id_item_checklist: str
    descricao_item: str
    status: str
    # Outros campos do checklist

class SugestaoCCTData(BaseModel):
    id_sugestao: str
    descricao_sugestao: str
    # Outros campos de sugestões CCT

class ErrorDetail(BaseModel):
    loc: List[str | int]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: Optional[List[ErrorDetail]] = None

class HealthCheckResponse(BaseModel):
    status: str = "OK"
    message: str = "API is healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BigQueryLoadConfig(BaseModel):
    project_id: str
    dataset_id: str
    table_id: str
    credentials_path: Optional[str] = None # Caminho para o arquivo JSON de credenciais
    # Adicionar outros campos conforme necessário, como schema, write_disposition, etc.

class BigQueryJobResponse(BaseModel):
    job_id: str
    status: str
    errors: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None

class GenericResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[List[Dict[str, Any]]] = None

class FileUploadRequest(BaseModel):
    file_type: str # Ex: "folha_pagamento", "cct_documento", "outros_documentos"
    client_id: str
    metadata: Optional[Dict[str, Any]] = None # Metadados adicionais como mes_referencia, ano_referencia, etc.

# Adicionando os esquemas que faltavam com base nos erros de importação
class RiscoCalculado(BaseModel):
    tipo_risco: str
    nivel_risco: float
    detalhes: Optional[str] = None

class ColaboradorRisco(BaseModel):
    id_colaborador: str
    nome: str
    cargo: str
    departamento: str
    riscos: List[RiscoCalculado]
    risco_geral: float

class DashboardDataResponse(BaseModel):
    total_colaboradores: int
    media_risco_geral: float
    distribuicao_riscos_departamento: Dict[str, float]
    distribuicao_riscos_cargo: Dict[str, float]
    colaboradores_alto_risco: List[ColaboradorRisco]

class DetalheColaboradorResponse(BaseModel):
    id_colaborador: str
    nome: str
    cargo: str
    departamento: str
    data_admissao: date
    salario_atual: float
    historico_risco: List[Dict[str, Any]] # e.g., {"mes_ano": "01/2024", "risco_calculado": 0.7}
    fatores_impacto_recente: List[str]
    sugestoes_mitigacao_especificas: List[str]

class ProcessamentoFolhaStatus(BaseModel):
    id_processamento: str
    nome_arquivo: str
    data_upload: datetime
    status: str # "Em processamento", "Concluído com sucesso", "Falha no processamento"
    total_registros: Optional[int] = None
    registros_processados: Optional[int] = None
    registros_com_erro: Optional[int] = None
    erros_detalhados: Optional[List[Dict[str, Any]]] = None # e.g., {"linha": 10, "erro": "Formato de data inválido"}

class CCTDetalheResponse(BaseModel):
    id_cct: str
    sindicato_representante: str
    data_vigencia_inicio: date
    data_vigencia_fim: date
    clausulas_principais: List[Dict[str, str]] # e.g., {"numero": "15.a", "descricao": "Adicional de periculosidade"}
    clausulas_nao_conformes_detectadas: List[Dict[str, str]] # e.g., {"clausula_cct": "X", "lei_referencia": "Y", "discrepancia": "..."}
    sugestoes_ajuste_cct: List[str]

class ChecklistItem(BaseModel):
    id_item: str
    descricao: str
    status_conformidade: str # "Conforme", "Não Conforme", "Não Aplicável", "Pendente"
    observacoes: Optional[str] = None
    evidencias_necessarias: Optional[List[str]] = None
    data_verificacao: Optional[date] = None
    responsavel_verificacao: Optional[str] = None

class ChecklistAuditoriaResponse(BaseModel):
    id_auditoria_checklist: str
    titulo_checklist: str
    area_foco: str # "Folha de Pagamento", "Benefícios", "Contratos de Trabalho"
    data_inicio_auditoria: date
    data_fim_prevista_auditoria: date
    status_geral_checklist: str # "Não Iniciado", "Em Andamento", "Concluído", "Pendente Revisão"
    itens_checklist: List[ChecklistItem]
    percentual_conformidade: Optional[float] = None
    pontos_criticos_identificados: Optional[List[str]] = None

class ParametroLegalDetalheResponse(BaseModel):
    id_parametro: str
    codigo_legal: str # e.g., "CLT Art. 457"
    descricao_resumida: str
    texto_integral_lei: Optional[str] = None
    data_ultima_revisao_parametro: date
    impacto_nas_operacoes_rh: str
    historico_alteracoes_parametro: List[Dict[str, Any]] # e.g., {"data_alteracao": "2023-01-01", "resumo_mudanca": "..."}

class SugestaoOtimizacaoResponse(BaseModel):
    id_sugestao: str
    area_processo_rh: str # "Recrutamento", "Folha", "Gestão de CCTs"
    descricao_problema_identificado: str
    sugestao_melhoria_proposta: str
    beneficios_esperados: List[str] # e.g., "Redução de X% em custos", "Aumento de Y% em eficiência"
    nivel_prioridade_sugestao: str # "Alta", "Média", "Baixa"
    status_implementacao_sugestao: str # "A implementar", "Em análise", "Implementada"

# Modelos para autenticação e usuário, se ainda não definidos de forma completa
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    nome_completo: str
    perfil_acesso: str = "Leitor" # Default profile

class User(UserBase):
    id_usuario: str # ou int, dependendo do seu DB
    nome_completo: str
    perfil_acesso: str
    ativo: bool
    data_criacao: datetime
    ultimo_login: Optional[datetime] = None

    class Config:
        orm_mode = True
