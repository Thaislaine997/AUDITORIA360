# Placeholder para automação de comunicados

from src.ai_agent import IAAuditoriaAgent
import os

def gerar_comunicados():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    ia_agent = IAAuditoriaAgent(gemini_api_key)
    comunicados = [
        {"tipo": "aviso_folha", "params": {"data": "2025-07-24", "mensagem": "Folha processada com sucesso."}},
        {"tipo": "alerta_risco", "params": {"risco": "Divergência salarial detectada."}},
    ]
    for comunicado in comunicados:
        texto = ia_agent.gerar_comunicado(comunicado["tipo"], comunicado["params"])
        print(f"Comunicado gerado ({comunicado['tipo']}):\n{texto}\n")

if __name__ == "__main__":
    gerar_comunicados()
