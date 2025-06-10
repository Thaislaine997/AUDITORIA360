#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teste de integração para o fluxo de autenticação do AUDITORIA360.
Este script valida:
1. O carregamento correto do arquivo login.yaml
2. A consistência da estrutura de dados para autenticação
3. As chamadas de API para obtenção do token JWT
4. O correto armazenamento de token e client_id na sessão
5. O comportamento da UI em diferentes estados de autenticação
"""

import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# Adicionar o diretório raiz ao sys.path para permitir imports dos módulos do projeto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Mockups para componentes do Streamlit que não podemos testar diretamente
class MockSession:
    def __init__(self):
        self.session_state = {}
    
    def __getitem__(self, key):
        return self.session_state.get(key)
    
    def __setitem__(self, key, value):
        self.session_state[key] = value
    
    def get(self, key, default=None):
        return self.session_state.get(key, default)

# Patch global para o streamlit
mock_session = MockSession()

@patch('streamlit.session_state', mock_session.session_state)
class TestAuthFlow(unittest.TestCase):
    
    def setUp(self):
        """Configurações iniciais para cada teste"""
        # Limpar a sessão simulada entre testes
        mock_session.session_state.clear()
        
        # Path para o arquivo de login
        self.login_yaml_path = os.path.join(project_root, 'auth', 'login.yaml')
        
        # Verificar se o arquivo existe
        self.assertTrue(os.path.exists(self.login_yaml_path), 
                       f"Arquivo login.yaml não encontrado em {self.login_yaml_path}")
    
    def test_login_yaml_structure(self):
        """Testa se o arquivo login.yaml tem a estrutura correta"""
        import yaml
        
        with open(self.login_yaml_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # Verificar estrutura básica
        self.assertIn('credentials', config, "login.yaml deve ter uma chave 'credentials'")
        self.assertIn('usernames', config['credentials'], "credentials deve ter uma chave 'usernames'")
        self.assertIn('cookie', config, "login.yaml deve ter uma chave 'cookie'")
        
        # Verificar se há pelo menos um usuário
        self.assertTrue(len(config['credentials']['usernames']) > 0, 
                       "Deve haver pelo menos um usuário definido")
        
        # Verificar estrutura para cada usuário
        for username, user_data in config['credentials']['usernames'].items():
            self.assertIn('password', user_data, f"Usuário {username} deve ter uma senha")
            self.assertIn('client_id', user_data, f"Usuário {username} deve ter um client_id")
    
    @patch('src.frontend.utils.get_api_token')
    @patch('src.frontend.utils.get_current_client_id')
    def test_utils_functions(self, mock_get_client_id, mock_get_token):
        """Testa as funções utilitárias do frontend"""
        from src.frontend.utils import get_auth_headers, display_user_info_sidebar, handle_api_error
        
        # Configurar mocks
        mock_get_token.return_value = "mocked_jwt_token"
        mock_get_client_id.return_value = "mocked_client_id"
        
        # Testar get_auth_headers
        headers = get_auth_headers("test_token")
        self.assertEqual(headers, {"Authorization": "Bearer test_token"}, 
                        "get_auth_headers deve retornar cabeçalho de autorização correto")
        
        headers = get_auth_headers()  # Sem token fornecido, usa o mock
        self.assertEqual(headers, {"Authorization": "Bearer mocked_jwt_token"}, 
                        "get_auth_headers deve usar token da sessão quando nenhum é fornecido")
        
        # Testar handle_api_error com erro 401
        with patch('streamlit.error') as mock_st_error:
            # Salvar um token falso na sessão
            mock_session.session_state['token'] = "fake_token"
            mock_session.session_state['client_id'] = "fake_client_id"
            mock_session.session_state['user_info'] = {"name": "Test User"}
            
            # Chamar a função
            handle_api_error(401)
            
            # Verificar se o erro foi mostrado
            mock_st_error.assert_called_once()
            
            # Verificar se as chaves foram removidas da sessão
            self.assertNotIn('token', mock_session.session_state)
            self.assertNotIn('client_id', mock_session.session_state)
            self.assertNotIn('user_info', mock_session.session_state)
    
    @patch('requests.post')
    def test_api_authentication(self, mock_post):
        """Testa a função de autenticação na API"""
        from src.frontend.painel import autenticar_api
        
        # Configurar mock para simular uma resposta bem-sucedida da API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "jwt_token_from_api"}
        mock_post.return_value = mock_response
        
        # Testar autenticação bem-sucedida
        token = autenticar_api("test_user", "test_password")
        self.assertEqual(token, "jwt_token_from_api", 
                        "autenticar_api deve retornar o token da resposta da API")
        
        # Verificar chamada ao endpoint correto
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("/auth/token", args[0], "O endpoint de autenticação deve ser '/auth/token'")
        
        # Verificar dados enviados
        self.assertEqual(kwargs['data'], {"username": "test_user", "password": "test_password"},
                        "Os dados de autenticação devem incluir username e password")
        
        # Testar erro de autenticação
        mock_post.reset_mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("Unauthorized")
        
        with patch('streamlit.error') as mock_st_error:
            token = autenticar_api("test_user", "wrong_password")
            self.assertIsNone(token, "autenticar_api deve retornar None em caso de erro")
            mock_st_error.assert_called_once()  # Verificar se o erro foi mostrado
    
    def test_session_state_consistency(self):
        """Testa a consistência entre os nomes de variáveis usados em diferentes partes do código"""
        # Importar os módulos que usam st.session_state
        from src.frontend import utils
        import importlib
        
        # Simular login bem-sucedido
        mock_session.session_state['token'] = "test_jwt_token"
        mock_session.session_state['client_id'] = "test_client_id"
        mock_session.session_state['user_info'] = {
            "name": "Test User",
            "username": "test_user",
            "roles": ["user"]
        }
        
        # Verificar se utils.get_api_token obtém o token corretamente
        self.assertEqual(utils.get_api_token(), "test_jwt_token", 
                        "get_api_token deve obter o token da sessão")
        
        # Verificar se utils.get_current_client_id obtém o client_id corretamente
        self.assertEqual(utils.get_current_client_id(), "test_client_id", 
                        "get_current_client_id deve obter o client_id da sessão")
        
        # Testar compatibilidade com nome legado (id_cliente)
        mock_session.session_state.clear()
        mock_session.session_state['id_cliente'] = "legacy_client_id"
        self.assertEqual(utils.get_current_client_id(), "legacy_client_id", 
                        "get_current_client_id deve ter fallback para id_cliente")

if __name__ == "__main__":
    unittest.main()
