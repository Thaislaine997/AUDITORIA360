import pytest
from unittest.mock import patch, mock_open, MagicMock, call
from datetime import datetime
import csv
import logging # Para spec=logging.Logger

# Importar funções e constantes do módulo sob teste
from src.log_utils import registrar_log, LOG_FILE, demonstrar_logs
import src.log_utils # Para inspecionar src.log_utils.logger se necessário para debug

@patch('src.log_utils.datetime')
@patch('src.log_utils.csv.DictWriter')
@patch('builtins.open', new_callable=mock_open)
@patch('src.log_utils.os.path.exists')
def test_registrar_log_arquivo_nao_existe(mock_exists, mock_file_open, mock_csv_writer, mock_dt):
    """
    Testa registrar_log quando o arquivo de log não existe (deve escrever o cabeçalho).
    """
    mock_exists.return_value = False # Simula que LOG_FILE não existe
    
    # Configura o mock do datetime para retornar um valor fixo
    fixed_timestamp = datetime(2023, 10, 26, 10, 0, 0)
    mock_dt.now.return_value = fixed_timestamp
    
    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    usuario_teste = "test_user"
    acao_teste = "login"
    ip_teste = "127.0.0.1"
    empresa_teste = "EmpresaX"
    competencia_teste = "2023-10"

    log_data_esperado = {
        "timestamp": fixed_timestamp.isoformat(),
        "usuario": usuario_teste,
        "acao": acao_teste,
        "ip": ip_teste,
        "empresa": empresa_teste,
        "competencia": competencia_teste
    }

    registrar_log(usuario_teste, acao_teste, ip_teste, empresa_teste, competencia_teste)

    mock_exists.assert_called_once_with(LOG_FILE)
    mock_file_open.assert_called_once_with(LOG_FILE, mode='a', newline='', encoding='utf-8')
    mock_csv_writer.assert_called_once_with(mock_file_open(), fieldnames=log_data_esperado.keys())
    
    mock_writer_instance.writeheader.assert_called_once()
    mock_writer_instance.writerow.assert_called_once_with(log_data_esperado)

@patch('src.log_utils.datetime')
@patch('src.log_utils.csv.DictWriter')
@patch('builtins.open', new_callable=mock_open)
@patch('src.log_utils.os.path.exists')
def test_registrar_log_arquivo_existe(mock_exists, mock_file_open, mock_csv_writer, mock_dt):
    """
    Testa registrar_log quando o arquivo de log já existe (não deve escrever o cabeçalho).
    """
    mock_exists.return_value = True # Simula que LOG_FILE existe
    
    fixed_timestamp = datetime(2023, 10, 26, 11, 0, 0)
    mock_dt.now.return_value = fixed_timestamp

    mock_writer_instance = MagicMock()
    mock_csv_writer.return_value = mock_writer_instance

    usuario_teste = "another_user"
    acao_teste = "consulta"
    # Testa com alguns campos opcionais como None para garantir que são tratados como ""
    ip_teste = None 
    empresa_teste = "EmpresaY"
    competencia_teste = None

    log_data_esperado = {
        "timestamp": fixed_timestamp.isoformat(),
        "usuario": usuario_teste,
        "acao": acao_teste,
        "ip": "", # Esperado como string vazia
        "empresa": empresa_teste,
        "competencia": "" # Esperado como string vazia
    }

    registrar_log(usuario_teste, acao_teste, ip_teste, empresa_teste, competencia_teste)

    mock_exists.assert_called_once_with(LOG_FILE)
    mock_file_open.assert_called_once_with(LOG_FILE, mode='a', newline='', encoding='utf-8')
    mock_csv_writer.assert_called_once_with(mock_file_open(), fieldnames=log_data_esperado.keys())
    
    mock_writer_instance.writeheader.assert_not_called() # Não deve chamar writeheader
    mock_writer_instance.writerow.assert_called_once_with(log_data_esperado)

@patch('src.log_utils.logging.basicConfig')  # Patch mais externo, mock_basic_config_injected será o último argumento
@patch('src.log_utils.logger', spec=logging.Logger) # Patch mais interno, mock_logger_injected será o primeiro argumento
def test_demonstrar_logs(mock_logger_injected, mock_basic_config_injected):
    """
    Testa a função demonstrar_logs.
    - Garante que logging.basicConfig seja mockado para evitar configuração global de log.
    - Garante que o logger usado por demonstrar_logs seja o mock_logger_injected.
    """
    demonstrar_logs() # Chama a função que usa o logger (agora mockado)

    expected_calls = [
        call.debug("Este é um log de debug."),
        call.info("Este é um log de informação."),
        call.warning("Este é um log de aviso."),
        call.error("Este é um log de erro."),
        call.critical("Este é um log crítico.")
    ]

    # Asserção primária: verifica se as chamadas esperadas estão em method_calls
    mock_logger_injected.assert_has_calls(expected_calls, any_order=False)

    # Asserção secundária: verifica se *apenas* as chamadas esperadas foram feitas
    assert len(mock_logger_injected.method_calls) == len(expected_calls)