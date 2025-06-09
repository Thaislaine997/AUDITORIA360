from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from src.config_manager import get_current_config

router = APIRouter(
    prefix="/api/v1/auditorias",
    tags=["Auditorias e Filtros"],
)

class ContabilidadeOption(BaseModel):
    id: str
    nome: str

class AuditoriaItem(BaseModel):
    id_folha: str
    client_id: str
    nome_arquivo: str
    status: str

class AuditoriasResponse(BaseModel):
    items: List[AuditoriaItem]
    total: int
    page: int
    size: int

MOCK_AUDITORIAS_DB: Dict[str, List[AuditoriaItem]] = {
    "cliente_a": [
        AuditoriaItem(id_folha="folha1_a", client_id="cliente_a", nome_arquivo="folha_A_01.pdf", status="Concluída"),
        AuditoriaItem(id_folha="folha2_a", client_id="cliente_a", nome_arquivo="folha_A_02.xlsx", status="Em processamento"),
    ],
    "cliente_b": [
        AuditoriaItem(id_folha="folha1_b", client_id="cliente_b", nome_arquivo="folha_B_01.pdf", status="Pendente"),
    ],
}

@router.get("/", response_model=AuditoriasResponse)
async def get_auditorias(
    config: dict = Depends(get_current_config)
):
    client_id = config["client_id"]

    auditorias_cliente = MOCK_AUDITORIAS_DB.get(str(client_id), [])
    items_filtrados = [item for item in auditorias_cliente if item.client_id == client_id]
    
    return AuditoriasResponse(
        items=items_filtrados,
        total=len(items_filtrados),
        page=1,
        size=len(items_filtrados)
    )

@router.get("/{id_folha}", response_model=AuditoriaItem)
async def get_auditoria_por_id(
    id_folha: str,
    config: dict = Depends(get_current_config)
):
    client_id = config["client_id"]

    auditorias_cliente = MOCK_AUDITORIAS_DB.get(str(client_id), [])
    for auditoria in auditorias_cliente:
        if auditoria.id_folha == id_folha:
            return auditoria
    raise HTTPException(status_code=404, detail="Auditoria não encontrada ou acesso não permitido")

@router.get("/options/contabilidades", response_model=List[ContabilidadeOption])
async def get_contabilidades_options():
    return [
        ContabilidadeOption(id="1", nome="Contabilidade Mock 1"),
        ContabilidadeOption(id="2", nome="Contabilidade Mock 2"),
    ]

# Rotas adicionadas para POST, PUT, DELETE (mock)
class AuditoriaCreate(BaseModel):
    nome: str
    # Adicione outros campos necessários para criar uma auditoria

class AuditoriaUpdate(BaseModel):
    nome: str
    # Adicione outros campos que podem ser atualizados

@router.post("/", response_model=AuditoriaItem, status_code=201)
async def create_auditoria(
    auditoria_data: AuditoriaCreate,
    config: dict = Depends(get_current_config)
):
    client_id = config["client_id"]
    new_id = f"new_audit_{len(MOCK_AUDITORIAS_DB.get(client_id, [])) + 1}"
    new_auditoria = AuditoriaItem(
        id_folha=new_id,
        client_id=client_id,
        nome_arquivo=f"{auditoria_data.nome.replace(' ', '_')}.pdf", # Exemplo
        status="Pendente"
    )
    if client_id not in MOCK_AUDITORIAS_DB:
        MOCK_AUDITORIAS_DB[client_id] = []
    MOCK_AUDITORIAS_DB[client_id].append(new_auditoria)
    return new_auditoria

@router.put("/{id_folha}", response_model=AuditoriaItem)
async def update_auditoria(
    id_folha: str,
    auditoria_data: AuditoriaUpdate,
    config: dict = Depends(get_current_config)
):
    client_id = config["client_id"]
    auditorias_cliente = MOCK_AUDITORIAS_DB.get(client_id, [])
    for i, auditoria in enumerate(auditorias_cliente):
        if auditoria.id_folha == id_folha:
            # Atualização simples de mock - apenas nome do arquivo como exemplo
            updated_item = auditoria.copy(update={"nome_arquivo": f"{auditoria_data.nome.replace(' ', '_')}_updated.pdf", "status": "Atualizada"})
            auditorias_cliente[i] = updated_item
            MOCK_AUDITORIAS_DB[client_id] = auditorias_cliente
            return updated_item
    raise HTTPException(status_code=404, detail="Auditoria não encontrada ou acesso não permitido")

@router.delete("/{id_folha}", status_code=204)
async def delete_auditoria(
    id_folha: str,
    config: dict = Depends(get_current_config)
):
    client_id = config["client_id"]
    auditorias_cliente = MOCK_AUDITORIAS_DB.get(client_id, [])
    for i, auditoria in enumerate(auditorias_cliente):
        if auditoria.id_folha == id_folha:
            del MOCK_AUDITORIAS_DB[client_id][i]
            return
    raise HTTPException(status_code=404, detail="Auditoria não encontrada ou acesso não permitido")
