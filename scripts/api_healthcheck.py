import requests

# Altere para a URL da sua API (local ou Vercel)
API_URL = "http://localhost:8000/"

try:
    resp = requests.get(API_URL, timeout=5)
    print(f"Status: {resp.status_code}")
    print("Resposta:", resp.json())
except Exception as e:
    print("Erro ao acessar a API:", e)
