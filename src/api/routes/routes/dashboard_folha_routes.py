# src/routes/dashboard_folha_routes.py
from fastapi import APIRouter, Depends, HTTPException
from src.controllers import dashboard_folha_controller
from src.schemas import DashboardSaudeFolhaResponse
from src.auth_utils import get_current_active_user, User # Importar User e get_current_active_user

router = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/dashboard-saude",
    tags=["Dashboard Folha"],
    dependencies=[Depends(get_current_active_user)] # Proteger todas as rotas neste router
)

@router.get("", response_model=DashboardSaudeFolhaResponse)
async def get_dashboard_saude_folha(
    id_cliente: str, # Mantido para consistência de URL, mas o id_cliente virá do token
    id_folha_processada: str,
    current_user: User = Depends(get_current_active_user) # Injetar usuário atual
):
    # Validar se o id_cliente da URL corresponde ao do usuário autenticado
    # Ou, se o usuário for um admin, permitir acesso a qualquer client_id.
    if not current_user.is_admin and current_user.client_id != id_cliente:
        raise HTTPException(status_code=403, detail=f"Acesso não autorizado ao cliente {id_cliente}")
    
    # Se for admin, usa o id_cliente da URL. Se não for admin, usa o client_id do token (que já foi validado).
    client_id_to_use = id_cliente if current_user.is_admin else current_user.client_id

    dashboard_data = await dashboard_folha_controller.gerar_dados_dashboard_saude(
        id_folha_processada=id_folha_processada,
        id_cliente=client_id_to_use 
    )
    if not dashboard_data:
        raise HTTPException(status_code=404, detail="Dados do dashboard não encontrados para a folha processada.")
    return dashboard_data
