# filepath: src/models.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import date, datetime # Adicionado para os novos models

@dataclass
class BigQueryRow:
    """
    Representa uma linha de dados a ser inserida na tabela do BigQuery.
    Este schema deve corresponder à sua tabela docai_extracted_data.
    """
    id_extracao: str
    id_item: str
    nome_arquivo_origem: str
    tipo_campo: str
    texto_extraido: str
    confianca: float
    pagina: Optional[int] = None  # Opcional, pode não estar sempre presente
    valor_limpo: Optional[str] = None # Opcional, pode ser derivado
    valor_numerico: Optional[float] = None # Opcional, pode ser derivado
    # timestamp_carga geralmente é adicionado no momento da inserção ou pelo BigQuery

@dataclass
class ExtractedEntity:
    """
    Representa uma entidade genérica extraída pelo Document AI antes de ser
    formatada para o BigQuery.
    """
    entity_type: str
    mention_text: str
    confidence: float
    page_number: Optional[int] = None
    # Você pode adicionar outros campos conforme necessário, como bounding_boxes, etc.

@dataclass
class Auditoria:
    """
    Representa uma auditoria de folha de pagamento.
    """
    id_auditoria: str
    id_folha: str
    id_regra: Optional[str] = None
    tipo_divergencia: Optional[str] = None
    mensagem_auditoria: Optional[str] = None
    status_auditoria: Optional[str] = None
    data_auditoria: Optional[datetime] = field(default_factory=datetime.now)
    client_id: Optional[str] = None # Adicionado para consistência

@dataclass
class Empresa:
    """
    Representa uma empresa cliente.
    Baseado em ControleMensalEmpresaSchema e uso em empresas_routes.py
    """
    empresa_id: str # Geralmente o ID principal
    client_id: Optional[str] = None # ID do cliente ao qual a empresa pertence
    nome_empresa: Optional[str] = None # Adicionado campo comum
    cnpj_empresa: Optional[str] = None # Adicionado campo comum
    
    # Campos de ControleMensalEmpresaSchema que parecem relevantes para um modelo Empresa geral
    ano_referencia: Optional[int] = None
    mes_referencia: Optional[int] = None
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
    data_criacao_registro: Optional[datetime] = field(default_factory=datetime.now)
    data_ultima_modificacao: Optional[datetime] = field(default_factory=datetime.now)
    # Adicione outros campos conforme necessário, por exemplo, de Tabela_Empresas se existir

@dataclass
class Usuario:
    """
    Representa um usuário do sistema.
    Estrutura básica, pode ser expandida conforme necessidade.
    """
    id_usuario: str
    nome_usuario: Optional[str] = None
    email: Optional[str] = None
    client_id: Optional[str] = None # Se usuários são vinculados a clientes
    roles: list[str] = field(default_factory=list) # Ex: ["admin", "auditor"]
    ativo: bool = True

# Você pode adicionar mais classes de modelo aqui conforme seu projeto evolui.
