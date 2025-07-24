


import sys
import types
import pytest
from unittest.mock import MagicMock, mock_open, patch
import os
import builtins
import subprocess
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from e2e_config import e2e_context_instance

# Adiciona o diretório raiz do projeto (onde este conftest.py está) ao sys.path.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Mock Google Cloud dependencies globalmente para todos os testes
google_cloud = types.ModuleType("google.cloud")
google_cloud_bigquery = types.ModuleType("google.cloud.bigquery")
google_cloud_storage = types.ModuleType("google.cloud.storage")
google_cloud_exceptions = types.ModuleType("google.cloud.exceptions")

setattr(google_cloud_bigquery, "Client", MagicMock())
setattr(google_cloud_bigquery, "SchemaField", MagicMock())
setattr(google_cloud_bigquery, "Dataset", MagicMock())
setattr(google_cloud_bigquery, "Table", MagicMock())
setattr(google_cloud_bigquery, "Row", MagicMock())
setattr(google_cloud_bigquery, "TimePartitioning", MagicMock())
setattr(google_cloud, "exceptions", google_cloud_exceptions)
setattr(google_cloud_bigquery, "exceptions", google_cloud_exceptions)
sys.modules["google.cloud"] = google_cloud
sys.modules["google.cloud.bigquery"] = google_cloud_bigquery
sys.modules["google.cloud.storage"] = google_cloud_storage
sys.modules["google.cloud.exceptions"] = google_cloud_exceptions
sys.modules["google.auth"] = MagicMock()
google_oauth2 = types.ModuleType("google.oauth2")
google_oauth2_service_account = types.ModuleType("google.oauth2.service_account")
setattr(google_oauth2, "service_account", google_oauth2_service_account)
sys.modules["google.oauth2"] = google_oauth2
sys.modules["google.oauth2.service_account"] = google_oauth2_service_account
sys.modules["google.cloud.storage"] = google_cloud_storage
sys.modules["google.cloud.exceptions"] = google_cloud_exceptions
sys.modules["google.auth"] = MagicMock()
_panel_specific_mock_open = mock_open()

# Contexto para testes E2E parametrizados
class E2EContext:
    current_username: str | None = None
    current_password: str | None = None

e2e_context = E2EContext()

def _selective_open_for_panel(filename, mode='r', *args, **kwargs):
    filename_str = str(filename)
    # TODO: Adicionar condições aqui se o painel Streamlit (painel.py)
    # ou suas dependências diretas (não já mockadas de outra forma)
    # precisarem que 'open' seja mockado para arquivos específicos.
    # Exemplo:
    # if "specific_panel_asset.txt" in filename_str:
    #     print(f"DEBUG: Mocking open for panel asset: {filename_str}")
    #     return _panel_specific_mock_open(filename, mode, *args, **kwargs)
    
    # Por padrão, para todos os outros arquivos (incluindo os JSON de config_manager), usa o open real.
    # Mock open: pode ser ajustado conforme necessário
    raise NotImplementedError("Mock open não implementado para este teste.")

def _selective_os_path_exists_for_panel(path):
    path_str = str(path)
    # TODO: Adicionar condições aqui se o painel Streamlit
    # precisar que 'os.path.exists' seja mockado para caminhos específicos.
    # Exemplo:
    # if "expected_panel_config_dir" in path_str:
    #     print(f"DEBUG: Mocking os.path.exists for panel path: {path_str} to return True")
    #     return True
        
    # Por padrão, usa o os.path.exists real.
    # Mock path.exists: pode ser ajustado conforme necessário
    raise NotImplementedError("Mock path.exists não implementado para este teste.")

@pytest.fixture(scope="session")
def streamlit_server(auto_mock_painel_dependencies): # Depende dos mocks para que o painel inicie corretamente
    """
    Fixture para iniciar e parar o servidor Streamlit para testes E2E.
    """
    # Caminho para o script do painel
    painel_path = os.path.join(os.path.dirname(__file__), "src", "painel.py")
    
    # Comando para iniciar o Streamlit
    # Usamos sys.executable para garantir que estamos usando o mesmo interpretador Python
    # que está executando o pytest.
    command = [
        sys.executable, "-m", "streamlit", "run",
        painel_path,
        "--server.port=8501",
        "--server.headless=true", # Roda em modo headless, importante para CI
        "--server.runOnSave=false",
        "--client.showErrorDetails=false" 
    ]
    
    process = None
    try:
        print(f"\nIniciando servidor Streamlit com comando: {' '.join(command)}")
        # Inicia o servidor Streamlit como um processo em segundo plano
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguarda um pouco para o servidor iniciar
        # Idealmente, deveríamos verificar a saída do servidor ou tentar uma conexão.
        time.sleep(15) # Aumentado para dar mais tempo ao servidor para iniciar
        
        # Verifica se o processo iniciou corretamente
        if process.poll() is not None: # Se poll() não for None, o processo terminou
            stdout, stderr = process.communicate()
            raise RuntimeError(
                f"Falha ao iniciar o servidor Streamlit.\n"
                f"Exit code: {process.returncode}\n"
                f"STDOUT: {stdout.decode('utf-8', errors='ignore')}\n"
                f"STDERR: {stderr.decode('utf-8', errors='ignore')}"
            )
        
        print("Servidor Streamlit iniciado.")
        yield # Permite que os testes sejam executados
        
    finally:
        if process:
            print("\nEncerrando servidor Streamlit...")
            process.terminate() # Tenta encerrar graciosamente
            try:
                process.wait(timeout=5) # Espera o encerramento
            except subprocess.TimeoutExpired:
                print("Servidor Streamlit não encerrou a tempo, forçando...")
                process.kill() # Força o encerramento
            stdout, stderr = process.communicate()
            print("Servidor Streamlit encerrado.")
            # print(f"STDOUT do servidor: {stdout.decode('utf-8', errors='ignore')}")
            # print(f"STDERR do servidor: {stderr.decode('utf-8', errors='ignore')}")

@pytest.fixture(scope="session") # Removido autouse=True
def auto_mock_painel_dependencies():
    """
    Moka automaticamente as dependências de src.painel em escopo de sessão
    usando unittest.mock.patch.
    Os mocks para builtins.open e os.path.exists são agora seletivos.
    """
    active_patchers = []

    try:
        # 1. Mockear 'builtins.open' SELETIVAMENTE
        p_open = patch("builtins.open", _selective_open_for_panel)
        active_patchers.append(p_open)
        p_open.start()

        # 2. Mockear o módulo 'yaml'
        mock_yaml_config_content = {
            "credentials": {"usernames": {
                "cliente1": {"name": "Cliente 1 User", "password": "hashed_password_cliente1"},
                "cliente2": {"name": "Cliente 2 User", "password": "hashed_password_cliente2"},
                "testuser": {"name": "Test User", "password": "hashed_password"}
            }},
            "cookie": {"name": "test_cookie", "key": "test_key", "expiry_days": 30},
            "preauthorized": {}
        }
        mock_yaml_module = MagicMock()
        mock_yaml_module.load = MagicMock(return_value=mock_yaml_config_content)
        mock_yaml_module.SafeLoader = MagicMock()
        p_yaml = patch.dict(sys.modules, {'yaml': mock_yaml_module})
        active_patchers.append(p_yaml)
        p_yaml.start()

        # 3. Mockear o módulo 'streamlit_authenticator' e sua classe 'Authenticate'
        mock_auth_instance = MagicMock()

        def dynamic_login_implementation(form_name, location='main'):
            _mock_st = sys.modules.get('streamlit') # Obter o módulo streamlit mockado

            if e2e_context_instance.username and _mock_st:
                username = e2e_context_instance.username
                user_config = mock_yaml_config_content["credentials"]["usernames"].get(username)
                name = user_config["name"] if user_config else username

                _mock_st.session_state['name'] = name
                _mock_st.session_state['authentication_status'] = True
                _mock_st.session_state['username'] = username
                return (name, True, username)
            elif _mock_st: # Fallback para testuser se e2e_context_instance não estiver preenchido
                _mock_st.session_state['name'] = 'Test User'
                _mock_st.session_state['authentication_status'] = True
                _mock_st.session_state['username'] = 'testuser'
                return ('Test User', True, 'testuser')
            return (None, False, None)

        mock_auth_instance.login.side_effect = dynamic_login_implementation
        mock_auth_instance.cookie_manager = MagicMock()
        mock_auth_instance.credentials = mock_yaml_config_content["credentials"]
        
        mock_authenticator_class_factory = MagicMock(return_value=mock_auth_instance)
        
        mock_stauth_module = MagicMock()
        mock_stauth_module.Authenticate = mock_authenticator_class_factory
        p_stauth = patch.dict(sys.modules, {'streamlit_authenticator': mock_stauth_module})
        active_patchers.append(p_stauth)
        p_stauth.start()

        # 4. Mockear o módulo 'streamlit' (st)
        mock_st = MagicMock()
        _session_state_dict = {}

        def session_state_getitem(key):
            if key in _session_state_dict:
                return _session_state_dict[key]
            raise KeyError(f"Mocked KeyError for st.session_state: {key}")

        def session_state_setitem(key, value):
            _session_state_dict[key] = value

        def session_state_contains(key):
            return key in _session_state_dict
        
        mock_st.session_state = MagicMock()
        mock_st.session_state.__getitem__.side_effect = session_state_getitem
        mock_st.session_state.__setitem__.side_effect = session_state_setitem
        mock_st.session_state.__contains__.side_effect = session_state_contains
        mock_st.session_state.get = MagicMock(side_effect=lambda key, default=None: _session_state_dict.get(key, default))

        def mock_text_input_implementation(label, value="", **kwargs):
            current_label = str(label).lower()

            if "username" in current_label or (kwargs.get("key") and "username" in str(kwargs.get("key")).lower()):
                return e2e_context_instance.username if e2e_context_instance.username is not None else "testuser_from_text_input"
            elif "password" in current_label or (kwargs.get("key") and "password" in str(kwargs.get("key")).lower()):
                return e2e_context_instance.password if e2e_context_instance.password is not None else "password_from_text_input"
            return value

        mock_st.text_input = MagicMock(side_effect=mock_text_input_implementation)

        mock_st.components = MagicMock()
        mock_st.components.v1 = MagicMock()
        mock_st.components.v1.html = MagicMock()
        mock_st.components.html = MagicMock()

        mock_st.sidebar = MagicMock()
        mock_st.sidebar.image = MagicMock()
        mock_st.sidebar.page_link = MagicMock()
        
        mock_st.image = MagicMock()
        mock_st.set_page_config = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.title = MagicMock()
        mock_st.header = MagicMock()
        mock_st.subheader = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.selectbox = MagicMock()
        mock_st.multiselect = MagicMock()
        mock_st.file_uploader = MagicMock()
        
        mock_st.spinner = MagicMock()
        mock_st.spinner.__enter__ = MagicMock(return_value=None)
        mock_st.spinner.__exit__ = MagicMock(return_value=None)
        
        mock_st.success = MagicMock()
        mock_st.error = MagicMock()
        mock_st.warning = MagicMock()
        mock_st.info = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.write = MagicMock()
        mock_st.columns = MagicMock(return_value=(MagicMock(), MagicMock()))
        
        mock_st.expander = MagicMock()
        mock_st.expander.__enter__ = MagicMock(return_value=None)
        mock_st.expander.__exit__ = MagicMock(return_value=None)
        
        mock_st.query_params = MagicMock()
        mock_st.secrets = MagicMock()
        mock_st.cache_data = lambda func: func
        mock_st.cache_resource = lambda func: func
        mock_st.rerun = MagicMock()

        p_streamlit = patch.dict(sys.modules, {'streamlit': mock_st})
        active_patchers.append(p_streamlit)
        p_streamlit.start()

        # 5. Mockear 'os.path.exists' SELETIVAMENTE
        p_os_path_exists = patch("os.path.exists", _selective_os_path_exists_for_panel)
        active_patchers.append(p_os_path_exists)
        p_os_path_exists.start()

        # 6. Mockear o módulo 'json'
        mock_json_module = MagicMock()
        mock_json_module.load = MagicMock(return_value={})
        mock_json_module.loads = MagicMock(return_value={})
        mock_json_module.dump = MagicMock()
        mock_json_module.dumps = MagicMock(return_value="{}")
        p_json = patch.dict(sys.modules, {'json': mock_json_module})
        active_patchers.append(p_json)
        p_json.start()

        # 7. Mockear o módulo 'requests'
        mock_requests_response = MagicMock()
        mock_requests_response.status_code = 200
        mock_requests_response.json.return_value = {"message": "success"}
        mock_requests_response.text = "Success"
        
        mock_requests_module = MagicMock()
        mock_requests_module.get = MagicMock(return_value=mock_requests_response)
        mock_requests_module.post = MagicMock(return_value=mock_requests_response)
        p_requests = patch.dict(sys.modules, {'requests': mock_requests_module})
        active_patchers.append(p_requests)
        p_requests.start()

        # 8. Mockear módulos do Google Cloud (BigQuery, Storage, etc.)
        mock_bigquery_module = MagicMock()
        mock_bigquery_module.Client = MagicMock()
        mock_storage_module = MagicMock()
        mock_storage_module.Client = MagicMock()
        p_gcloud = patch.dict(sys.modules, {
            'google.cloud.bigquery': mock_bigquery_module,
            'google.cloud.storage': mock_storage_module,
            'google.cloud': MagicMock(bigquery=mock_bigquery_module, storage=mock_storage_module),
            'google.auth': MagicMock(),
        })
        active_patchers.append(p_gcloud)
        p_gcloud.start()

        yield

    finally:
        for p in reversed(active_patchers):
            p.stop()

# Se você tiver outras fixtures globais, elas podem vir aqui.