# filepath: C:\Users\55479\Documents\AUDITORIA360\conftest.py
import pytest
from unittest.mock import MagicMock, mock_open, patch
import sys
import os
import builtins  # Necessário para mockar builtins.open
import subprocess
import time

# Adiciona o diretório raiz do projeto (onde este conftest.py está) ao sys.path.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
        time.sleep(10) # Aumentado para dar mais tempo ao servidor para iniciar
        
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

@pytest.fixture(scope="session", autouse=True)
def auto_mock_painel_dependencies():
    """
    Moka automaticamente as dependências de src.painel em escopo de sessão
    usando unittest.mock.patch.
    """
    active_patchers = []

    try:
        # 1. Mockear 'builtins.open'
        mocked_open_instance = mock_open()
        p_open = patch("builtins.open", mocked_open_instance)
        active_patchers.append(p_open)
        p_open.start()

        # 2. Mockear o módulo 'yaml'
        mock_yaml_config_content = {
            "credentials": {"usernames": {"testuser": {"name": "Test User", "password": "hashed_password"}}},
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
        mock_auth_instance.login.return_value = ('Test User', True, 'testuser')
        mock_auth_instance.cookie_manager = MagicMock()
        mock_auth_instance.credentials = {"usernames": {"testuser_on_instance": {"name": "Test User on Instance"}}}
        
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
        mock_st.text_input = MagicMock(return_value="some_input")
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

        # 5. Mockear 'os.path.exists'
        p_os_path_exists = patch("os.path.exists", MagicMock(return_value=True))
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

        yield

    finally:
        for p in reversed(active_patchers):
            p.stop()

# Se você tiver outras fixtures globais, elas podem vir aqui.