"""
BigQuery client management and connection handling
"""

import logging
import os
from typing import Any, Dict, Optional

from google.cloud import bigquery
from google.cloud import exceptions as google_exceptions
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class BigQueryClient:
    """Manages BigQuery client connections and configuration"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._client = None
        self._project_id = None
    
    @property
    def client(self) -> Optional[bigquery.Client]:
        """Get or create BigQuery client"""
        if self._client is None:
            self._client = self._create_client()
        return self._client
    
    @property 
    def project_id(self) -> Optional[str]:
        """Get the project ID for the current client"""
        if self.client:
            return self.client.project
        return None
    
    def _create_client(self) -> Optional[bigquery.Client]:
        """Create and configure BigQuery client"""
        try:
            credentials = None
            project_id_from_config = self.config.get("GCP_PROJECT_ID")

            # Handle service account file
            if self.config.get("GCP_SERVICE_ACCOUNT_FILE"):
                credentials_path = self.config["GCP_SERVICE_ACCOUNT_FILE"]
                if os.path.exists(credentials_path):
                    logger.info(f"Using service account file: {credentials_path}")
                    credentials = service_account.Credentials.from_service_account_file(
                        credentials_path
                    )
                    # Use project from credentials if not specified in config
                    project_id_from_config = (
                        project_id_from_config or credentials.project_id
                    )
                else:
                    logger.error(f"Service account file not found: {credentials_path}")
                    return None

            # Build client arguments
            client_kwargs: Dict[str, Any] = {}
            if credentials:
                client_kwargs["credentials"] = credentials
            if project_id_from_config:
                client_kwargs["project"] = project_id_from_config
                logger.info(f"Using project ID: {project_id_from_config}")
            else:
                logger.info("Using default environment credentials and project")

            client = bigquery.Client(**client_kwargs)

            # Validate client setup
            if client.project:
                logger.info(f"BigQuery client initialized successfully. Project: {client.project}")
            else:
                logger.warning(
                    "BigQuery client initialized but project not determined. "
                    "Operations requiring explicit project may fail."
                )
            
            return client

        except google_exceptions.GoogleCloudError as e:
            logger.error(f"Google Cloud error initializing BigQuery client: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Generic error initializing BigQuery client: {e}", exc_info=True)
            return None
    
    def test_connection(self) -> bool:
        """Test BigQuery connection by running a simple query"""
        try:
            if not self.client:
                return False
            
            # Run a simple query to test connection
            query = "SELECT 1 as test"
            query_job = self.client.query(query)
            results = list(query_job.result())
            return len(results) == 1 and results[0].test == 1
            
        except Exception as e:
            logger.error(f"BigQuery connection test failed: {e}")
            return False
    
    def close(self):
        """Close the client connection"""
        if self._client:
            self._client.close()
            self._client = None


def get_bigquery_client(config: Optional[Dict[str, Any]] = None) -> Optional[bigquery.Client]:
    """
    Legacy function for backward compatibility.
    Creates and returns a BigQuery client.
    """
    bq_client = BigQueryClient(config)
    return bq_client.client