# src/routes/consultor_riscos_routes.py
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from typing import List

from src.schemas import ConsultorRiscosRequest, ConsultorRiscosResponse, ChatMessage, ChatMessagePart
from src.controllers.consultor_riscos_controller import consultor_riscos_controller
# from src.dependencies import get_current_user # Exemplo de dependência de autenticação

router = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/consultor-riscos",
    tags=["Consultor de Riscos com IA"],
    # dependencies=[Depends(get_current_user)], # Adicionar autenticação aqui
)

@router.post(
    "/chat",
    response_model=ConsultorRiscosResponse,
    summary="Interage com o Consultor de Riscos de IA",
    description="Envia uma pergunta do usuário para o consultor de riscos baseado em IA (Gemini) e recebe uma resposta contextualizada.",
    response_description="A resposta do consultor, incluindo o histórico atualizado do chat."
)
async def interagir_consultor_riscos(
    id_cliente: str = Path(..., description="ID do cliente para o qual a consulta está sendo feita.", example="cliente_xyz_123"),
    request_data: ConsultorRiscosRequest = Body(..., description="Dados da requisição contendo a pergunta atual e o histórico do chat.")
):
    """
    Endpoint para interação com o Consultor de Riscos.
    Recebe o ID do cliente, a pergunta atual do usuário e o histórico do chat.
    Retorna a resposta gerada pelo consultor e o histórico atualizado.
    """
    try:
        # Chama o método do controller para processar o chat
        response = await consultor_riscos_controller.processar_chat_consultor(
            id_cliente=id_cliente,
            request_data=request_data
        )
        return response
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions para que o FastAPI as manipule
        raise http_exc
    except Exception as e:
        # Logar a exceção (idealmente com um logger configurado)
        print(f"Erro inesperado no endpoint /chat do consultor: {e}") # Substituir por logging
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado ao processar sua solicitação: {str(e)}")

# Exemplo de como o histórico de chat pode ser estruturado (já definido em schemas.py)
# historico_exemplo = [
#     ChatMessage(role="user", parts=[ChatMessagePart(text="Olá, qual o risco da minha folha este mês?")]),
#     ChatMessage(role="assistant", parts=[ChatMessagePart(text="Para analisar o risco, preciso de alguns dados...")])
# ]
