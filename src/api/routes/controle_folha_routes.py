from fastapi import APIRouter, UploadFile, File, Query, Depends, HTTPException
from src.controllers import controle_folha_controller
import pandas as pd
from typing import List, Dict
from src.utils.config_manager import get_current_config # Corrigido o caminho do import
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/folhas", tags=["Controle Folha"])

class FolhaControleItem(BaseModel):
    id_folha: str
    client_id: str
    nome_arquivo: str
    status: str

class FolhasResponse(BaseModel):
    items: List[FolhaControleItem]
    total: int
    page: int
    size: int

class ProcessarResponse(BaseModel):
    id_folha: str
    status: str
    mensagem: str

MOCK_FOLHAS_DB: Dict[str, List[FolhaControleItem]] = {
    "cliente_a": [
        FolhaControleItem(id_folha="folha_ctrl_1_a", client_id="cliente_a", nome_arquivo="controle_A_01.csv", status="Importado"),
        FolhaControleItem(id_folha="folha_ctrl_2_a", client_id="cliente_a", nome_arquivo="controle_A_02.csv", status="Pendente"),
    ],
    "cliente_b": [
        FolhaControleItem(id_folha="folha_ctrl_1_b", client_id="cliente_b", nome_arquivo="controle_B_01.csv", status="Importado"),
    ],
}

@router.post("/importar-csv/")
async def importar_csv(
    csv_file: UploadFile = File(...), 
    ano_referencia: int = Query(...), 
    mes_referencia: int = Query(...),
    config: dict = Depends(get_current_config)
):
    client_id = config.get("client_id")
    if not client_id:
        raise HTTPException(status_code=401, detail="Client ID não pôde ser determinado a partir da requisição.")

    try:
        new_id_folha = f"folha_ctrl_new_{len(MOCK_FOLHAS_DB.get(client_id, [])) + 1}_{client_id[:1]}"
        nova_folha = FolhaControleItem(
            id_folha=new_id_folha,
            client_id=client_id,
            nome_arquivo=csv_file.filename if csv_file.filename else "unknown.csv",
            status="Importado"
        )
        if client_id not in MOCK_FOLHAS_DB:
            MOCK_FOLHAS_DB[client_id] = []
        MOCK_FOLHAS_DB[client_id].append(nova_folha)
        
        return {"message": f"Arquivo {csv_file.filename} importado com sucesso para o cliente {client_id}", "id_folha": nova_folha.id_folha, "status": "Importado"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo CSV: {str(e)}")

@router.get("/", response_model=FolhasResponse)
async def listar_controle_folha(
    config: dict = Depends(get_current_config)
):
    client_id = config.get("client_id")
    if not client_id:
        raise HTTPException(status_code=500, detail="Client ID não encontrado na configuração após autenticação.")

    folhas_cliente = MOCK_FOLHAS_DB.get(str(client_id), [])
    items_filtrados = [item for item in folhas_cliente if item.client_id == client_id]

    return FolhasResponse(
        items=items_filtrados,
        total=len(items_filtrados),
        page=1,
        size=len(items_filtrados)
    )

@router.get("/{id_folha}", response_model=FolhaControleItem)
async def get_controle_folha_by_id(
    id_folha: str, 
    config: dict = Depends(get_current_config)
):
    client_id = config.get("client_id")
    if not client_id:
        raise HTTPException(status_code=500, detail="Client ID não encontrado na configuração após autenticação.")

    folhas_cliente = MOCK_FOLHAS_DB.get(str(client_id), [])
    for folha in folhas_cliente:
        if folha.id_folha == id_folha and folha.client_id == client_id:
            return folha
    raise HTTPException(status_code=404, detail=f"Folha de controle com ID {id_folha} não encontrada ou acesso não permitido.")

@router.post("/processar/{id_folha}", response_model=ProcessarResponse)
async def processar_folha(
    id_folha: str,
    config: dict = Depends(get_current_config)
):
    client_id = config.get("client_id")
    if not client_id:
        raise HTTPException(status_code=500, detail="Client ID não encontrado na configuração após autenticação.")

    folhas_cliente = MOCK_FOLHAS_DB.get(str(client_id), [])
    for i, folha in enumerate(folhas_cliente):
        if folha.id_folha == id_folha and folha.client_id == client_id:
            if folha.status != "Processada":
                updated_folha = folha.copy(update={"status": "Processada"})
                MOCK_FOLHAS_DB[str(client_id)][i] = updated_folha
                return ProcessarResponse(id_folha=id_folha, status="Processada", mensagem="Folha processada com sucesso.")
            else:
                return ProcessarResponse(id_folha=id_folha, status=folha.status, mensagem="Folha já foi processada.")
    
    raise HTTPException(status_code=404, detail=f"Folha com id {id_folha} não encontrada para o cliente {client_id}.")