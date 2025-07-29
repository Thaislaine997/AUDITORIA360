
"""
Logging utilities for AUDITORIA360
Provides centralized logging configuration and functionality.
"""

import csv
from datetime import datetime
import os
import logging
import sys
from typing import Optional

def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Set up logging configuration."""
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )
    
    return logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)

# Default logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

LOG_FILE = "logs.csv"

def registrar_log(usuario, acao, ip=None, empresa=None, competencia=None):
    """Register activity log entry."""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "usuario": usuario,
        "acao": acao,
        "ip": ip or "",
        "empresa": empresa or "",
        "competencia": competencia or ""
    }
    write_header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=log_data.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(log_data)

def demonstrar_logs():
    """Demonstrate logging functionality."""
    print(f"--- ID do logger DENTRO de demonstrar_logs: {id(logger)} ---")
    logger.debug("Este é um log de debug.")
    logger.info("Este é um log de informação.")
    logger.warning("Este é um log de aviso.")
    logger.error("Este é um log de erro.")
    logger.critical("Este é um log crítico.")

if __name__ == "__main__":
    demonstrar_logs()
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=log_data.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(log_data)

def demonstrar_logs():
    print(f"--- ID do logger DENTRO de demonstrar_logs: {id(logger)} ---")
    logger.debug("Este é um log de debug.")
    logger.info("Este é um log de informação.")
    logger.warning("Este é um log de aviso.")
    logger.error("Este é um log de erro.")
    logger.critical("Este é um log crítico.")

if __name__ == "__main__":
    demonstrar_logs()
