import streamlit as st
import sys
import os
from services.core.log_utils import logger # Corrigido caminho do logger

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

# Import centralized authentication utilities
from src.utils.auth import (
    get_api_token,
    get_auth_headers, 
    get_current_client_id,
    handle_api_error,
    display_user_info_sidebar
)

# Re-export for backward compatibility with existing dashboard pages
__all__ = [
    'get_api_token',
    'get_auth_headers', 
    'get_current_client_id',
    'handle_api_error',
    'display_user_info_sidebar'
]
