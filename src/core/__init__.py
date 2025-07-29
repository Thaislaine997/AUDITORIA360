"""
Core module for AUDITORIA360
Contains fundamental system components, configuration, and base functionality.
"""

from .config_manager import ConfigManager
from .validators import (
    validate_cpf,
    validate_cnpj,
    validate_email,
    validate_phone,
    DataValidator
)
from .log_utils import setup_logging, get_logger

__all__ = [
    'ConfigManager',
    'validate_cpf',
    'validate_cnpj', 
    'validate_email',
    'validate_phone',
    'DataValidator',
    'setup_logging',
    'get_logger'
]