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

    class Config:
        from_attributes = True