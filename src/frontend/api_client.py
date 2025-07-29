# Cliente de API para dashboard personalizado
import requests


def get_dados_dashboard(token):
    url = "http://localhost:8000/api/dashboard"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
