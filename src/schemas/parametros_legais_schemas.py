# Modelos para integração contabilidade
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class RegistroContabilidadePayload(BaseModel):
    id_empresa: str
    periodo: str
    dados_contabeis: dict
    usuario_email: EmailStr


class RegistroContabilidadeResponse(BaseModel):
    id_registro: str
    status: str
    mensagem: Optional[str] = None


class ContabilidadeResponse(BaseModel):
    id_contabilidade: str
    cnpj: str
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    data_cadastro: Optional[str] = None
    data_atualizacao: Optional[str] = None
    ativo: bool = True
    nome: Optional[str] = None
    email: Optional[EmailStr] = None


class UsuarioContabilidadeResponse(BaseModel):
    id_usuario_contabilidade: str
    id_contabilidade: Optional[str] = None
    email: EmailStr
    nome_usuario: Optional[str] = None
    cargo: Optional[str] = None
    data_criacao: Optional[str] = None
    data_ultimo_login: Optional[str] = None
    ativo: bool = True


class EmpresaClienteSimplificado(BaseModel):
    id_empresa_cliente: Optional[str] = None
    cnpj_empresa: Optional[str] = None
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    ativo: Optional[bool] = None


"""
Schemas de parâmetros legais: salário mínimo, família, FGTS, IRRF, INSS.
"""


class TabelaSalarioMinimo(BaseModel):
    ano: int
    valor: float
    id_versao: str = ""
    data_criacao_registro: Optional[str] = None
    data_ultima_modificacao: Optional[str] = None
    data_inativacao: Optional[str] = None
    data_inicio_vigencia: Optional[str] = None
    data_fim_vigencia: Optional[str] = None


class TabelaSalarioFamilia(BaseModel):
    ano: int
    faixa: str
    valor: float
    id_versao: str = ""
    data_criacao_registro: Optional[str] = None
    data_ultima_modificacao: Optional[str] = None
    data_inativacao: Optional[str] = None
    data_inicio_vigencia: Optional[str] = None
    data_fim_vigencia: Optional[str] = None


class TabelaFGTS(BaseModel):
    ano: int
    aliquota: float
    id_versao: str = ""
    data_criacao_registro: Optional[str] = None
    data_ultima_modificacao: Optional[str] = None
    data_inativacao: Optional[str] = None
    data_inicio_vigencia: Optional[str] = None
    data_fim_vigencia: Optional[str] = None


class TabelaIRRF(BaseModel):
    ano: int
    faixas: list
    id_versao: str = ""
    data_criacao_registro: Optional[str] = None
    data_ultima_modificacao: Optional[str] = None
    data_inativacao: Optional[str] = None
    data_inicio_vigencia: Optional[str] = None
    data_fim_vigencia: Optional[str] = None


class FaixaIRRF(BaseModel):
    faixa: str
    valor: float


class TabelaINSS(BaseModel):
    ano: int
    faixas: list
    id_versao: str = ""
    data_criacao_registro: Optional[str] = None
    data_ultima_modificacao: Optional[str] = None
    data_inativacao: Optional[str] = None
    data_inicio_vigencia: Optional[str] = None
    data_fim_vigencia: Optional[str] = None


# Payloads e Responses para integração
class SugestaoAtualizacaoParametros(BaseModel):
    id_parametro: str
    sugestao: str
    justificativa: Optional[str] = None


class AprovarSugestaoPayload(BaseModel):
    id_sugestao: str
    aprovado_por: str
    comentario: Optional[str] = None


class RejeitarSugestaoPayload(BaseModel):
    id_sugestao: str
    rejeitado_por: str
    motivo: Optional[str] = None


class FaixaINSS(BaseModel):
    faixa: str
    valor: float
