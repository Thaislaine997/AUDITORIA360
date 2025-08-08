"""
Exemplo prático de uso da API de Autenticação do AUDITORIA360.

Este exemplo demonstra:
- Login de usuário
- Criação de usuário
- Gestão de permissões
- Proteção de rotas com JWT

Requer: requests, python-dotenv
"""

from typing import Dict

import requests


class AuditAPI:
    """Cliente para interagir com a API do AUDITORIA360."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def login(self, email: str, password: str) -> Dict:
        """
        Realiza login na API e armazena o token.

        Args:
            email: Email do usuário
            password: Senha do usuário

        Returns:
            dict: Resposta do login com token
        """
        url = f"{self.base_url}/api/v1/auth/login"
        data = {"email": email, "password": password}

        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()

            login_data = response.json()
            self.token = login_data.get("access_token")

            # Atualiza headers com token
            if self.token:
                self.headers["Authorization"] = f"Bearer {self.token}"

            print(f"✅ Login realizado com sucesso para {email}")
            return login_data

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro no login: {e}")
            return {"error": str(e)}

    def get_user_profile(self) -> Dict:
        """
        Obtém o perfil do usuário atual.

        Returns:
            dict: Dados do usuário atual
        """
        if not self.token:
            return {"error": "Token não encontrado. Faça login primeiro."}

        url = f"{self.base_url}/api/v1/auth/me"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            user_data = response.json()
            print(f"✅ Perfil obtido: {user_data.get('name', 'N/A')}")
            return user_data

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao obter perfil: {e}")
            return {"error": str(e)}

    def create_user(self, user_data: Dict) -> Dict:
        """
        Cria um novo usuário (requer permissões de admin).

        Args:
            user_data: Dados do usuário a ser criado

        Returns:
            dict: Resposta da criação do usuário
        """
        if not self.token:
            return {"error": "Token não encontrado. Faça login primeiro."}

        url = f"{self.base_url}/api/v1/auth/users"

        try:
            response = requests.post(url, json=user_data, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            print(f"✅ Usuário criado: {user_data.get('email', 'N/A')}")
            return result

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao criar usuário: {e}")
            return {"error": str(e)}

    def list_permissions(self) -> Dict:
        """
        Lista todas as permissões disponíveis.

        Returns:
            dict: Lista de permissões
        """
        if not self.token:
            return {"error": "Token não encontrado. Faça login primeiro."}

        url = f"{self.base_url}/api/v1/auth/permissions"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            permissions = response.json()
            print(f"✅ Permissões obtidas: {len(permissions)} encontradas")
            return permissions

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao listar permissões: {e}")
            return {"error": str(e)}


def example_basic_authentication():
    """Exemplo básico de autenticação."""
    print("\n🔐 === EXEMPLO DE AUTENTICAÇÃO BÁSICA ===")

    api = AuditAPI()

    # Exemplo de login
    login_result = api.login("admin@auditoria360.com", "admin123")

    if "access_token" in login_result:
        print(f"Token de acesso: {login_result['access_token'][:20]}...")
        print(f"Tipo de token: {login_result.get('token_type', 'Bearer')}")
        print(f"Expira em: {login_result.get('expires_in', 'N/A')} segundos")

        # Obter perfil do usuário
        profile = api.get_user_profile()
        if "name" in profile:
            print(f"Usuário logado: {profile['name']}")
            print(f"Email: {profile['email']}")
            print(f"Role: {profile.get('role', 'N/A')}")


def example_user_management():
    """Exemplo de gerenciamento de usuários."""
    print("\n👥 === EXEMPLO DE GERENCIAMENTO DE USUÁRIOS ===")

    api = AuditAPI()

    # Login como admin
    api.login("admin@auditoria360.com", "admin123")

    # Criar novo usuário
    new_user = {
        "name": "João Silva",
        "email": "joao@exemplo.com",
        "password": "exemplo_senha_segura_123!",
        "role": "hr_user",
        "department": "RH",
        "is_active": True,
    }

    result = api.create_user(new_user)

    if "id" in result:
        print(f"Novo usuário criado com ID: {result['id']}")
        print(f"Status: {'Ativo' if result.get('is_active') else 'Inativo'}")


def example_permissions_check():
    """Exemplo de verificação de permissões."""
    print("\n🛡️ === EXEMPLO DE VERIFICAÇÃO DE PERMISSÕES ===")

    api = AuditAPI()
    api.login("admin@auditoria360.com", "admin123")

    # Listar permissões
    permissions = api.list_permissions()

    if isinstance(permissions, list):
        print("\nPermissões disponíveis:")
        for perm in permissions[:5]:  # Mostrar apenas as primeiras 5
            print(f"- {perm.get('name', 'N/A')}: {perm.get('description', 'N/A')}")

        if len(permissions) > 5:
            print(f"... e mais {len(permissions) - 5} permissões")


def example_error_handling():
    """Exemplo de tratamento de erros."""
    print("\n⚠️ === EXEMPLO DE TRATAMENTO DE ERROS ===")

    api = AuditAPI()

    # Tentar acessar recurso sem autenticação
    profile = api.get_user_profile()
    print(f"Sem token: {profile}")

    # Login com credenciais inválidas
    invalid_login = api.login("invalid@exemplo.com", "senha_errada")
    print(f"Login inválido: {invalid_login}")

    # Tentar criar usuário sem permissões
    api.login("user@exemplo.com", "exemplo_senha_user")  # Login como usuário comum

    user_data = {
        "name": "Teste",
        "email": "teste@exemplo.com",
        "password": "exemplo_senha_123!",
    }

    result = api.create_user(user_data)
    print(f"Criação sem permissão: {result}")


def main():
    """Função principal com todos os exemplos."""
    print("🚀 EXEMPLOS DE USO - API DE AUTENTICAÇÃO AUDITORIA360")
    print("=" * 60)

    try:
        example_basic_authentication()
        example_user_management()
        example_permissions_check()
        example_error_handling()

        print("\n✅ Todos os exemplos executados com sucesso!")
        print("\n📚 Para mais informações, consulte:")
        print("- Documentação da API: http://localhost:8000/docs")
        print("- Manual do usuário: docs/usuario/manual-usuario.md")

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("Verifique se a API está rodando em http://localhost:8000")


if __name__ == "__main__":
    main()
