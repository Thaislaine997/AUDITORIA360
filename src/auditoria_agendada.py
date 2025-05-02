from pathlib import Path
from datetime import datetime

PASTA = r'C:\DPEIXER\AUDITORIAS\2025\05'

def executar_auditoria_mensal():
    for file in Path(PASTA).glob("*.pdf"):
        print(f"[{datetime.now()}] Processando: {file.name}")
        # Aqui entraria o processamento com DocAI

if __name__ == "__main__":
    executar_auditoria_mensal()
