"""
BigQuery integration module for AUDITORIA360
Provides modular BigQuery client management, schema handling, and data operations
"""

from .client import BigQueryClient, get_bigquery_client
from .schema import SchemaManager
from .operations import DataOperations
from .loaders import ControleFolhaLoader

__all__ = [
    "BigQueryClient",
    "get_bigquery_client", 
    "SchemaManager",
    "DataOperations",
    "ControleFolhaLoader"
]