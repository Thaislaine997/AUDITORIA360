# tests/integration/test_rls.py
""" 
Teste de isolamento multi-tenant (RLS).
Pré-requisitos: API rodando localmente (`make run` ou `uvicorn`), e usuários demo criados conforme README.
Este teste tenta criar um recurso sob a Contabilidade A e garante que Contabilidade B não consegue acessá-lo.
"""
import os
import requests

BASE = os.getenv("TEST_API_URL", "http://localhost:8000")

def login(email, password):
    r = requests.post(f"{BASE}/api/auth/login", json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()["access_token"]

def create_cliente(token, payload):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE}/api/contabilidade/clientes", json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

def get_cliente(token, cliente_id):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE}/api/contabilidade/clientes/{cliente_id}", headers=headers)

def test_rls_isolation():
    # credenciais demo — ajuste conforme seu env/local
    token_a = login("contab_a@demo.local", "demo123")
    token_b = login("contab_b@demo.local", "demo123")

    payload = {
        "nome": "Cliente Teste Isolamento",
        "cnpj": "00000000000191",
        "email_contato": "teste@cliente.local"
    }

    created = create_cliente(token_a, payload)
    cliente_id = created.get("id")
    assert cliente_id is not None

    # leitura com o mesmo tenant (deve retornar OK)
    r_ok = get_cliente(token_a, cliente_id)
    assert r_ok.status_code == 200

    # leitura com tenant diferente (deve ser 403 ou 404)
    r_bad = get_cliente(token_b, cliente_id)
    assert r_bad.status_code in (403, 404)
