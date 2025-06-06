# src/utils/bq_executor.py
from google.cloud import bigquery
import pandas as pd
from typing import List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BQExecutor:
    def __init__(self, bq_client: bigquery.Client, project_id: str, dataset_id: str):
        self.client = bq_client
        self.project_id = project_id
        self.dataset_id = dataset_id # Este é o dataset específico para as tabelas de auditoria da folha

    def execute_query_to_dataframe(self, query_template: str, query_params: Optional[List[bigquery.ScalarQueryParameter]] = None) -> pd.DataFrame:
        """
        Executa uma query no BigQuery e retorna um DataFrame Pandas.
        Substitui o placeholder 'auditoria_folha_dataset' na query pelo 
        dataset real configurado para o cliente.
        """
        
        # Constrói o nome completo do dataset no formato `projeto.dataset`
        # As queries usam "auditoria_folha_dataset.NomeTabela"
        # Isso será substituído por "`meu-projeto.dataset_do_cliente`.NomeTabela"
        fully_qualified_dataset_placeholder = f"`{self.project_id}.{self.dataset_id}`"
        
        final_query = query_template.replace("auditoria_folha_dataset", fully_qualified_dataset_placeholder)
        
        job_config = bigquery.QueryJobConfig()
        if query_params:
            job_config.query_parameters = query_params

        try:
            logger.info(f"Executando query no BigQuery. Projeto: {self.project_id}, Dataset: {self.dataset_id}")
            logger.debug(f"Query final: {final_query} com params: {query_params}")
            query_job = self.client.query(final_query, job_config=job_config)
            results_df = query_job.to_dataframe()
            logger.info(f"Query executada com sucesso. {len(results_df)} linhas retornadas.")
            return results_df
        except Exception as e:
            logger.error(f"Erro ao executar query no BigQuery (Projeto: {self.project_id}, Dataset: {self.dataset_id}): {e}", exc_info=True)
            # Considerar se deve levantar uma exceção customizada ou propagar a original
            raise
