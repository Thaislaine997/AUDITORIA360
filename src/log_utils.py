import csv
from datetime import datetime
import os
import logging
import sys

# Configuração básica do logger
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
    """Função que demonstra os diferentes níveis de log."""
    print(f"--- ID do logger DENTRO de demonstrar_logs: {id(logger)} ---") # LINHA DE DEBUG
    logger.debug("Este é um log de debug.")
    logger.info("Este é um log de informação.")
    logger.warning("Este é um log de aviso.")
    logger.error("Este é um log de erro.")
    logger.critical("Este é um log crítico.")

# Exemplo de uso (opcional, apenas para demonstrar)
if __name__ == "__main__":
    demonstrar_logs()
