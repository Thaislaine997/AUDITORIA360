# filepath: src/utils/docai_utils.py
import json
import logging
import uuid
import os
import sys
from datetime import datetime, timezone
from google.api_core.client_options import ClientOptions
from google.cloud import documentai, storage, bigquery
from google.oauth2 import service_account
from unittest.mock import MagicMock
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.utils.bq_loader import load_data_to_bigquery, get_bigquery_client

# ...restante do código igual ao src/docai_utils.py...
