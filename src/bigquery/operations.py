"""
BigQuery data operations - loading, inserting, updating, and querying data
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

from google.cloud import bigquery

logger = logging.getLogger(__name__)


class DataOperations:
    """Handles BigQuery data operations"""
    
    def __init__(self, client: bigquery.Client):
        self.client = client
    
    def insert_rows(
        self, 
        dataset_id: str, 
        table_id: str, 
        rows: List[Dict[str, Any]],
        ignore_unknown_values: bool = False
    ) -> bool:
        """Insert rows into a BigQuery table"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            table = self.client.get_table(full_table_id)
            
            errors = self.client.insert_rows_json(
                table, 
                rows, 
                ignore_unknown_values=ignore_unknown_values
            )
            
            if errors:
                logger.error(f"Errors inserting rows into {table_id}: {errors}")
                return False
            
            logger.info(f"Successfully inserted {len(rows)} rows into {table_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting rows into {table_id}: {e}")
            return False
    
    def load_data_from_file(
        self,
        dataset_id: str,
        table_id: str,
        source_file_path: str,
        file_format: str = "CSV",
        write_disposition: str = "WRITE_APPEND",
        skip_leading_rows: int = 1
    ) -> bool:
        """Load data from a file into BigQuery table"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            
            job_config = bigquery.LoadJobConfig()
            job_config.write_disposition = write_disposition
            
            if file_format.upper() == "CSV":
                job_config.source_format = bigquery.SourceFormat.CSV
                job_config.skip_leading_rows = skip_leading_rows
                job_config.autodetect = True
            elif file_format.upper() == "JSON":
                job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
                job_config.autodetect = True
            
            with open(source_file_path, "rb") as source_file:
                load_job = self.client.load_table_from_file(
                    source_file, full_table_id, job_config=job_config
                )
            
            load_job.result()  # Wait for job to complete
            
            logger.info(f"Successfully loaded data from {source_file_path} into {table_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data from file {source_file_path}: {e}")
            return False
    
    def update_rows(
        self,
        dataset_id: str,
        table_id: str, 
        update_query: str,
        query_parameters: Optional[List] = None
    ) -> bool:
        """Update rows using a SQL query"""
        try:
            job_config = bigquery.QueryJobConfig()
            if query_parameters:
                job_config.query_parameters = query_parameters
            
            query_job = self.client.query(update_query, job_config=job_config)
            query_job.result()  # Wait for job to complete
            
            logger.info(f"Successfully updated rows in {table_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating rows in {table_id}: {e}")
            return False
    
    def delete_rows(
        self,
        dataset_id: str,
        table_id: str,
        where_clause: str,
        query_parameters: Optional[List] = None
    ) -> bool:
        """Delete rows using a WHERE clause"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            delete_query = f"DELETE FROM `{full_table_id}` WHERE {where_clause}"
            
            job_config = bigquery.QueryJobConfig()
            if query_parameters:
                job_config.query_parameters = query_parameters
            
            query_job = self.client.query(delete_query, job_config=job_config)
            query_job.result()  # Wait for job to complete
            
            logger.info(f"Successfully deleted rows from {table_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting rows from {table_id}: {e}")
            return False
    
    def query_data(
        self,
        query: str,
        query_parameters: Optional[List] = None,
        max_results: Optional[int] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a query and return results"""
        try:
            job_config = bigquery.QueryJobConfig()
            if query_parameters:
                job_config.query_parameters = query_parameters
            
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result(max_results=max_results)
            
            # Convert results to list of dictionaries
            rows = []
            for row in results:
                rows.append(dict(row))
            
            logger.info(f"Query executed successfully, returned {len(rows)} rows")
            return rows
            
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None
    
    def get_table_row_count(self, dataset_id: str, table_id: str) -> Optional[int]:
        """Get the number of rows in a table"""
        try:
            query = f"""
                SELECT COUNT(*) as row_count 
                FROM `{self.client.project}.{dataset_id}.{table_id}`
            """
            
            results = self.query_data(query)
            if results and len(results) > 0:
                return results[0]["row_count"]
            return None
            
        except Exception as e:
            logger.error(f"Error getting row count for {table_id}: {e}")
            return None
    
    def check_table_exists(self, dataset_id: str, table_id: str) -> bool:
        """Check if a table exists"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            self.client.get_table(full_table_id)
            return True
        except Exception:
            return False
    
    def get_distinct_values(
        self, 
        dataset_id: str, 
        table_id: str, 
        column_name: str,
        where_clause: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Optional[List[Any]]:
        """Get distinct values from a column"""
        try:
            full_table_id = f"{self.client.project}.{dataset_id}.{table_id}"
            
            query = f"SELECT DISTINCT {column_name} FROM `{full_table_id}`"
            
            if where_clause:
                query += f" WHERE {where_clause}"
            
            query += f" ORDER BY {column_name}"
            
            if limit:
                query += f" LIMIT {limit}"
            
            results = self.query_data(query)
            if results:
                return [row[column_name] for row in results]
            return []
            
        except Exception as e:
            logger.error(f"Error getting distinct values from {column_name}: {e}")
            return None
    
    def backup_table(
        self, 
        source_dataset_id: str, 
        source_table_id: str,
        backup_dataset_id: str, 
        backup_table_id: Optional[str] = None
    ) -> bool:
        """Create a backup copy of a table"""
        try:
            if not backup_table_id:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_table_id = f"{source_table_id}_backup_{timestamp}"
            
            source_table_ref = f"{self.client.project}.{source_dataset_id}.{source_table_id}"
            backup_table_ref = f"{self.client.project}.{backup_dataset_id}.{backup_table_id}"
            
            query = f"""
                CREATE OR REPLACE TABLE `{backup_table_ref}` 
                AS SELECT * FROM `{source_table_ref}`
            """
            
            query_job = self.client.query(query)
            query_job.result()  # Wait for job to complete
            
            logger.info(f"Successfully backed up {source_table_id} to {backup_table_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up table {source_table_id}: {e}")
            return False


def load_data_to_bq(
    client: bigquery.Client,
    data: Sequence[Dict[str, Any]],
    dataset_id: str,
    table_id: str,
    **kwargs
) -> bool:
    """
    Legacy function for backward compatibility.
    Load data to BigQuery table.
    """
    operations = DataOperations(client)
    return operations.insert_rows(dataset_id, table_id, list(data), **kwargs)