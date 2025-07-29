import pytest

from src.schemas.checklist_schemas import (
    ChecklistFolhaSchema,
    ChecklistItemResponseSchema,
    ChecklistItemUpdateSchema,
)


def test_checklist_folha_schema():
    obj = ChecklistFolhaSchema(id="1", nome="Fechamento")
    assert obj.id == "1"
    assert obj.nome == "Fechamento"


def test_checklist_item_response_schema():
    obj = ChecklistItemResponseSchema(
        id="1", descricao="Validar INSS", status="pendente"
    )
    assert obj.status == "pendente"


def test_checklist_item_update_schema():
    obj = ChecklistItemUpdateSchema(
        status="feito", notas="OK", usuario_responsavel="João"
    )
    assert obj.status == "feito"
    assert obj.notas == "OK"
    assert obj.usuario_responsavel == "João"
