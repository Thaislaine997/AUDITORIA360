"""
Script de automação para busca diária de legislação.
"""
import datetime
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)

DATA_DIR = "data/updates"
os.makedirs(DATA_DIR, exist_ok=True)

# Função principal de busca
def buscar_legislacao():
    hoje = datetime.date.today()
    logging.info(f"Buscando legislação em {hoje}")
    url = "https://api.legislacao.gov.br/hoje"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        file_path = os.path.join(DATA_DIR, f"{hoje}.json")
        with open(file_path, "w") as f:
            f.write(resp.text)
        logging.info(f"Legislação salva em {file_path}")
    except Exception as e:
        logging.error(f"Erro ao buscar legislação: {e}")

if __name__ == "__main__":
    buscar_legislacao()
