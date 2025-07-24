import requests
import os

# Placeholder para automação de onboarding

def onboarding_automacao():
    portal_url = os.getenv("PORTAL_DEMANDAS_URL", "http://localhost:8000/api/clientes")
    novo_cliente = {
        "nome": "Empresa Exemplo",
        "email": "contato@empresa.com",
        "responsavel": "João RH",
        "data_onboarding": "2025-07-24"
    }
    try:
        response = requests.post(portal_url, json=novo_cliente, timeout=10)
        if response.status_code == 201:
            print(f"Onboarding realizado com sucesso: {response.json()}")
        else:
            print(f"Falha no onboarding: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro na integração com Portal Demandas: {e}")

if __name__ == "__main__":
    onboarding_automacao()
