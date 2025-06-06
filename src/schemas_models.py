# filepath: src/schemas.py
# Este arquivo pode ser usado para definir Pydantic models para validação de dados,
# ou outros tipos de schemas usados na aplicação.

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime
from decimal import Decimal
import uuid

class ControleMensalEmpresaSchema(BaseModel):
    id: Optional[str] = None
    empresa_id: str
    ano_referencia: int
    mes_referencia: int
    status_dados_pasta: Optional[str] = None
    documentos_enviados_cliente: Optional[bool] = None
    data_envio_documentos_cliente: Optional[date] = None
    guia_fgts_gerada: Optional[bool] = None
    data_geracao_guia_fgts: Optional[date] = None
    darf_inss_gerado: Optional[bool] = None
    data_geracao_darf_inss: Optional[date] = None
    esocial_dctfweb_enviado: Optional[bool] = None
    data_envio_esocial_dctfweb: Optional[date] = None
    tipo_movimentacao: Optional[str] = None
    particularidades_observacoes: Optional[str] = None
    forma_envio_preferencial: Optional[str] = None
    email_contato_folha: Optional[str] = None
    nome_contato_cliente_folha: Optional[str] = None
    sindicato_id_aplicavel: Optional[str] = None
    data_criacao_registro: datetime = Field(default_factory=datetime.now)
    data_ultima_modificacao: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

# Schemas para Tabelas Regulatórias

class TabelaBase(BaseModel):
    id_versao: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Identificador único para esta versão da tabela")
    data_inicio_vigencia: date = Field(description="Data em que esta versão da tabela começa a valer")
    data_fim_vigencia: Optional[date] = Field(None, description="Data em que esta versão da tabela deixa de valer. Nulo se for a versão atualmente ativa.")
    descricao: Optional[str] = Field(None, description="Descrição ou observação sobre esta versão da tabela")
    data_criacao_registro: datetime = Field(default_factory=datetime.now, description="Quando esta entrada de versão foi criada no sistema")
    data_ultima_modificacao: datetime = Field(default_factory=datetime.now, description="Quando esta entrada de versão foi modificada pela última vez")
    data_inativacao: Optional[datetime] = Field(None, description="Data e hora em que esta versão do registro foi inativada (deleção lógica). Nulo se estiver ativa.")

    @model_validator(mode='after')
    def verificar_datas_de_vigencia(cls, values):
        data_inicio = values.data_inicio_vigencia
        data_fim = values.data_fim_vigencia
        
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValueError("A data_fim_vigencia não pode ser anterior à data_inicio_vigencia.")
        return values

class FaixaINSS(BaseModel):
    valor_inicial: Decimal = Field(..., description="Valor inicial da faixa de salário de contribuição")
    valor_final: Optional[Decimal] = Field(None, description="Valor final da faixa de salário de contribuição. Nulo para a última faixa antes do teto.")
    aliquota: Decimal = Field(..., description="Alíquota aplicável à faixa (ex: 7.5 para 7.5%)")

class TabelaINSS(TabelaBase):
    tipo_tabela: str = Field("INSS", description="Tipo da tabela, fixo como INSS")
    faixas: List[FaixaINSS] = Field(description="Lista das faixas de INSS para esta vigência")
    valor_teto_contribuicao: Optional[Decimal] = Field(None, description="Valor do teto de contribuição do INSS, se aplicável.")

class FaixaIRRF(BaseModel):
    base_calculo_inicial: Decimal = Field(..., description="Valor inicial da base de cálculo do IRRF")
    base_calculo_final: Optional[Decimal] = Field(None, description="Valor final da base de cálculo do IRRF. Nulo para a última faixa.")
    aliquota: Decimal = Field(..., description="Alíquota aplicável à faixa (ex: 7.5 para 7.5%)")
    parcela_a_deduzir: Decimal = Field(..., description="Parcela a deduzir do imposto apurado")

class TabelaIRRF(TabelaBase):
    tipo_tabela: str = Field("IRRF", description="Tipo da tabela, fixo como IRRF")
    faixas: List[FaixaIRRF] = Field(description="Lista das faixas de IRRF para esta vigência")
    deducao_por_dependente: Decimal = Field(description="Valor da dedução por dependente para esta vigência")
    limite_desconto_simplificado: Optional[Decimal] = None

class FaixaSalarioFamilia(BaseModel):
    remuneracao_maxima_elegivel: Decimal = Field(..., description="Remuneração máxima para ter direito à cota do salário família nesta faixa")
    valor_cota_por_filho: Decimal = Field(..., description="Valor da cota do salário família por filho/dependente")

class TabelaSalarioFamilia(TabelaBase):
    tipo_tabela: str = Field("SalarioFamilia", description="Tipo da tabela, fixo como Salário Família")
    faixas: List[FaixaSalarioFamilia] = Field(description="Lista das faixas de Salário Família para esta vigência")

class TabelaSalarioMinimo(TabelaBase):
    """Schema para a tabela de Salário Mínimo."""
    valor_nacional: float
    # Usaremos um dicionário para valores regionais, onde a chave é a sigla da região/estado e o valor é o salário.
    # Ex: {"SP": 1500.00, "RJ": 1450.00}
    valores_regionais: Optional[Dict[str, float]] = None
    observacao: Optional[str] = None

class TabelaFGTS(TabelaBase):
    """Schema para os parâmetros de FGTS."""
    aliquota_mensal: float
    aliquota_multa_rescisoria: float
    observacao: Optional[str] = None

# Schemas para Contabilidade e Usuários de Contabilidade

class ContabilidadeBase(BaseModel):
    cnpj: str = Field(..., description="CNPJ da empresa de contabilidade", examples=["00.000.000/0001-00"])
    razao_social: Optional[str] = Field(None, description="Razão Social da empresa de contabilidade", examples=["Contabilidade Exemplo LTDA"])
    nome_fantasia: Optional[str] = Field(None, description="Nome Fantasia da empresa de contabilidade", examples=["Contax Contabilidade"])

class ContabilidadeCreate(ContabilidadeBase):
    pass

class ContabilidadeResponse(ContabilidadeBase):
    id_contabilidade: str = Field(description="Identificador único da contabilidade")
    data_cadastro: datetime
    data_atualizacao: datetime
    ativo: bool

    class Config:
        from_attributes = True

class UsuarioContabilidadeBase(BaseModel):
    email: str = Field(..., description="Email de login do usuário", examples=["usuario@contabilidade.com"])
    nome_usuario: Optional[str] = Field(None, description="Nome do usuário", examples=["João Silva"])
    cargo: Optional[str] = Field(None, description="Cargo do usuário na contabilidade", examples=["Analista Contábil"])

class UsuarioContabilidadeCreate(UsuarioContabilidadeBase):
    senha: str = Field(..., min_length=8, description="Senha do usuário (mínimo 8 caracteres)")

class UsuarioContabilidadeResponse(UsuarioContabilidadeBase):
    id_usuario_contabilidade: str = Field(description="Identificador único do usuário da contabilidade")
    id_contabilidade: str = Field(description="Identificador da contabilidade vinculada")
    data_criacao: datetime
    data_ultimo_login: Optional[datetime] = None
    ativo: bool

    class Config:
        from_attributes = True

class RegistroContabilidadePayload(BaseModel):
    contabilidade: ContabilidadeCreate
    usuario: UsuarioContabilidadeCreate

class RegistroContabilidadeResponse(BaseModel):
    contabilidade: ContabilidadeResponse
    usuario: UsuarioContabilidadeResponse
    message: str = "Registro realizado com sucesso."

class LoginRequest(BaseModel):
    email: str = Field(..., examples=["usuario@contabilidade.com"])
    senha: str = Field(..., examples=["senhaSuperSegura123"])

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    id_usuario_contabilidade: Optional[str] = None # Adicionado para identificar o usuário no token
    id_contabilidade: Optional[str] = None # Adicionado para identificar a contabilidade no token

# Schema para representar uma Empresa Cliente (simplificado para listagem)
class EmpresaClienteSimplificado(BaseModel):
    id_empresa_cliente: str
    cnpj_empresa: str
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    ativo: bool
    cidade: Optional[str] = None
    uf: Optional[str] = None
    data_cadastro: Optional[datetime] = None
    responsavel: Optional[str] = None
    segmento: Optional[str] = None
    porte: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    observacao: Optional[str] = None

    class Config:
        from_attributes = True

# --- Rubricas Mestre ---
class RubricaMestreCreateSchema(BaseModel):
    id_rubrica_mestre: Optional[str] = None
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = True

class RubricaMestreUpdateSchema(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = None

class RubricaMestreResponseSchema(BaseModel):
    id_rubrica_mestre: str
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

# --- Rubricas Cliente Config ---
class RubricaClienteConfigCreateSchema(BaseModel):
    id_rubrica_cliente: Optional[str] = None
    id_rubrica_mestre: str
    nome_personalizado: Optional[str] = None
    ativo: Optional[bool] = True

class RubricaClienteConfigUpdateSchema(BaseModel):
    nome_personalizado: Optional[str] = None
    ativo: Optional[bool] = None

class RubricaClienteConfigResponseSchema(BaseModel):
    id_rubrica_cliente: str
    id_rubrica_mestre: str
    nome_personalizado: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

# Schemas para Dashboard de Saúde da Folha (Épico 2.3.1)
class ResumoDivergenciaPorSeveridade(BaseModel):
    severidade: str
    quantidade: int

class ResumoDivergenciaPorTipo(BaseModel):
    tipo_divergencia: str # Ex: VALOR_INSS_EMPREGADO
    quantidade: int
    soma_diferenca_absoluta: Decimal

class KPIDashboardSaudeFolha(BaseModel):
    total_bruto_folha_extrato: Optional[Decimal] = None
    total_liquido_folha_extrato: Optional[Decimal] = None
    numero_funcionarios_identificados: Optional[int] = None
    status_geral_folha: Optional[str] = None
    total_divergencias_identificadas: int
    # Para comparativo com mês anterior (opcional)
    variacao_percentual_total_bruto: Optional[float] = None
    variacao_percentual_num_funcionarios: Optional[float] = None
    variacao_percentual_total_divergencias: Optional[float] = None

class DashboardSaudeFolhaResponse(BaseModel):
    kpis: KPIDashboardSaudeFolha
    divergencias_por_severidade: List[ResumoDivergenciaPorSeveridade]
    divergencias_por_tipo: List[ResumoDivergenciaPorTipo]
    # Adicionar outros dados conforme necessário, como top 5 funcionários, etc.
    # top_funcionarios_com_divergencias: Optional[List[Dict]] = None

# Schemas para Consultor de Riscos com IA (Épico 3.2)

class ChatMessagePart(BaseModel):
    """Representa uma parte de uma mensagem de chat, que pode ser texto ou dados estruturados."""
    text: Optional[str] = None
    # Adicionar outros tipos de partes se necessário, ex: inline_data para imagens, etc.
    # inline_data: Optional[Dict] = None # Ex: { "mime_type": "image/png", "data": "base64_encoded_image" }

class ChatMessage(BaseModel):
    """Representa uma única mensagem no histórico do chat."""
    role: str = Field(..., description="Quem enviou a mensagem ('user' ou 'model')")
    parts: List[ChatMessagePart] = Field(..., description="Lista de partes da mensagem")
    timestamp: datetime = Field(default_factory=datetime.now)

class ConsultorRiscosRequest(BaseModel):
    """Schema para a requisição da API do consultor de riscos."""
    pergunta_usuario: str = Field(..., description="A pergunta ou comando do usuário.")
    id_folha_processada_contexto: Optional[str] = Field(None, description="ID da folha de pagamento processada para dar contexto à conversa.")
    historico_conversa_anterior: List[ChatMessage] = Field(default_factory=list, description="Histórico da conversa para manter o contexto.")
    # Outros parâmetros de configuração para o Gemini, se necessário
    # config_geracao: Optional[Dict] = None 
    # safety_settings: Optional[List[Dict]] = None

class ConsultorRiscosResponse(BaseModel):
    """Schema para a resposta da API do consultor de riscos."""
    resposta_consultor: str # Mantido para compatibilidade com o controller atual
    partes_resposta: Optional[List[ChatMessagePart]] = Field(None, description="Resposta do modelo em partes (se aplicável, para respostas mais ricas)")
    historico_conversa_atualizado: List[ChatMessage] = Field(..., description="Todo o histórico da conversa, incluindo a última interação.")
    dados_suporte: Optional[Dict[str, Any]] = Field(None, description="Dados adicionais que suportam a resposta, ex: riscos identificados, links para documentos, etc.")
    # id_sessao_chat: Optional[str] = Field(None, description="ID da sessão de chat, se aplicável")


# Schemas para Visualização de Riscos Preditivos e Score de Saúde (Épico 3.3)

class RiscoPrevistoDetalheSchema(BaseModel):
    id_risco_detalhe: str # UUID para identificar unicamente este risco detalhado na lista
    descricao_risco: str
    probabilidade_estimada: Optional[float] = None # 0-1
    severidade_estimada: Optional[str] = None # BAIXA, MEDIA, ALTA, CRITICA
    fator_principal: Optional[str] = None # Descrição do principal fator
    # Outros campos como 'tipo_risco_tecnico' podem ser adicionados internamente
    # Adicionado para compatibilidade com o mock do controller
    nome_amigavel_risco: Optional[str] = None 
    tipo_risco: Optional[str] = None
    principais_fatores: Optional[List[str]] = None
    explicacao_explainable_ai: Optional[Dict[str, float]] = None


class PredicaoRiscoDashboardResponse(BaseModel):
    score_saude_folha: Optional[float] = None # Alterado para float para consistência, pode ser int no display
    classe_risco_geral: Optional[str] = None
    principais_riscos_previstos: List[RiscoPrevistoDetalheSchema] = []
    explicacao_geral_ia: Optional[str] = None
    id_folha_processada: str
    periodo_referencia: date # Para confirmar o contexto no frontend

class FatorContribuinteTecnicoSchema(BaseModel):
    feature: str # Nome da feature do modelo
    valor: Any # Valor da feature para esta folha/predição
    atribuicao_impacto: Optional[float] = None # Ex: SHAP value ou outra medida de importância/atribuição do Explainable AI

class DadosSuporteVisualizacaoSchema(BaseModel):
    tipo_grafico: Optional[str] = None # Ex: "SERIE_TEMPORAL", "LISTA_TEXTO", "VALOR_SIMPLES"
    titulo_grafico: Optional[str] = None
    dados: Any # Pode ser uma lista de valores para série temporal, lista de strings, dict para valor simples etc.
    # Ex: {"historico_horas_extras_depto_X": [10, 12, 11, 15.5], "label_eixo_x": "Mês", "label_eixo_y": "Horas"}

class DetalhePredicaoRiscoResponse(BaseModel):
    id_folha_processada: str
    risco_selecionado: Optional[RiscoPrevistoDetalheSchema] = None # Se for detalhe de um risco específico
    score_saude_folha: Optional[float] = None # Se for detalhe do score geral
    classe_risco_geral: Optional[str] = None
    
    fatores_contribuintes_tecnicos: List[FatorContribuinteTecnicoSchema] = []
    explicacao_detalhada_ia: str # Gerada/Refinada pelo Gemini
    dados_suporte_visualizacao: Optional[List[DadosSuporteVisualizacaoSchema]] = None # Lista de dados para gráficos contextuais
    recomendacoes_ia: Optional[List[str]] = None

class FolhaProcessadaSelecaoSchema(BaseModel):
    id_folha_processada: str
    descricao_display: str
    periodo_referencia: date
    status_geral_folha: str

__all__ = [
    "ControleMensalEmpresaSchema",
    "ChatMessagePart",
    "ChatMessage",
    "ConsultorRiscosRequest",
    "ConsultorRiscosResponse",
    "RiscoPrevistoDetalheSchema",
    "PredicaoRiscoDashboardResponse",
    "FatorContribuinteTecnicoSchema",
    "DadosSuporteVisualizacaoSchema",
    "DetalhePredicaoRiscoResponse",
    "DashboardSaudeFolhaResponse",
    "KPIDashboardSaudeFolha",
    "ResumoDivergenciaPorSeveridade",
    "ResumoDivergenciaPorTipo",
    "FolhaProcessadaSelecaoSchema",
    # Adicione outros schemas conforme necessário
]