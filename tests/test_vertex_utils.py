import pytest
from unittest.mock import MagicMock, patch, ANY

# Importar as funções do módulo que queremos testar
from services.ml.components.vertex_utils import inicializar_vertex, prever_rubrica_com_vertex, PROJECT_ID, LOCATION, ENDPOINT_ID

# Testes para inicializar_vertex
def test_inicializar_vertex_chama_aiplatform_init(mocker):
    """
    Testa se aiplatform.init é chamado com os argumentos corretos.
    """
    mock_aiplatform_init = mocker.patch('src.vertex_utils.aiplatform.init')

    inicializar_vertex()

    mock_aiplatform_init.assert_called_once_with(project=PROJECT_ID, location=LOCATION)

# Testes para prever_rubrica_com_vertex
def test_prever_rubrica_com_vertex_sucesso(mocker):
    """
    Testa o caminho de sucesso da previsão de rubrica.
    """
    texto_clausula_exemplo = "O pagamento será efetuado no quinto dia útil."
    rubrica_esperada = "PAGAMENTO_SALARIO"

    mock_init_vertex = mocker.patch('src.vertex_utils.inicializar_vertex')
    mock_endpoint_instance = MagicMock()
    mock_predict_response = MagicMock()
    mock_predict_response.predictions = [{'displayName': rubrica_esperada}] 
    mock_endpoint_instance.predict.return_value = mock_predict_response
    mock_aiplatform_endpoint_class = mocker.patch('src.vertex_utils.aiplatform.Endpoint', autospec=True)
    mock_aiplatform_endpoint_class.return_value = mock_endpoint_instance

    resultado = prever_rubrica_com_vertex(texto_clausula_exemplo)

    mock_init_vertex.assert_called_once()
    expected_endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    mock_aiplatform_endpoint_class.assert_called_once_with(endpoint_name=expected_endpoint_name)
    mock_endpoint_instance.predict.assert_called_once_with(instances=[{"content": texto_clausula_exemplo}])
    assert resultado == rubrica_esperada

def test_prever_rubrica_com_vertex_resposta_sem_predicoes(mocker):
    """
    Testa o caso em que a resposta do endpoint.predict não tem 'predictions'.
    """
    texto_clausula_exemplo = "Cláusula qualquer."
    mock_init_vertex = mocker.patch('src.vertex_utils.inicializar_vertex')
    mock_endpoint_instance = MagicMock()
    mock_predict_response = MagicMock()
    mock_predict_response.predictions = []

    mock_endpoint_instance.predict.return_value = mock_predict_response
    mock_aiplatform_endpoint_class = mocker.patch('src.vertex_utils.aiplatform.Endpoint', autospec=True)
    mock_aiplatform_endpoint_class.return_value = mock_endpoint_instance

    resultado = prever_rubrica_com_vertex(texto_clausula_exemplo)

    mock_init_vertex.assert_called_once()
    expected_endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    mock_aiplatform_endpoint_class.assert_called_once_with(endpoint_name=expected_endpoint_name)
    mock_endpoint_instance.predict.assert_called_once_with(instances=[{"content": texto_clausula_exemplo}])
    assert resultado == "Erro na predição da rubrica: Nenhuma predição retornada."

def test_prever_rubrica_com_vertex_resposta_malformada(mocker):
    """
    Testa o caso em que a predição não tem 'displayName'.
    """
    texto_clausula_exemplo = "Outra cláusula."
    mock_init_vertex = mocker.patch('src.vertex_utils.inicializar_vertex')
    mock_endpoint_instance = MagicMock()
    mock_predict_response = MagicMock()
    mock_predict_response.predictions = [{"alguma_outra_chave": "valor"}]
    mock_endpoint_instance.predict.return_value = mock_predict_response
    mock_aiplatform_endpoint_class = mocker.patch('src.vertex_utils.aiplatform.Endpoint', autospec=True)
    mock_aiplatform_endpoint_class.return_value = mock_endpoint_instance

    resultado = prever_rubrica_com_vertex(texto_clausula_exemplo)
    
    expected_endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    mock_aiplatform_endpoint_class.assert_called_once_with(endpoint_name=expected_endpoint_name)
    assert resultado == "Rubrica não encontrada na predição."

def test_prever_rubrica_com_vertex_excecao_no_predict(mocker):
    """
    Testa o tratamento de exceção durante a chamada a endpoint.predict().
    """
    texto_clausula_exemplo = "Cláusula problemática."
    mock_init_vertex = mocker.patch('src.vertex_utils.inicializar_vertex')
    mock_endpoint_instance = MagicMock()
    erro_simulado = Exception("Falha na API Vertex")
    mock_endpoint_instance.predict.side_effect = erro_simulado
    mock_aiplatform_endpoint_class = mocker.patch('src.vertex_utils.aiplatform.Endpoint', autospec=True)
    mock_aiplatform_endpoint_class.return_value = mock_endpoint_instance

    resultado = prever_rubrica_com_vertex(texto_clausula_exemplo)

    mock_init_vertex.assert_called_once()
    expected_endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    mock_aiplatform_endpoint_class.assert_called_once_with(endpoint_name=expected_endpoint_name)
    mock_endpoint_instance.predict.assert_called_once_with(instances=[{"content": texto_clausula_exemplo}])
    assert f"Erro na predição da rubrica: {erro_simulado}" == resultado

def test_prever_rubrica_com_vertex_excecao_no_endpoint_init(mocker):
    """
    Testa o tratamento de exceção durante a inicialização do aiplatform.Endpoint.
    """
    texto_clausula_exemplo = "Cláusula que falha antes."
    mock_init_vertex = mocker.patch('src.vertex_utils.inicializar_vertex')
    
    erro_simulado = Exception("Falha ao criar Endpoint")
    mock_aiplatform_endpoint_class = mocker.patch('src.vertex_utils.aiplatform.Endpoint', autospec=True)
    mock_aiplatform_endpoint_class.side_effect = erro_simulado

    resultado = prever_rubrica_com_vertex(texto_clausula_exemplo)

    mock_init_vertex.assert_called_once()
    expected_endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    mock_aiplatform_endpoint_class.assert_called_once_with(endpoint_name=expected_endpoint_name)
    assert f"Erro na predição da rubrica: {erro_simulado}" == resultado

def test_prever_rubrica_com_vertex_endpoint_predict_retorna_none(mocker):
    """
    Testa o caso em que endpoint.predict() retorna None.
    """
    texto_clausula_exemplo = "Cláusula com predict None."
    mock_init_vertex = mocker.patch('src.vertex_utils.inicializar_vertex')
    mock_endpoint_instance = MagicMock()
    mock_endpoint_instance.predict.return_value = None
    
    mock_aiplatform_endpoint_class = mocker.patch('src.vertex_utils.aiplatform.Endpoint', autospec=True)
    mock_aiplatform_endpoint_class.return_value = mock_endpoint_instance

    resultado = prever_rubrica_com_vertex(texto_clausula_exemplo)

    mock_init_vertex.assert_called_once()
    expected_endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    mock_aiplatform_endpoint_class.assert_called_once_with(endpoint_name=expected_endpoint_name)
    mock_endpoint_instance.predict.assert_called_once_with(instances=[{"content": texto_clausula_exemplo}])
    assert resultado == "Erro na predição da rubrica: A predição retornou None."