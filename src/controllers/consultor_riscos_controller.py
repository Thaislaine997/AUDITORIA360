from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from src.database import get_db_session_context as get_db
from src.schemas_models import ConsultorRiscosRequest, ConsultorRiscosResponse, ChatMessage, ChatMessagePart
# Supondo que gemini_utils.py será criado em src.utils
# from src.utils.gemini_utils import chamar_gemini_para_consultoria_riscos 

# Mock para a função do Gemini até que ela seja implementada
async def chamar_gemini_para_consultoria_riscos_mock(
    id_cliente: str, 
    historico_chat: List[ChatMessage], 
    pergunta_atual: str
) -> str:
    """Mock da função que chama a API Gemini para obter insights."""
    # Simula uma análise simples e uma resposta baseada na pergunta
    if "previsões" in pergunta_atual.lower():
        return f"Para o cliente {id_cliente}, as últimas previsões indicam um risco moderado. Detalhes podem ser encontrados no painel de risco."
    elif "recomendações" in pergunta_atual.lower():
        return f"Com base nos dados do cliente {id_cliente}, recomendo revisar as políticas de férias e verificar as horas extras não compensadas."
    elif "simular" in pergunta_atual.lower():
        return f"A simulação de cenário para o cliente {id_cliente} ainda não está implementada, mas estou aprendendo!"
    else:
        return f"Entendido. Processando sua pergunta sobre '{pergunta_atual}' para o cliente {id_cliente}. Em breve terei mais informações."

class ConsultorRiscosController:
    async def processar_chat_consultor(
        self,
        id_cliente: str,
        request_data: ConsultorRiscosRequest, # Schema correto
        db: Session = Depends(get_db)
    ) -> ConsultorRiscosResponse: # Schema correto
        """
        Processa a mensagem do usuário, interage com o Gemini (ou mock) e retorna a resposta.
        """
        try:
            resposta_gemini = await chamar_gemini_para_consultoria_riscos_mock(
                id_cliente=id_cliente,
                historico_chat=request_data.historico_conversa_anterior, # nome correto
                pergunta_atual=request_data.pergunta_usuario # nome correto
            )

            nova_mensagem_assistente = ChatMessage(
                role="assistant",
                parts=[ChatMessagePart(text=resposta_gemini)]
            )
            historico_atualizado = list(request_data.historico_conversa_anterior)
            historico_atualizado.append(ChatMessage(role="user", parts=[ChatMessagePart(text=request_data.pergunta_usuario)]))
            historico_atualizado.append(nova_mensagem_assistente)

            return ConsultorRiscosResponse(
                resposta_consultor=resposta_gemini,
                partes_resposta=[ChatMessagePart(text=resposta_gemini)],
                historico_conversa_atualizado=historico_atualizado,
                dados_suporte=None
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# Instância do controller para ser usada nas rotas
consultor_riscos_controller = ConsultorRiscosController()
