# filepath: src/schemas.py
# Este arquivo pode ser usado para definir Pydantic models para validação de dados,
# ou outros tipos de schemas usados na aplicação.

from typing import Optional, List, Dict
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

# --- Rubricas Mestre (DicionarioRubricasMestre) ---
class RubricaMestreBaseSchema(BaseModel):
    id_rubrica_mestre: Optional[str] = Field(None, description="ID único da rubrica mestre")
    codigo_esocial_sugestao: str = Field(..., description="Código sugerido do eSocial")
    descricao_padrao: str = Field(..., description="Descrição padrão da rubrica")
    natureza_juridica_sugestao: Optional[str] = Field(None, description="Natureza jurídica sugerida")
    incide_inss_padrao: bool = Field(..., description="Incide INSS por padrão?")
    incide_irrf_padrao: bool = Field(..., description="Incide IRRF por padrão?")
    incide_fgts_padrao: bool = Field(..., description="Incide FGTS por padrão?")
    explicacao_incidencias_padrao: Optional[str] = Field(None, description="Explicação padrão das incidências")
    tipo_rubrica_padrao: Optional[str] = Field(None, description="Tipo da rubrica (Vencimento, Desconto, etc.)")
    ativo: bool = Field(default=True, description="Rubrica ativa?")
    data_criacao: Optional[datetime] = Field(default_factory=datetime.now)
    data_atualizacao: Optional[datetime] = Field(default_factory=datetime.now)
    usuario_criacao: Optional[str] = None
    usuario_ultima_modificacao: Optional[str] = None

class RubricaMestreCreateSchema(RubricaMestreBaseSchema):
    pass

class RubricaMestreUpdateSchema(RubricaMestreBaseSchema):
    pass

class RubricaMestreResponseSchema(RubricaMestreBaseSchema):
    pass

# --- Rubricas Cliente (DicionarioRubricasCliente) ---
class RubricaClienteBaseSchema(BaseModel):
    id_rubrica_cliente: Optional[str] = None
    id_cliente: str
    id_rubrica_mestre_fk: Optional[str] = None
    codigo_rubrica_cliente: str
    descricao_cliente: str
    incide_inss_empregado: bool
    incide_inss_empresa: bool
    incide_inss_rat: bool
    incide_inss_terceiros: bool
    incide_irrf: bool
    incide_fgts_mensal: bool
    incide_fgts_rescisorio: bool
    eh_base_para_dsr: bool
    eh_base_para_medias_ferias: bool
    eh_base_para_medias_13: bool
    eh_base_para_outras_rubricas_config_ids: Optional[List[str]] = Field(default_factory=list, description="IDs de rubricas para as quais esta serve de base")
    config_incidencia_data_inicio_vigencia: date
    config_incidencia_data_fim_vigencia: Optional[date] = None
    id_cct_regra_especifica_fk: Optional[str] = None
    justificativa_config_incidencia: Optional[str] = None
    tipo_rubrica_cliente: Optional[str] = None
    irrf_tipo_rendimento: Optional[str] = None
    irrf_codigo_receita: Optional[str] = None
    fgts_percentual_se_diferente_padrao: Optional[float] = None
    eh_base_para_aviso_previo_indenizado: Optional[bool] = None
    eh_base_para_periculosidade_percentual: Optional[float] = None
    eh_base_para_insalubridade_grau: Optional[str] = None
    ativo: bool = Field(default=True)
    data_criacao_config: Optional[datetime] = Field(default_factory=datetime.now)
    usuario_criacao_config: Optional[str] = None
    data_modificacao_config: Optional[datetime] = Field(default_factory=datetime.now)
    usuario_modificacao_config: Optional[str] = None

class RubricaClienteConfigCreateSchema(RubricaClienteBaseSchema):
    pass

class RubricaClienteConfigUpdateSchema(RubricaClienteBaseSchema):
    pass

class RubricaClienteConfigResponseSchema(RubricaClienteBaseSchema):
    pass# Schemas para Dados Extraídos e Processados da Folha

class DocAIExtractedDataSchema(BaseModel):
    id_extracao: str
    id_item: str
    nome_arquivo_origem: Optional[str] = None
    pagina: Optional[int] = None
    tipo_campo: Optional[str] = None
    texto_extraido: Optional[str] = None
    valor_limpo: Optional[str] = None
    valor_numerico: Optional[float] = None
    confianca: Optional[float] = None
    timestamp_carga: datetime
    client_id: str

    class Config:
        from_attributes = True

class JobsProcessamentoFolhaSchema(BaseModel):
    id_job: str
    id_importacao: Optional[str] = None # Referência ao ID da importação original (ex: do controle)
    id_cliente: str
    periodo_referencia: date # YYYY-MM-DD (usar o 1º dia do mês)
    nome_arquivo_original: str
    gcs_uri_pdf_original: Optional[str] = None
    status_job: str # Ex: PENDENTE, PROCESSANDO, CONCLUIDO_SUCESSO, CONCLUIDO_ERROS, FALHA_CRITICA
    timestamp_criacao_job: datetime = Field(default_factory=datetime.now)
    timestamp_inicio_processamento: Optional[datetime] = None
    timestamp_fim_processamento: Optional[datetime] = None
    id_processador_docai_usado: Optional[str] = None
    versao_processador_docai_usado: Optional[str] = None
    detalhes_erro: Optional[str] = None # JSON string ou texto livre para detalhes de erro

    class Config:
        from_attributes = True

class FolhasProcessadasHeaderSchema(BaseModel):
    id_folha_processada: str # UUID ou ID gerado
    id_job_fk: str # FK para JobsProcessamentoFolha.id_job
    id_cliente: str
    periodo_referencia: date # YYYY-MM-DD (usar o 