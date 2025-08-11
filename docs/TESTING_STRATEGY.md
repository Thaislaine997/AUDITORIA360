# 🧪 AUDITORIA360 - Estratégia de Testes Completa

*Framework abrangente de testes para garantir qualidade e confiabilidade*

---

## 🎯 Visão Geral da Estratégia

### Pirâmide de Testes
```
                  🔺 E2E Tests (10%)
                 /                 \
                /   Integration      \
               /    Tests (30%)       \
              /                       \
             /_________________________\
            Unit Tests (60%)
```

### Tipos de Teste Implementados
- **Unit Tests**: Testes de componentes isolados
- **Integration Tests**: Testes de módulos interagindo
- **E2E Tests**: Testes de fluxo completo do usuário
- **Load Tests**: Testes de performance e escalabilidade
- **Security Tests**: Testes de vulnerabilidades
- **Smoke Tests**: Testes básicos pós-deploy

---

## 🔬 Testes Unitários

### Cobertura Atual
- **Meta**: >85% de cobertura
- **Atual**: 85.2% (conforme checklist interno)
- **Críticos**: 100% (auth, payments, security)

### Estrutura dos Testes
```
tests/unit/
├── auth/
│   ├── test_authentication.py
│   ├── test_authorization.py  
│   └── test_jwt_tokens.py
├── contabilidade/
│   ├── test_client_management.py
│   ├── test_audit_service.py
│   └── test_report_generation.py
├── ml/
│   ├── test_risk_analysis.py
│   ├── test_ai_integration.py
│   └── test_model_validation.py
└── utils/
    ├── test_validators.py
    ├── test_helpers.py
    └── test_encryption.py
```

### Exemplo de Teste Unitário
```python
# tests/unit/auth/test_authentication.py
import pytest
from fastapi.testclient import TestClient
from src.auth.service import AuthService
from src.auth.models import User

class TestAuthentication:
    
    @pytest.fixture
    def auth_service(self):
        return AuthService()
    
    @pytest.fixture
    def sample_user(self):
        return {
            "email": "test@exemplo.com",
            "password": "senha123",
            "contabilidade_id": "123e4567-e89b-12d3-a456-426614174000"
        }
    
    def test_create_user_success(self, auth_service, sample_user):
        """Teste criação de usuário com sucesso"""
        user = auth_service.create_user(**sample_user)
        
        assert user.email == sample_user["email"]
        assert user.contabilidade_id == sample_user["contabilidade_id"]
        assert user.password_hash != sample_user["password"]  # Senha foi hasheada
    
    def test_create_user_duplicate_email(self, auth_service, sample_user):
        """Teste criação de usuário com email duplicado"""
        auth_service.create_user(**sample_user)
        
        with pytest.raises(ValueError, match="Email já existe"):
            auth_service.create_user(**sample_user)
    
    def test_login_valid_credentials(self, auth_service, sample_user):
        """Teste login com credenciais válidas"""
        auth_service.create_user(**sample_user)
        
        token = auth_service.login(
            sample_user["email"], 
            sample_user["password"]
        )
        
        assert token is not None
        assert len(token) > 0
    
    def test_login_invalid_credentials(self, auth_service, sample_user):
        """Teste login com credenciais inválidas"""
        auth_service.create_user(**sample_user)
        
        with pytest.raises(ValueError, match="Credenciais inválidas"):
            auth_service.login(sample_user["email"], "senha_errada")

    @pytest.mark.parametrize("email,password,expected_error", [
        ("", "senha123", "Email é obrigatório"),
        ("email_inválido", "senha123", "Email inválido"),
        ("test@exemplo.com", "", "Senha é obrigatória"),
        ("test@exemplo.com", "123", "Senha deve ter pelo menos 6 caracteres"),
    ])
    def test_create_user_validation(self, auth_service, email, password, expected_error):
        """Teste validações de entrada"""
        with pytest.raises(ValueError, match=expected_error):
            auth_service.create_user(
                email=email,
                password=password,
                contabilidade_id="123e4567-e89b-12d3-a456-426614174000"
            )
```

---

## 🔗 Testes de Integração

### Cenários de Integração
- **API + Database**: Endpoints com persistência
- **API + AI Services**: Integração OpenAI
- **API + Storage**: Upload/download R2
- **Frontend + Backend**: Comunicação completa
- **Multi-tenant**: Isolamento de dados

### Exemplo de Teste de Integração
```python
# tests/integration/test_audit_flow.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestAuditFlow:
    
    @pytest.fixture
    def authenticated_user(self):
        """Usuário autenticado para testes"""
        # Criar usuário de teste
        response = client.post("/api/auth/register", json={
            "email": "contab@teste.com",
            "password": "teste123",
            "contabilidade_id": "550e8400-e29b-41d4-a716-446655440000"
        })
        
        # Fazer login
        login_response = client.post("/api/auth/login", json={
            "email": "contab@teste.com",
            "password": "teste123"
        })
        
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_complete_audit_flow(self, authenticated_user):
        """Teste do fluxo completo de auditoria"""
        
        # 1. Criar cliente final
        client_response = client.post(
            "/api/contabilidade/clientes",
            headers=authenticated_user,
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678000199",
                "email_contato": "rh@empresateste.com"
            }
        )
        assert client_response.status_code == 201
        cliente_id = client_response.json()["id"]
        
        # 2. Disparar auditoria
        audit_response = client.post(
            "/api/contabilidade/auditorias",
            headers=authenticated_user,
            json={
                "cliente_id": cliente_id,
                "mes_referencia": "2025-08",
                "tipo": "mensal"
            }
        )
        assert audit_response.status_code == 201
        auditoria_id = audit_response.json()["id"]
        
        # 3. Verificar status da auditoria
        status_response = client.get(
            f"/api/contabilidade/auditorias/{auditoria_id}",
            headers=authenticated_user
        )
        assert status_response.status_code == 200
        assert status_response.json()["status"] in ["processando", "concluida"]
        
        # 4. Obter score de risco (quando disponível)
        # Pode precisar de retry/polling para aguardar processamento IA
        import time
        for _ in range(10):  # Retry por 10 segundos
            score_response = client.get(
                f"/api/contabilidade/auditorias/{auditoria_id}/score_risco",
                headers=authenticated_user
            )
            if score_response.status_code == 200:
                break
            time.sleep(1)
        
        assert score_response.status_code == 200
        score_data = score_response.json()
        assert "score_risco" in score_data
        assert 0 <= score_data["score_risco"] <= 100
    
    def test_multi_tenant_isolation(self):
        """Teste isolamento multi-tenant"""
        
        # Criar usuários de contabilidades diferentes
        user1_response = client.post("/api/auth/register", json={
            "email": "contab1@teste.com",
            "password": "teste123",
            "contabilidade_id": "550e8400-e29b-41d4-a716-446655440000"
        })
        
        user2_response = client.post("/api/auth/register", json={
            "email": "contab2@teste.com", 
            "password": "teste123",
            "contabilidade_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
        })
        
        # Login usuários
        token1 = client.post("/api/auth/login", json={
            "email": "contab1@teste.com",
            "password": "teste123"
        }).json()["access_token"]
        
        token2 = client.post("/api/auth/login", json={
            "email": "contab2@teste.com",
            "password": "teste123"
        }).json()["access_token"]
        
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Usuário 1 cria cliente
        client1_response = client.post(
            "/api/contabilidade/clientes",
            headers=headers1,
            json={
                "nome": "Cliente Contab 1",
                "cnpj": "11111111000111"
            }
        )
        
        # Usuário 2 não deve ver cliente do usuário 1
        clientes2_response = client.get(
            "/api/contabilidade/clientes",
            headers=headers2
        )
        
        clientes2_data = clientes2_response.json()
        client1_id = client1_response.json()["id"]
        
        # Verificar que cliente do user1 não aparece para user2
        client1_ids = [c["id"] for c in clientes2_data]
        assert client1_id not in client1_ids
```

---

## 🎭 Testes End-to-End (E2E)

### Ferramentas Utilizadas
- **Playwright**: Para automação do browser
- **pytest-playwright**: Integração com pytest

### Cenários E2E Críticos
1. **Onboarding Completo**: Registro → Login → Setup inicial
2. **Fluxo de Auditoria**: Criar cliente → Disparar auditoria → Visualizar relatório
3. **Fluxo Admin**: Gestão de contabilidades e usuários
4. **Responsividade**: Testes em diferentes dispositivos

### Exemplo de Teste E2E
```python
# tests/e2e/test_audit_workflow.py
import pytest
from playwright.async_api import async_playwright, Page

class TestAuditWorkflowE2E:
    
    @pytest.fixture
    async def page(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            yield page
            await context.close()
            await browser.close()
    
    async def test_complete_audit_workflow(self, page: Page):
        """Teste E2E completo do workflow de auditoria"""
        
        # 1. Navegar para a página de login
        await page.goto("http://localhost:3000/login")
        
        # 2. Fazer login
        await page.fill('[data-testid="email-input"]', 'contab@teste.com')
        await page.fill('[data-testid="password-input"]', 'teste123')
        await page.click('[data-testid="login-button"]')
        
        # 3. Aguardar redirecionamento para dashboard
        await page.wait_for_url("**/dashboard")
        
        # 4. Navegar para página de clientes
        await page.click('[data-testid="clientes-menu"]')
        await page.wait_for_url("**/clientes")
        
        # 5. Criar novo cliente
        await page.click('[data-testid="novo-cliente-button"]')
        await page.fill('[data-testid="nome-input"]', 'Empresa E2E Teste')
        await page.fill('[data-testid="cnpj-input"]', '12345678000199')
        await page.fill('[data-testid="email-input"]', 'rh@e2eteste.com')
        await page.click('[data-testid="salvar-cliente-button"]')
        
        # 6. Verificar cliente criado
        await page.wait_for_selector('[data-testid="cliente-item"]')
        cliente_nome = await page.text_content('[data-testid="cliente-nome"]')
        assert "Empresa E2E Teste" in cliente_nome
        
        # 7. Disparar auditoria
        await page.click('[data-testid="auditoria-button"]')
        await page.select_option('[data-testid="mes-select"]', '2025-08')
        await page.click('[data-testid="disparar-auditoria-button"]')
        
        # 8. Aguardar processamento
        await page.wait_for_selector('[data-testid="auditoria-status"]')
        
        # 9. Verificar resultado
        # Aguardar até auditoria completar (pode demorar devido à IA)
        await page.wait_for_selector('[data-testid="score-risco"]', timeout=30000)
        score_text = await page.text_content('[data-testid="score-risco"]')
        assert score_text is not None
        
        # 10. Download do relatório
        async with page.expect_download() as download_info:
            await page.click('[data-testid="download-relatorio-button"]')
        download = await download_info.value
        assert download.suggested_filename.endswith('.pdf')
    
    @pytest.mark.parametrize("device", [
        "iPhone 12",
        "iPad", 
        "Desktop Chrome"
    ])
    async def test_responsive_design(self, device):
        """Teste de responsividade em diferentes dispositivos"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            
            if device == "Desktop Chrome":
                context = await browser.new_context()
            else:
                device_config = p.devices[device]
                context = await browser.new_context(**device_config)
            
            page = await context.new_page()
            
            # Testar páginas principais
            urls = [
                "http://localhost:3000/login",
                "http://localhost:3000/dashboard", 
                "http://localhost:3000/clientes"
            ]
            
            for url in urls:
                await page.goto(url)
                
                # Verificar se elementos críticos estão visíveis
                if "login" in url:
                    await page.wait_for_selector('[data-testid="login-form"]')
                    assert await page.is_visible('[data-testid="login-button"]')
                
                # Verificar que não há overflow horizontal
                viewport_width = page.viewport_size["width"]
                body_width = await page.evaluate("document.body.scrollWidth")
                assert body_width <= viewport_width, f"Overflow horizontal detectado em {url}"
            
            await context.close()
            await browser.close()
```

---

## ⚡ Testes de Performance e Carga

### Ferramentas Utilizadas
- **Locust**: Para testes de carga
- **Artillery**: Para testes de performance
- **Pytest-benchmark**: Para benchmarks unitários

### Cenários de Carga
```python
# tests/load/locustfile.py
from locust import HttpUser, task, between
import random

class AuditUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup inicial - login do usuário"""
        self.login()
    
    def login(self):
        """Realizar login e armazenar token"""
        response = self.client.post("/api/auth/login", json={
            "email": f"test{random.randint(1,100)}@exemplo.com",
            "password": "teste123"
        })
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def list_clients(self):
        """Listar clientes (operação mais comum)"""
        self.client.get(
            "/api/contabilidade/clientes",
            headers=self.headers
        )
    
    @task(2) 
    def view_dashboard(self):
        """Visualizar dashboard"""
        self.client.get(
            "/api/reports/dashboard",
            headers=self.headers
        )
    
    @task(1)
    def create_audit(self):
        """Disparar auditoria (operação menos frequente)"""
        client_id = f"client_{random.randint(1,50)}"
        
        self.client.post(
            "/api/contabilidade/auditorias",
            headers=self.headers,
            json={
                "cliente_id": client_id,
                "mes_referencia": "2025-08",
                "tipo": "mensal"
            }
        )
    
    @task(1)
    def health_check(self):
        """Health check periódico"""
        self.client.get("/api/health")

# Comando para executar:
# locust -f tests/load/locustfile.py --host=https://api.auditoria360.com
```

### Métricas de Performance Esperadas
| Métrica | Meta | Crítico |
|---------|------|---------|
| **Response Time (p95)** | < 500ms | < 2s |
| **Throughput** | > 100 req/s | > 50 req/s |
| **Error Rate** | < 1% | < 5% |
| **CPU Usage** | < 70% | < 90% |
| **Memory Usage** | < 80% | < 95% |

---

## 🔒 Testes de Segurança

### Categorias de Testes
- **Authentication/Authorization**: Bypass attempts
- **Input Validation**: SQL injection, XSS
- **Rate Limiting**: Brute force protection
- **Data Privacy**: Multi-tenant isolation
- **HTTPS/TLS**: Certificate validation

### Exemplo de Teste de Segurança
```python
# tests/security/test_security_vulnerabilities.py
import pytest
from fastapi.testclient import TestClient
import time

class TestSecurityVulnerabilities:
    
    def test_sql_injection_protection(self, client: TestClient):
        """Teste proteção contra SQL injection"""
        # Tentar SQL injection no parâmetro de busca
        malicious_input = "'; DROP TABLE usuarios; --"
        
        response = client.get(
            f"/api/contabilidade/clientes?search={malicious_input}",
            headers=self.get_auth_headers()
        )
        
        # Sistema deve retornar erro ou resultado vazio, não falhar
        assert response.status_code in [200, 400, 422]
        
        # Verificar que tabela usuarios ainda existe
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
    
    def test_xss_protection(self, client: TestClient):
        """Teste proteção contra XSS"""
        xss_payload = "<script>alert('XSS')</script>"
        
        response = client.post(
            "/api/contabilidade/clientes",
            headers=self.get_auth_headers(),
            json={
                "nome": xss_payload,
                "cnpj": "12345678000199"
            }
        )
        
        if response.status_code == 201:
            # Se cliente foi criado, verificar que script foi sanitizado
            client_data = response.json()
            assert "<script>" not in client_data["nome"]
            assert "&lt;script&gt;" in client_data["nome"] or xss_payload not in client_data["nome"]
    
    def test_rate_limiting(self, client: TestClient):
        """Teste rate limiting na API"""
        # Fazer muitas requisições rapidamente
        responses = []
        for i in range(15):  # Mais que o limite de 10/min
            response = client.post("/api/auth/login", json={
                "email": "test@exemplo.com",
                "password": "wrong_password"
            })
            responses.append(response.status_code)
        
        # Deve ter pelo menos uma requisição bloqueada (429)
        assert 429 in responses, "Rate limiting não está funcionando"
    
    def test_authorization_bypass(self, client: TestClient):
        """Teste tentativa de bypass de autorização"""
        # Tentar acessar dados sem token
        response = client.get("/api/contabilidade/clientes")
        assert response.status_code == 401
        
        # Tentar com token inválido
        response = client.get(
            "/api/contabilidade/clientes",
            headers={"Authorization": "Bearer token_invalido"}
        )
        assert response.status_code in [401, 403]
        
        # Tentar acessar dados de outra contabilidade
        token1 = self.get_token_for_user("user1@contab1.com")
        token2 = self.get_token_for_user("user2@contab2.com")
        
        # User1 cria cliente
        client1_response = client.post(
            "/api/contabilidade/clientes",
            headers={"Authorization": f"Bearer {token1}"},
            json={"nome": "Cliente Contab1", "cnpj": "11111111000111"}
        )
        client1_id = client1_response.json()["id"]
        
        # User2 tenta acessar cliente do User1
        response = client.get(
            f"/api/contabilidade/clientes/{client1_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code in [403, 404]  # Forbidden ou Not Found
```

---

## 💨 Smoke Tests (Pós-Deploy)

### Testes Críticos Pós-Deploy
```python
# tests/smoke/test_production_health.py
import pytest
import requests
import os

BASE_URL = os.getenv("PRODUCTION_URL", "https://auditoria360.com")
API_URL = os.getenv("API_URL", "https://api.auditoria360.com")

class TestProductionSmoke:
    
    def test_frontend_availability(self):
        """Teste se frontend está acessível"""
        response = requests.get(f"{BASE_URL}/", timeout=10)
        assert response.status_code == 200
        assert "AUDITORIA360" in response.text
    
    def test_api_health_check(self):
        """Teste health check da API"""
        response = requests.get(f"{API_URL}/health", timeout=10)
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data["status"] == "healthy"
        assert health_data["checks"]["database"] == "healthy"
    
    def test_login_endpoint(self):
        """Teste endpoint de login"""
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json={
                "email": os.getenv("SMOKE_TEST_EMAIL"),
                "password": os.getenv("SMOKE_TEST_PASSWORD")
            },
            timeout=10
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_ssl_certificate(self):
        """Teste validade do certificado SSL"""
        import ssl
        import socket
        from datetime import datetime, timedelta
        
        hostname = "auditoria360.com"
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Verificar que certificado é válido por pelo menos 30 dias
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (not_after - datetime.now()).days
                
                assert days_until_expiry > 30, f"SSL certificate expires in {days_until_expiry} days"
```

---

## 📊 Configuração e Execução

### Configuração do Pytest
```ini
# pyproject.toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=src --cov-report=html --cov-report=term-missing"
testpaths = [
    "tests",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests", 
    "e2e: End-to-end tests",
    "load: Load tests",
    "security: Security tests",
    "smoke: Smoke tests"
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/migrations/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError"
]
```

### Comandos de Execução
```bash
# Testes unitários
pytest tests/unit/ -m unit

# Testes de integração
pytest tests/integration/ -m integration

# Testes E2E
pytest tests/e2e/ -m e2e

# Testes de segurança
pytest tests/security/ -m security

# Testes de fumaça (pós-deploy)
pytest tests/smoke/ -m smoke

# Todos os testes com relatório de cobertura
pytest --cov=src --cov-report=html

# Testes em paralelo (mais rápido)
pytest -n auto

# Testes específicos por padrão
pytest -k "test_auth"

# Testes com verbose output
pytest -v

# Executar apenas testes que falharam na última vez
pytest --lf
```

---

## 📈 Métricas e Relatórios

### Relatório de Cobertura
```bash
# Gerar relatório HTML
pytest --cov=src --cov-report=html
# Relatório disponível em htmlcov/index.html

# Relatório no terminal
pytest --cov=src --cov-report=term-missing
```

### Integração com CI/CD
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: pytest tests/unit/ --cov=src
      
      - name: Run integration tests
        run: pytest tests/integration/
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
```

---

## 🎯 Metas de Qualidade

### Critérios de Aceitação
- **✅ Unit Tests**: >85% cobertura (críticos: 100%)
- **✅ Integration Tests**: Todos os fluxos principais cobertos
- **✅ E2E Tests**: Cenários de usuário mais críticos
- **✅ Performance**: <500ms p95 response time
- **✅ Security**: Zero vulnerabilidades críticas
- **✅ Smoke Tests**: 100% success rate pós-deploy

### Processo de Quality Gate
```mermaid
graph TD
    A[Code Commit] --> B[Unit Tests]
    B --> C{>85% Coverage?}
    C -->|No| D[Block Merge]
    C -->|Yes| E[Integration Tests]
    E --> F{All Pass?}
    F -->|No| D
    F -->|Yes| G[Security Tests]
    G --> H{No Vulnerabilities?}
    H -->|No| D
    H -->|Yes| I[Merge Approved]
    I --> J[Deploy to Staging]
    J --> K[E2E Tests]
    K --> L{All Pass?}
    L -->|No| M[Rollback]
    L -->|Yes| N[Deploy to Production]
    N --> O[Smoke Tests]
```

---

**Esta estratégia de testes garante a qualidade e confiabilidade do sistema AUDITORIA360 em todos os níveis, desde componentes individuais até o sistema completo em produção.**