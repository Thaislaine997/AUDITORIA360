"""
Specialized data loaders for specific business domains
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google.cloud import bigquery

from .client import BigQueryClient
from .schema import SchemaManager
from .operations import DataOperations

logger = logging.getLogger(__name__)


class BaseLoader:
    """Base class for all BigQuery data loaders"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.bq_client = BigQueryClient(config)
        
        if not self.bq_client.client:
            raise ValueError("Failed to initialize BigQuery client")
        
        self.schema_manager = SchemaManager(self.bq_client.client)
        self.data_operations = DataOperations(self.bq_client.client)
        self.dataset_id = config.get("dataset_id", "auditoria360")
    
    def ensure_infrastructure(self) -> bool:
        """Ensure dataset and tables exist"""
        # Create dataset if it doesn't exist
        if not self.schema_manager.create_dataset_if_not_exists(self.dataset_id):
            return False
        
        # Create tables - to be implemented by subclasses
        return self._create_tables()
    
    def _create_tables(self) -> bool:
        """Create required tables - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement _create_tables")


class ControleFolhaLoader(BaseLoader):
    """Loader for payroll control data (controle de folha)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.table_id = "controle_folha"
        self._client_id = config.get("client_id")
    
    @property
    def client_id(self):
        """Get the current client ID"""
        return self._client_id
    
    @client_id.setter
    def client_id(self, value):
        """Set the client ID"""
        self._client_id = value
    
    def _create_tables(self) -> bool:
        """Create controle_folha table"""
        schema = self.schema_manager.get_controle_folha_schema()
        return self.schema_manager.create_table_if_not_exists(
            self.dataset_id,
            self.table_id,
            schema,
            "Payroll control data for AUDITORIA360"
        )
    
    def inserir_folha(
        self,
        cnpj: str,
        nome_empresa: str,
        mes_referencia: int,
        ano_referencia: int,
        qtd_funcionarios: int,
        total_proventos: float,
        total_descontos: float,
        total_liquido: float,
        observacoes: str = "",
        usuario_responsavel: str = "",
        inss_empresa: float = 0.0,
        fgts_empresa: float = 0.0,
        **kwargs
    ) -> Optional[str]:
        """Insert payroll data into BigQuery"""
        try:
            # Ensure infrastructure exists
            if not self.ensure_infrastructure():
                logger.error("Failed to ensure BigQuery infrastructure")
                return None
            
            # Generate unique ID
            record_id = str(uuid.uuid4())
            current_time = datetime.now(timezone.utc)
            
            # Prepare data
            data = {
                "id": record_id,
                "cnpj": cnpj,
                "nome_empresa": nome_empresa,
                "mes_referencia": mes_referencia,
                "ano_referencia": ano_referencia,
                "qtd_funcionarios": qtd_funcionarios,
                "total_proventos": total_proventos,
                "total_descontos": total_descontos,
                "total_liquido": total_liquido,
                "observacoes": observacoes,
                "data_processamento": current_time.isoformat(),
                "status": "PROCESSADO",
                "usuario_responsavel": usuario_responsavel,
                "inss_empresa": inss_empresa,
                "fgts_empresa": fgts_empresa,
                "created_at": current_time.isoformat(),
                "updated_at": current_time.isoformat(),
                "empresa_id": self.client_id or cnpj,  # Use client_id or fallback to CNPJ
            }
            
            # Add any additional fields from kwargs
            data.update(kwargs)
            
            # Insert data
            success = self.data_operations.insert_rows(
                self.dataset_id, 
                self.table_id, 
                [data]
            )
            
            if success:
                logger.info(f"Payroll data inserted successfully with ID: {record_id}")
                return record_id
            else:
                logger.error("Failed to insert payroll data")
                return None
                
        except Exception as e:
            logger.error(f"Error inserting payroll data: {e}", exc_info=True)
            return None
    
    def atualizar_status_folha(self, registro_id: str, novo_status: str) -> bool:
        """Update payroll record status"""
        try:
            update_query = f"""
                UPDATE `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
                SET status = @novo_status, updated_at = @updated_at
                WHERE id = @registro_id
            """
            
            query_parameters = [
                bigquery.ScalarQueryParameter("novo_status", "STRING", novo_status),
                bigquery.ScalarQueryParameter("updated_at", "TIMESTAMP", datetime.now(timezone.utc)),
                bigquery.ScalarQueryParameter("registro_id", "STRING", registro_id),
            ]
            
            return self.data_operations.update_rows(
                self.dataset_id,
                self.table_id,
                update_query,
                query_parameters
            )
            
        except Exception as e:
            logger.error(f"Error updating payroll status: {e}")
            return False
    
    def listar_todas_as_empresas(self) -> List[Dict[str, Any]]:
        """List all companies in the system"""
        try:
            query = f"""
                SELECT DISTINCT cnpj, nome_empresa, empresa_id
                FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
                ORDER BY nome_empresa
            """
            
            results = self.data_operations.query_data(query)
            return results or []
            
        except Exception as e:
            logger.error(f"Error listing companies: {e}")
            return []
    
    def get_empresa_by_cnpj(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """Get company information by CNPJ"""
        try:
            query = f"""
                SELECT DISTINCT cnpj, nome_empresa, empresa_id
                FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
                WHERE cnpj = @cnpj
                LIMIT 1
            """
            
            from google.cloud import bigquery
            query_parameters = [
                bigquery.ScalarQueryParameter("cnpj", "STRING", cnpj)
            ]
            
            results = self.data_operations.query_data(query, query_parameters)
            return results[0] if results else None
            
        except Exception as e:
            logger.error(f"Error getting company by CNPJ: {e}")
            return None
    
    def get_payroll_summary(
        self, 
        ano: Optional[int] = None, 
        mes: Optional[int] = None,
        cnpj: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get payroll summary with optional filters"""
        try:
            conditions = []
            parameters = []
            
            if ano:
                conditions.append("ano_referencia = @ano")
                from google.cloud import bigquery
                parameters.append(bigquery.ScalarQueryParameter("ano", "INTEGER", ano))
            
            if mes:
                conditions.append("mes_referencia = @mes")
                from google.cloud import bigquery
                parameters.append(bigquery.ScalarQueryParameter("mes", "INTEGER", mes))
            
            if cnpj:
                conditions.append("cnpj = @cnpj")
                from google.cloud import bigquery
                parameters.append(bigquery.ScalarQueryParameter("cnpj", "STRING", cnpj))
            
            # Add tenant filtering if client_id is set
            if self.client_id:
                conditions.append("empresa_id = @empresa_id")
                from google.cloud import bigquery
                parameters.append(bigquery.ScalarQueryParameter("empresa_id", "STRING", self.client_id))
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            query = f"""
                SELECT 
                    cnpj,
                    nome_empresa,
                    mes_referencia,
                    ano_referencia,
                    qtd_funcionarios,
                    total_proventos,
                    total_descontos,
                    total_liquido,
                    status,
                    data_processamento
                FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
                WHERE {where_clause}
                ORDER BY ano_referencia DESC, mes_referencia DESC, nome_empresa
            """
            
            results = self.data_operations.query_data(query, parameters)
            return results or []
            
        except Exception as e:
            logger.error(f"Error getting payroll summary: {e}")
            return []


class EmployeeLoader(BaseLoader):
    """Loader for employee data"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.table_id = "employees"
    
    def _create_tables(self) -> bool:
        """Create employees table"""
        schema = self.schema_manager.get_employees_schema()
        return self.schema_manager.create_table_if_not_exists(
            self.dataset_id,
            self.table_id,
            schema,
            "Employee data for AUDITORIA360"
        )


class PayrollLoader(BaseLoader):
    """Loader for detailed payroll data"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.table_id = "payroll"
    
    def _create_tables(self) -> bool:
        """Create payroll table"""
        schema = self.schema_manager.get_payroll_schema()
        return self.schema_manager.create_table_if_not_exists(
            self.dataset_id,
            self.table_id,
            schema,
            "Detailed payroll data for AUDITORIA360"
        )