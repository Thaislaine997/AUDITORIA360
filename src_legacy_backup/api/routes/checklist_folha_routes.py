# src/routes/checklist_folha_routes.py
from fastapi import APIRouter, Depends, HTTPException, Path, Body, Query
from typing import List, Dict, Any

from src.controllers.checklist_folha_controller import ChecklistFolhaController
from src.schemas.checklist_schemas import (
    ChecklistItemResponseSchema,
    ChecklistItemUpdateSchema,
)
from src.utils.auth_utils import User, get_current_active_user

router = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist",
    tags=["Checklist de Fechamento da Folha"],
    # dependencies=[Depends(get_current_active_user)] # Aplicar a todas as rotas do router
)

# Helper para instanciar o controller
async def get_checklist_controller(
    id_cliente: str = Path(...),
    id_folha_processada: str = Path(...),
    current_user: User = Depends(get_current_active_user)
) -> ChecklistFolhaController:
    # Validação básica para garantir que o usuário logado corresponde ao id_cliente da rota,
    # ou se é admin (se essa lógica for implementada no controller ou aqui)
    if not current_user.is_admin and current_user.client_id != id_cliente:
        raise HTTPException(status_code=403, detail="Acesso não autorizado a este cliente.")
    return ChecklistFolhaController(client_id=id_cliente, id_folha_processada=id_folha_processada, current_user=current_user)

@router.get(
    "/", 
    response_model=List[ChecklistItemResponseSchema],
    summary="Obter o checklist de fechamento da folha",
    description="Retorna a lista de itens do checklist para a folha processada especificada. Se não existir, cria com base nos itens padrão e dinâmicos."
)
async def get_checklist_da_folha(
    controller: ChecklistFolhaController = Depends(get_checklist_controller)
):
    return controller.get_checklist_folha() # Removido await

@router.put(
    "/{id_item_checklist}", 
    response_model=ChecklistItemResponseSchema,
    summary="Atualizar um item do checklist",
    description="Atualiza o status, notas ou responsável de um item específico do checklist."
)
async def update_item_do_checklist(
    id_item_checklist: str = Path(..., description="ID do item do checklist a ser atualizado"),
    item_update_data: ChecklistItemUpdateSchema = Body(...),
    controller: ChecklistFolhaController = Depends(get_checklist_controller),
    current_user: User = Depends(get_current_active_user) # Para pegar o usuário que está fazendo a alteração
):
    # O controller já usa self.current_user.username, mas podemos passar explicitamente se preferir.
    # Aqui, o current_user do Depends(get_current_active_user) é o mesmo que está no controller.
    updated_item = await controller.update_item_checklist_bd(
        id_item_checklist=id_item_checklist, 
        item_update_data=item_update_data, 
        usuario_responsavel=current_user.username
    )
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item do checklist não encontrado ou falha na atualização.")
    return updated_item

# --- Rotas para Funcionalidade 2.4.2 --- #
@router.get(
    "/dica-ia", # Alterado para não colidir com /{id_item_checklist} e ser mais específico
    response_model=Dict[str, Any], # Ou um schema Pydantic específico para a dica
    summary="Obter dica da IA para um item do checklist",
    description="Fornece dicas contextuais geradas por IA para um item específico do checklist."
)
async def get_dica_ia_para_item_checklist(
    id_item_checklist: str = Query(..., description="ID do item do checklist para o qual a dica é solicitada"),
    # Adicionar descricao_item como parâmetro opcional de query
    descricao_item: str = Query(None, description="Descrição atual do item (opcional, para IA usar a mais recente)"), 
    controller: ChecklistFolhaController = Depends(get_checklist_controller)
):
    return await controller.get_dica_ia_para_item(id_item_checklist, descricao_item_externa=descricao_item)


# --- Rota para Funcionalidade 2.4.3 (Marcar Folha como Fechada) --- #
# Esta rota fica fora do prefixo /checklist pois se refere à folha como um todo.
# Vamos criar um novo router ou adicionar ao controle_folha_routes.py.
# Por agora, vou criar um router separado para manter o foco.

router_folha_actions = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}",
    tags=["Ações da Folha"],
    # dependencies=[Depends(get_current_active_user)]
)

@router_folha_actions.post(
    "/marcar-fechada", 
    response_model=Dict[str, str], # Ex: {"message": "...", "novo_status_folha": "..."}
    summary="Marcar a folha como fechada pelo cliente",
    description="Permite ao cliente marcar a folha como fechada após a conclusão do checklist e resolução de pendências críticas."
)
async def marcar_folha_como_fechada_endpoint(
    controller: ChecklistFolhaController = Depends(get_checklist_controller),
    current_user: User = Depends(get_current_active_user)
):
    # A lógica de verificação de pendências críticas está dentro do controller.marcar_folha_como_fechada
    return await controller.marcar_folha_como_fechada(usuario_fechamento=current_user.username)

# Nota: Será necessário incluir router_folha_actions no main.py também.
