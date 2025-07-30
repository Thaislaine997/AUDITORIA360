"""
BigQuery schema management and table structure definitions
"""

import logging
from typing import Any, Dict, List, Optional

from google.cloud import bigquery

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages BigQuery schemas and table structures"""
    
    def __init__(self, client: bigquery.Client):
        self.client = client
    
    def get_controle_folha_schema(self) -> List[bigquery.SchemaField]:
        """Get schema for controle_folha table"""
        return [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("cnpj", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("nome_empresa", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("mes_referencia", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ano_referencia", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("qtd_funcionarios", "INTEGER"),
            bigquery.SchemaField("total_proventos", "FLOAT"),
            bigquery.SchemaField("total_descontos", "FLOAT"),
            bigquery.SchemaField("total_liquido", "FLOAT"),
            bigquery.SchemaField("observacoes", "STRING"),
            bigquery.SchemaField("data_processamento", "TIMESTAMP"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("usuario_responsavel", "STRING"),
            bigquery.SchemaField("inss_empresa", "FLOAT"),
            bigquery.SchemaField("fgts_empresa", "FLOAT"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
            # Additional fields for enhanced tracking
            bigquery.SchemaField("empresa_id", "STRING"),  # For multi-tenant support
            bigquery.SchemaField("periodo_inicio", "DATE"),
            bigquery.SchemaField("periodo_fim", "DATE"),
            bigquery.SchemaField("total_funcionarios_ativos", "INTEGER"),
            bigquery.SchemaField("total_funcionarios_demitidos", "INTEGER"),
            bigquery.SchemaField("total_funcionarios_admitidos", "INTEGER"),
            bigquery.SchemaField("versao_schema", "STRING"),
            bigquery.SchemaField("metadata", "JSON"),
        ]
    
    def get_employees_schema(self) -> List[bigquery.SchemaField]:
        """Get schema for employees table"""
        return [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("empresa_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("employee_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("cpf", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("email", "STRING"),
            bigquery.SchemaField("phone", "STRING"),
            bigquery.SchemaField("department", "STRING"),
            bigquery.SchemaField("position", "STRING"),
            bigquery.SchemaField("salary", "FLOAT"),
            bigquery.SchemaField("hire_date", "DATE"),
            bigquery.SchemaField("termination_date", "DATE"),
            bigquery.SchemaField("is_active", "BOOLEAN"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]
    
    def get_payroll_schema(self) -> List[bigquery.SchemaField]:
        """Get schema for payroll table"""
        return [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("empresa_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("employee_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("competencia_mes", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("competencia_ano", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("salario_base", "FLOAT"),
            bigquery.SchemaField("total_proventos", "FLOAT"),
            bigquery.SchemaField("total_descontos", "FLOAT"),
            bigquery.SchemaField("total_liquido", "FLOAT"),
            bigquery.SchemaField("inss_funcionario", "FLOAT"),
            bigquery.SchemaField("ir_funcionario", "FLOAT"),
            bigquery.SchemaField("fgts_funcionario", "FLOAT"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]
    
    def create_dataset_if_not_exists(self, dataset_id: str, location: str = "US") -> bool:
        """Create dataset if it doesn't exist"""
        try:
            full_dataset_id = f"{self.client.project}.{dataset_id}"
            
            # Check if dataset exists
            try:
                self.client.get_dataset(full_dataset_id)
                logger.info(f"Dataset {dataset_id} already exists")
                return True
            except Exception:
                # Dataset doesn't exist, create it
                logger.info(f"Creating dataset {dataset_id}")
                
                dataset = bigquery.Dataset(full_dataset_id)
                dataset.location = location
                dataset.description = f"AUDITORIA360 dataset: {dataset_id}"
                
                dataset = self.client.create_dataset(dataset, timeout=30)
                logger.info(f"Dataset {dataset_id} created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating dataset {dataset_id}: {e}")
            return False
    
    def create_table_if_not_exists(
        self, 
        dataset_id: str, 
        table_id: str, 
        schema: List[bigquery.SchemaField],
        description: Optional[str] = None
    ) -> bool:
        """Create table if it doesn't exist"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            
            # Check if table exists
            try:
                self.client.get_table(full_table_id)
                logger.info(f"Table {table_id} already exists")
                return True
            except Exception:
                # Table doesn't exist, create it
                logger.info(f"Creating table {table_id}")
                
                table = bigquery.Table(full_table_id, schema=schema)
                if description:
                    table.description = description
                
                table = self.client.create_table(table)
                logger.info(f"Table {table_id} created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating table {table_id}: {e}")
            return False
    
    def update_table_schema(
        self, 
        dataset_id: str, 
        table_id: str, 
        new_schema: List[bigquery.SchemaField]
    ) -> bool:
        """Update table schema (only allows adding new fields)"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            
            table = self.client.get_table(full_table_id)
            original_schema = table.schema
            
            # Update the schema
            table.schema = new_schema
            table = self.client.update_table(table, ["schema"])
            
            logger.info(f"Table {table_id} schema updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating table schema for {table_id}: {e}")
            return False
    
    def get_table_info(self, dataset_id: str, table_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a table"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            table = self.client.get_table(full_table_id)
            
            return {
                "table_id": table.table_id,
                "dataset_id": table.dataset_id,
                "project": table.project,
                "num_rows": table.num_rows,
                "num_bytes": table.num_bytes,
                "created": table.created,
                "modified": table.modified,
                "description": table.description,
                "schema_fields": len(table.schema),
                "location": table.location,
            }
            
        except Exception as e:
            logger.error(f"Error getting table info for {table_id}: {e}")
            return None