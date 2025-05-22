# filepath: src/models.py
from dataclasses import dataclass, field
from typing import Optional

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

# Você pode adicionar mais classes de modelo aqui conforme seu projeto evolui.
# Por exemplo, um modelo para representar a configuração da aplicação, etc.
