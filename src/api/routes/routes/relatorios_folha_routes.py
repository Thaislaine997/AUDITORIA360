# src/routes/relatorios_folha_routes.py
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from src.controllers import relatorios_folha_controller
from src.auth_utils import get_current_active_user, User # Importar User e get_current_active_user
import io

router = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/relatorios",
    tags=["Relatórios Folha"],
    dependencies=[Depends(get_current_active_user)] # Proteger todas as rotas neste router
)

@router.get("/{nome_relatorio}")
async def gerar_relatorio_folha(
    id_cliente: str, # Mantido para consistência de URL
    id_folha_processada: str,
    nome_relatorio: str, # Ex: "divergencias_completo", "conferencia_encargos"
    formato: str = Query(default="csv", enum=["csv", "xlsx"]),
    current_user: User = Depends(get_current_active_user) # Injetar usuário atual
):
    # Validar se o id_cliente da URL corresponde ao do usuário autenticado
    # Ou, se o usuário for um admin, permitir acesso a qualquer client_id.
    if not current_user.is_admin and current_user.client_id != id_cliente:
        raise HTTPException(status_code=403, detail=f"Acesso não autorizado ao cliente {id_cliente}")
    
    # Se for admin, usa o id_cliente da URL. Se não for admin, usa o client_id do token (que já foi validado).
    client_id_to_use = id_cliente if current_user.is_admin else current_user.client_id

    try:
        dados_relatorio_bytes, filename = await relatorios_folha_controller.gerar_e_formatar_relatorio(
            id_folha_processada=id_folha_processada,
            id_cliente=client_id_to_use, # Usar o client_id apropriado
            nome_relatorio=nome_relatorio,
            formato=formato
        )
    except HTTPException as e: # Repassa HTTPExceptions do controller
        raise e
    except Exception as e: # Captura outras exceções e retorna um 500 genérico
        # Logar o erro e.g. logging.error(f"Erro inesperado ao gerar relatório: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o relatório: {str(e)}")


    media_type = "text/csv" if formato == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        io.BytesIO(dados_relatorio_bytes),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
