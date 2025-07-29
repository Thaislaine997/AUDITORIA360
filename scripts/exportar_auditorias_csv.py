import csv
import os

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1/auditorias/")
CLIENT_ID = os.getenv("CLIENT_ID", "cliente_a")
OUTPUT = "auditorias_export.csv"

headers = {"x-client-id": CLIENT_ID}
resp = requests.get(API_URL, headers=headers)
resp.raise_for_status()
data = resp.json().get("items", [])

if not data:
    print("Nenhuma auditoria encontrada para exportação.")
    exit(0)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print(f"Exportação concluída: {OUTPUT}")
