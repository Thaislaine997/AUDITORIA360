import json
import logging
import os
import uuid
from datetime import datetime, timezone, date
from google.cloud import bigquery
from google.oauth2 import service_account
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError
import pandas as pd
from typing import Optional, List, Dict, Any
import unittest.mock

# Exportação explícita dos símbolos principais
__all__ = [
    'get_bigquery_client',
    'ControleFolhaLoader',
    'load_data_to_bigquery',
    'create_dataset_if_not_exists',
    'create_or_update_table',
]

# ...schemas e funções do src/bq_loader.py...
