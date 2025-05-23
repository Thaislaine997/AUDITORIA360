"""
Rotas para o auto-registro e login de Contabilidades.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

from src.controllers.contabilidade_controller import (
    registrar_nova_contabilidade_e_usuario,
    login_para_token_acesso,
    get_current_active_user,
    get_usuario_contabilidade_completo_por_id, # Nova importação
    listar_clientes_vinculados_por_contabilidade
)
from src.schemas import (
    RegistroContabilidadePayload,
    RegistroContabilidadeResponse,
    Token,
    TokenData,
    UsuarioContabilidadeResponse, # Para o endpoint de "me"
    EmpresaClienteSimplificado
)

router = APIRouter(
    prefix="/contabilidades",
    tags=["Contabilidades"],
)

@router.post("/registrar", 
              response_model=RegistroContabilidadeResponse, 
              status_code=status.HTTP_201_CREATED,
              summary="Registra uma nova contabilidade e seu primeiro usuário",
              description="Permite que uma nova empresa de contabilidade se cadastre no sistema, juntamente com um usuário administrador inicial."
)
async def registrar_contabilidade(payload: RegistroContabilidadePayload):
    try:
        return registrar_nova_contabilidade_e_usuario(payload)
    except HTTPException as e:
        raise e
    except Exception as e:
        # Logar a exceção e retornar um erro genérico
        print(f"Erro inesperado durante o registro da contabilidade: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao processar o registro. Tente novamente mais tarde."
        )

@router.post("/login/token", 
              response_model=Token,
              summary="Login para Contabilidades",
              description="Autentica um usuário de contabilidade e retorna um token JWT de acesso."
)
async def login_contabilidade_obter_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_para_token_acesso(form_data)

@router.get("/me", 
            response_model=UsuarioContabilidadeResponse, # Alterado para TokenData para incluir mais infos
            summary="Obtém informações do usuário logado",
            description="Retorna informações detalhadas sobre o usuário da contabilidade atualmente autenticado."
)
async def ler_usuario_contabilidade_logado(current_user: TokenData = Depends(get_current_active_user)):
    usuario_completo = get_usuario_contabilidade_completo_por_id(current_user.id_usuario_contabilidade)
    if not usuario_completo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado no banco de dados")
    return usuario_completo

@router.get("/me/clientes",
            response_model=list[EmpresaClienteSimplificado],
            summary="Lista empresas clientes vinculadas à contabilidade logada",
            description="Retorna uma lista simplificada das empresas clientes vinculadas à contabilidade do usuário autenticado.")
async def listar_clientes_vinculados(current_user: TokenData = Depends(get_current_active_user)):
    if not current_user.id_contabilidade:
        raise HTTPException(status_code=401, detail="Usuário sem contabilidade associada.")
    return listar_clientes_vinculados_por_contabilidade(current_user.id_contabilidade)
