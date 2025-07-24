# Cliente de API v2 para uso em dashboards/pages/8_📊_Benchmarking_Anonimizado.py
import requests

def get_benchmarking(token):
    url = "http://localhost:8000/api/benchmarking"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
