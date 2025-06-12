from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class RiscoPrevistoDetalheSchema(BaseModel):
    id_risco_detalhe: str
    tipo_risco: str
    nome_amigavel_risco: str
    probabilidade: float
    severidade_estimada: str
    principais_fatores: Optional[List[str]] = None
    explicacao_explainable_ai: Optional[Dict[str, Any]] = None
    descricao_risco: Optional[str] = None
    fator_principal: Optional[str] = None
    probabilidade_estimada: Optional[float] = None
    severidade_estimada_extra: Optional[str] = None  # Renomeado para evitar conflito

class PredicaoRiscoDashboardResponse(BaseModel):
    score_saude_folha: Optional[float] = None
    classe_risco_geral: Optional[str] = None
    principais_riscos_previstos: Optional[List[RiscoPrevistoDetalheSchema]] = None
    explicacao_geral_ia: Optional[str] = None
    id_folha_processada: Optional[str] = None
    periodo_referencia: Optional[date] = None

class DetalhePredicaoRiscoResponse(BaseModel):
    id_folha_processada: str
    risco_selecionado: Optional[RiscoPrevistoDetalheSchema] = None
    score_saude_folha: Optional[float] = None
    classe_risco_geral: Optional[str] = None
    fatores_contribuintes_tecnicos: Optional[List[Any]] = None
    explicacao_detalhada_ia: Optional[str] = None
    dados_suporte_visualizacao: Optional[List[Any]] = None
    recomendacoes_ia: Optional[List[str]] = None

class FatorContribuinteTecnicoSchema(BaseModel):
    feature: str
    valor: Any
    atribuicao_impacto: Any

class DadosSuporteVisualizacaoSchema(BaseModel):
    tipo_grafico: str
    titulo_grafico: str
    dados: Dict[str, Any]
