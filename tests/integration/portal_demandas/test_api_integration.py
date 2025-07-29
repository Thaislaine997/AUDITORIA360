"""
Teste de integração para API de demandas.
"""

import requests


def test_api_demandas_integration():
    # TODO: Ajustar endpoint real
    url = "http://localhost:8000/api/demandas"
    response = requests.get(url)
    assert response.status_code == 200
    print("Teste de integração da API de demandas passou!")
