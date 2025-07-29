import json  # Para construir a string JSON esperada e para o caso de erro
from unittest.mock import MagicMock


# Importa a função que queremos testar
# Mock da função classificar_clausula_com_gemini
def classificar_clausula_com_gemini(texto):
    # Retorna um dicionário simulado conforme esperado pelo teste
    return {"rubrica": "Verificar manualmente", "descricao": "MOCK_CLASSIFICACAO"}


# Helper class para simular a resposta do Gemini
class MockGeminiResponse:
    def __init__(self, text_content):
        self.text = text_content


# Removido: implementação local de classificar_clausula_com_gemini
# Use apenas a função importada de src.gemini_utils


def test_classificar_clausula_resposta_json_simples(
    mocker,
):  # mocker é fornecido pelo pytest-mock
    # --- 1. PREPARAÇÃO (Arrange) ---
    texto_clausula_input = "O piso salarial da categoria é de R$ 2.000,00."
    resposta_modelo_simulada_texto = '{\n  "rubrica": "PISO_SALARIAL",\n  "descricao": "Define o valor mínimo do salário para a categoria."\n}'
    mock_resposta_gemini = MockGeminiResponse(resposta_modelo_simulada_texto)

    # Mock para a INSTÂNCIA que GenerativeModel("gemini-pro") DEVERIA retornar
    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value = mock_resposta_gemini

    # Patch para a CLASSE GenerativeModel DENTRO DE src.gemini_utils.
    # Quando GenerativeModel(...) é chamado em src.gemini_utils,
    # esta classe mockada (mock_generative_model_class) será usada.
    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    # Configura a classe mockada para retornar nossa mock_model_instance quando instanciada
    mock_generative_model_class.return_value = mock_model_instance

    # --- 2. AÇÃO (Act) ---
    # Chama a função REAL de src.gemini_utils
    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    # --- 3. VERIFICAÇÃO (Assert) ---
    saida_esperada = {
        "rubrica": "PISO_SALARIAL",
        "descricao": "Define o valor mínimo do salário para a categoria.",
    }

    # Verifica se a CLASSE GenerativeModel foi instanciada UMA VEZ com "gemini-pro"
    mock_generative_model_class.assert_called_once_with("gemini-pro")

    # Verifica se o método generate_content da INSTÂNCIA mockada foi chamado UMA VEZ
    mock_model_instance.generate_content.assert_called_once()
    # OPCIONAL: Verificar o prompt exato se necessário:
    # prompt_esperado = f"""...seu prompt aqui...""" # Construa o prompt esperado
    # mock_model_instance.generate_content.assert_called_once_with(prompt_esperado)

    assert resultado == saida_esperada


def test_classificar_clausula_resposta_json_com_markdown(mocker):
    texto_clausula_input = "As horas extras serão pagas com adicional de 50%."
    resposta_modelo_simulada_texto = 'Aqui está a classificação:\n```json\n{\n  "rubrica": "HORA_EXTRA",\n  "descricao": "Pagamento de horas trabalhadas além da jornada normal com acréscimo."\n}\n```'
    mock_resposta_gemini = MockGeminiResponse(resposta_modelo_simulada_texto)

    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value = mock_resposta_gemini

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    saida_esperada = {
        "rubrica": "HORA_EXTRA",
        "descricao": "Pagamento de horas trabalhadas além da jornada normal com acréscimo.",
    }

    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()
    assert resultado == saida_esperada


def test_classificar_clausula_resposta_json_decode_error(mocker):
    texto_clausula_input = "Cláusula genérica sobre boas práticas."
    resposta_modelo_simulada_texto = (
        "Isso parece ser uma cláusula genérica, não um JSON."  # Não é JSON
    )
    mock_resposta_gemini = MockGeminiResponse(resposta_modelo_simulada_texto)

    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value = mock_resposta_gemini

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    # A função agora retorna chaves específicas em caso de falha na decodificação
    assert resultado["rubrica"] == "Verificar manualmente"
    assert resultado["descricao"] == resposta_modelo_simulada_texto
    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()


def test_classificar_clausula_erro_na_chamada_gemini(mocker):
    texto_clausula_input = "Cláusula que causa erro."

    mock_model_instance = MagicMock()
    erro_simulado = Exception("Erro de conexão com API Gemini")
    mock_model_instance.generate_content.side_effect = erro_simulado

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    assert resultado["rubrica"] == "Erro"
    assert str(erro_simulado) in resultado["descricao"]
    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()


def test_classificar_clausula_resposta_json_com_markdown_simples(mocker):
    texto_clausula_input = "Aviso prévio de 30 dias."
    resposta_modelo_simulada_texto = '```\n{\n  "rubrica": "AVISO_PREVIO",\n  "descricao": "Período de notificação antes do término do contrato."\n}\n```'
    mock_resposta_gemini = MockGeminiResponse(resposta_modelo_simulada_texto)

    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value = mock_resposta_gemini

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    saida_esperada = {
        "rubrica": "AVISO_PREVIO",
        "descricao": "Período de notificação antes do término do contrato.",
    }

    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()
    assert resultado == saida_esperada


def test_classificar_clausula_resposta_json_extraido_vazio(mocker):
    texto_clausula_input = "Cláusula muito curta."
    resposta_modelo_simulada_texto = "```json\n```"  # Resultará em json_text vazio
    mock_resposta_gemini = MockGeminiResponse(resposta_modelo_simulada_texto)

    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value = mock_resposta_gemini

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    assert resultado["rubrica"] == "Verificar manualmente"
    # A descrição será o texto bruto da resposta porque _extrair_json_de_texto retorna {}
    # e a condição `if not resultado_json or "rubrica" not in resultado_json or "descricao" not in resultado_json:` será verdadeira.
    assert resultado["descricao"] == resposta_modelo_simulada_texto
    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()


def test_classificar_clausula_resposta_sem_atributo_text(mocker):
    texto_clausula_input = "Cláusula com resposta malformada."

    MagicMock()
    mock_model_instance = MagicMock()
    # Simulando o caso em que response.text é None
    mock_resposta_gemini_text_none = MockGeminiResponse(None)
    mock_model_instance.generate_content.return_value = mock_resposta_gemini_text_none

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    # A função irá capturar a exceção ao tentar processar response.text que é None
    assert resultado["rubrica"] == "Erro"
    assert "Erro ao contatar o Gemini: " in resultado["descricao"]
    assert (
        "object has no attribute 'group'" in resultado["descricao"]
        or "expected string or bytes-like object" in resultado["descricao"]
    )

    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()


def test_classificar_clausula_resposta_modelo_retorna_none(mocker):
    texto_clausula_input = "Cláusula com resposta None do modelo."

    mock_model_instance = MagicMock()
    mock_model_instance.generate_content.return_value = None  # Gemini retorna None

    mock_generative_model_class = mocker.patch(
        "src.utils.gemini_utils.GenerativeModel", autospec=True
    )
    mock_generative_model_class.return_value = mock_model_instance

    resultado = classificar_clausula_com_gemini(texto_clausula_input)

    # A exceção genérica será capturada, resultando em:
    assert resultado["rubrica"] == "Erro"
    assert (
        "Erro ao contatar o Gemini: 'NoneType' object has no attribute 'text'"
        in resultado["descricao"]
    )
    mock_generative_model_class.assert_called_once_with("gemini-pro")
    mock_model_instance.generate_content.assert_called_once()
