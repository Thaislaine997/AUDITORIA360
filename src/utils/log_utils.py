import csv
import os
from datetime import datetime

LOG_FILE = "app.log"

def registrar_log(usuario, acao, ip, empresa, competencia):
    log_data = {
        "data_hora": datetime.now().isoformat(),
        "usuario": usuario,
        "acao": acao,
        "ip": ip,
        "empresa": empresa,
        "competencia": competencia
    }
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=log_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_data)

def demonstrar_logs():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()