"""
Testes automatizados para o fluxo de sumarização e comparação de CCTs.
"""
import pytest
import asyncio
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_sumarizar_e_comparar_cct_textos_gcs(monkeypatch):
    # Mock BigQuery e GCS
    monkeypatch.setattr("scripts.test_cct_sumarizacao_comparacao.ler_texto_do_gcs", lambda gcs_uri: "Texto simulado da CCT para sumarização e comparação.")
    monkeypatch.setattr("scripts.test_cct_sumarizacao_comparacao.bq_client", MagicMock())
    from scripts.test_cct_sumarizacao_comparacao import sumarizar_e_comparar_cct_textos_gcs
    await sumarizar_e_comparar_cct_textos_gcs(
        id_cct_documento_atual="cct-teste-456",
        texto_atual_gcs_uri="gs://bucket-ccts-textos/cliente1/2025/cct-teste-456.txt",
        id_cct_base_referencia="cct-teste-123"
    )
    # Se não lançar exceção, passou
