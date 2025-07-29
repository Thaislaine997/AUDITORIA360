from src.schemas.folha_processada_schemas import FolhaProcessadaSelecaoSchema


def test_folha_processada_selecao_schema():
    obj = FolhaProcessadaSelecaoSchema(
        id_folha_processada="123",
        descricao_display="Folha Maio",
        periodo_referencia="2025-05",
        status_geral_folha="OK",
    )
    assert obj.id_folha_processada == "123"
    assert obj.status_geral_folha == "OK"
