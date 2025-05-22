# filepath: src/schemas.py
# Este arquivo pode ser usado para definir Pydantic models para validação de dados,
# ou outros tipos de schemas usados na aplicação.

from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

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