import os
import time
from pathlib import Path
from datetime import datetime
# Supondo que as funções abaixo estejam implementadas
# from src.docai_utils import processar_pdf_documentai
# from src.email_utils import enviar_email_com_pdf
# from src.chat_utils import enviar_mensagem_chat

PASTA = r'C:\DPEIXER\AUDITORIAS\2025\05'
DESTINATARIO = 'contato@dpeixerassessoria.com.br'

def executar_auditoria_mensal():
    for file in Path(PASTA).glob("*.pdf"):
        print(f"[{datetime.now()}] Processando: {file.name}")
        with open(file, "rb") as f:
            pass  # Placeholder para processamento e envio

if __name__ == "__main__":
    executar_auditoria_mensal()
