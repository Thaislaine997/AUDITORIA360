# tests/test_cct_upload.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_upload_cct_missing_file():
    response = client.post("/api/v1/ccts/upload", data={
        "nome_documento_original": "Teste CCT",
        "data_inicio_vigencia_cct": "2025-01-01"
    })
    assert response.status_code == 422  # campo file obrigatório

def test_upload_cct_success(monkeypatch, tmp_path):
    # Mock do controller para não chamar GCS/BQ reais
    async def mock_salvar(*args, **kwargs):
        return {
            "id_cct_documento": "uuid-teste",
            "nome_documento_original": "Teste CCT",
            "gcs_uri_documento": "gs://bucket/teste.pdf",
            "data_inicio_vigencia_cct": "2025-01-01",
            "data_fim_vigencia_cct": None,
            "sindicatos_laborais": None,
            "sindicatos_patronais": None,
            "status_processamento_ia": "PENDENTE_EXTRACAO"
        }
    monkeypatch.setattr("src.controllers.cct_controller.salvar_documento_cct_e_metadados", mock_salvar)

    file_path = tmp_path / "teste.pdf"
    file_path.write_bytes(b"%PDF-1.4 mock")
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/ccts/upload",
            data={
                "nome_documento_original": "Teste CCT",
                "data_inicio_vigencia_cct": "2025-01-01"
            },
            files={"file": ("teste.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id_cct_documento"] == "uuid-teste"

def test_upload_cct_invalid_file_type(monkeypatch, tmp_path):
    async def mock_salvar(*args, **kwargs):
        return {"id_cct_documento": "uuid-teste"}
    monkeypatch.setattr("src.controllers.cct_controller.salvar_documento_cct_e_metadados", mock_salvar)
    file_path = tmp_path / "teste.txt"
    file_path.write_text("arquivo texto")
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/ccts/upload",
            data={
                "nome_documento_original": "Teste CCT",
                "data_inicio_vigencia_cct": "2025-01-01"
            },
            files={"file": ("teste.txt", f, "text/plain")}
        )
    # Espera-se erro 422 pois só aceita PDF/DOCX
    assert response.status_code in (400, 422)

def test_upload_cct_missing_nome(monkeypatch, tmp_path):
    file_path = tmp_path / "teste.pdf"
    file_path.write_bytes(b"%PDF-1.4 mock")
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/ccts/upload",
            data={
                "data_inicio_vigencia_cct": "2025-01-01"
            },
            files={"file": ("teste.pdf", f, "application/pdf")}
        )
    assert response.status_code == 422

def test_upload_cct_invalid_date(monkeypatch, tmp_path):
    file_path = tmp_path / "teste.pdf"
    file_path.write_bytes(b"%PDF-1.4 mock")
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/ccts/upload",
            data={
                "nome_documento_original": "Teste CCT",
                "data_inicio_vigencia_cct": "data-invalida"
            },
            files={"file": ("teste.pdf", f, "application/pdf")}
        )
    assert response.status_code == 422