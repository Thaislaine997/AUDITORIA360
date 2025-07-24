# Modelos para integração consultor de riscos
from typing import Optional, List
from pydantic import BaseModel

class ConsultorRiscosRequest(BaseModel):
    empresa_id: str
    periodo: str
    parametros_legais: Optional[dict] = None
    folha_processada: Optional[dict] = None

class ConsultorRiscosResponse(BaseModel):
    risco_id: str
    descricao: str
    nivel: str
    recomendacoes: Optional[List[str]] = None
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class RiscoPrevistoDetalheSchema(BaseModel):
    tipo_risco: str
    descricao_risco: str
    probabilidade: float
    impacto: str
    detalhes_adicionais: Optional[str] = None
    severidade_estimada: Optional[str] = None
    probabilidade_estimada: Optional[float] = None
    fator_principal: Optional[str] = None
    id_risco_detalhe: Optional[str] = None

class FatorContribuinteTecnicoSchema(BaseModel):
    fator: str
    descricao: str
    origem_dado: str
    valor_referencia: Optional[Any] = None

class DadosSuporteVisualizacaoSchema(BaseModel):
    tipo_grafico: str
    titulo: str
    titulo_grafico: Optional[str] = None
    dados: Dict[str, Any]
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
    principais_riscos_previstos: Optional[List[RiscoPrevistoDetalheSchema]] = None

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
