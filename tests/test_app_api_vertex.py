from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Importa a instância 'app' do seu módulo
from services.api.main import app

# Cria um cliente de teste para a sua aplicação FastAPI
client = TestClient(app)


def test_prever_rubrica_sucesso_identificado(mocker):
    """
    Testa o endpoint /prever-rubrica/ quando uma rubrica é identificada.
    """
    texto_clausula_exemplo = "O piso salarial será de R$ 1500."
    rubrica_mock_retorno = "PISO_SALARIAL"
    payload_esperado = {"rubrica_prevista": rubrica_mock_retorno}

    # Mock para a função prever_rubrica_com_vertex DENTRO do escopo de app_api_vertex
    # É importante mockar onde a função é USADA (importada), não onde ela é definida.
    mock_prever = mocker.patch("src.app_api_vertex.prever_rubrica_com_vertex")
    mock_prever.return_value = rubrica_mock_retorno

    response = client.post("/prever-rubrica/", json={"texto": texto_clausula_exemplo})

    assert response.status_code == 200
    assert response.json() == payload_esperado
    mock_prever.assert_called_once_with(texto_clausula_exemplo)


def test_prever_rubrica_sucesso_nao_identificado(mocker):
    """
    Testa o endpoint /prever-rubrica/ quando prever_rubrica_com_vertex retorna None.
    """
    texto_clausula_exemplo = "Cláusula genérica sem rubrica clara."
    payload_esperado = {"rubrica_prevista": "Não identificado"}

    mock_prever = mocker.patch("src.app_api_vertex.prever_rubrica_com_vertex")
    mock_prever.return_value = None  # Simula que a função não identificou rubrica

    response = client.post("/prever-rubrica/", json={"texto": texto_clausula_exemplo})

    assert response.status_code == 200
    assert response.json() == payload_esperado
    mock_prever.assert_called_once_with(texto_clausula_exemplo)


def test_prever_rubrica_sucesso_rubrica_vazia(mocker):
    """
    Testa o endpoint /prever-rubrica/ quando prever_rubrica_com_vertex retorna string vazia.
    """
    texto_clausula_exemplo = "Outra cláusula."
    payload_esperado = {"rubrica_prevista": "Não identificado"}

    mock_prever = mocker.patch("src.app_api_vertex.prever_rubrica_com_vertex")
    mock_prever.return_value = ""  # Simula que a função retornou uma string vazia

    response = client.post("/prever-rubrica/", json={"texto": texto_clausula_exemplo})

    assert response.status_code == 200
    assert response.json() == payload_esperado
    mock_prever.assert_called_once_with(texto_clausula_exemplo)


def test_prever_rubrica_payload_invalido():
    """
    Testa o endpoint /prever-rubrica/ com um payload inválido (sem o campo 'texto').
    Espera-se um erro 422 do FastAPI.
    """
    response = client.post(
        "/prever-rubrica/", json={"conteudo": "Isso está errado"}
    )  # Campo incorreto

    assert response.status_code == 422  # Unprocessable Entity
    # O corpo do erro 422 pode ser verificado mais detalhadamente se necessário
    # Ex: assert "field required" in response.json()["detail"][0]["msg"].lower()


def test_prever_rubrica_payload_texto_nao_string():
    """
    Testa o endpoint /prever-rubrica/ com 'texto' não sendo uma string.
    Espera-se um erro 422 do FastAPI.
    """
    response = client.post(
        "/prever-rubrica/", json={"texto": 12345}
    )  # 'texto' não é string

    assert response.status_code == 422
    # Ex: assert "string type expected" in response.json()["detail"][0]["msg"].lower()


# TODO: Considerar se há outros casos de erro específicos da API a serem testados.
# Por exemplo, se prever_rubrica_com_vertex pudesse levantar uma exceção específica
# que a API deveria tratar de forma diferente (além do que já é tratado internamente
# por prever_rubrica_com_vertex). No entanto, dado o código atual, os testes acima
# cobrem bem a lógica do endpoint.
