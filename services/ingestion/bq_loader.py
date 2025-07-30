"""
BigQuery Data Loader for AUDITORIA360
Enhanced ingestion system with modular architecture.

This module provides backward compatibility by importing from the new modular structure.
For new code, import from src.bigquery directly.
"""

# Import all components from the new modular structure for backward compatibility
from src.bigquery.client import BigQueryClient, get_bigquery_client
from src.bigquery.loaders import ControleFolhaLoader, BaseLoader, EmployeeLoader, PayrollLoader
from src.bigquery.operations import DataOperations, load_data_to_bq
from src.bigquery.schema import SchemaManager

# Legacy function imports for backward compatibility
def ensure_dataset_exists(client, dataset_id: str, location: str = "US") -> bool:
    """Legacy function for backward compatibility"""
    schema_manager = SchemaManager(client)
    return schema_manager.create_dataset_if_not_exists(dataset_id, location)

def ensure_table_exists_or_updated(client, dataset_id: str, table_id: str, schema, description: str = None) -> bool:
    """Legacy function for backward compatibility"""
    schema_manager = SchemaManager(client)
    return schema_manager.create_table_if_not_exists(dataset_id, table_id, schema, description)

# Re-export all symbols for backward compatibility
__all__ = [
    # Client and connection management
    "BigQueryClient",
    "get_bigquery_client",
    
    # Loaders
    "ControleFolhaLoader", 
    "BaseLoader",
    "EmployeeLoader",
    "PayrollLoader",
    
    # Operations
    "DataOperations",
    "load_data_to_bq",
    
    # Schema management
    "SchemaManager",
    
    # Legacy functions
    "ensure_dataset_exists",
    "ensure_table_exists_or_updated",
]