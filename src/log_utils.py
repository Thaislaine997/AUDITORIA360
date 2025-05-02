import csv
from datetime import datetime
import os

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
