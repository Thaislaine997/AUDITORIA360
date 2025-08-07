# /auditoria360/src/services/controle_mensal_service.py

from supabase import AsyncClient
from typing import List, Dict
import logging

TAREFAS_PADRAO = ["INFO_FOLHA", "ENVIO_CLIENTE", "GUIA_FGTS", "DARF_INSS", "ESOCIAL_DCTFWEB"]

class ControleMensalService:
    def __init__(self, supabase: AsyncClient):
        self.db = supabase

    async def obter_controles_por_mes_ano(self, ano: int, mes: int) -> List[Dict]:
        """Busca todos os controles mensais para um dado ano/mês, incluindo dados da empresa e tarefas."""
        logging.info(f"Buscando controles para {mes}/{ano}")

        # Usamos uma RPC (Remote Procedure Call) para fazer um JOIN mais complexo no Supabase
        # Esta função precisará ser criada na base de dados (ver Parte 4)
        response = await self.db.rpc('obter_controles_detalhados', {'p_ano': ano, 'p_mes': mes}).execute()

        if response.data is None:
            return []

        return response.data

    async def gerar_controles_para_mes_corrente(self) -> Dict:
        """Gera os registros de controle para todas as empresas ativas para o mês/ano corrente."""
        # Esta é uma função complexa. Vamos detalhá-la:
        # 1. Obter a data atual para pegar o mês e ano.
        # 2. Buscar todas as empresas com 'ativo = true'.
        # 3. Para cada empresa, verificar se já existe um controle para o mês/ano atual.
        # 4. Se não existir, criar um registro em 'ControlesMensais'.
        # 5. Para o novo controle, criar todas as 'TarefasControle' padrão.

        # Por simplicidade, vamos retornar um placeholder. A implementação completa virá no PR #3.
        logging.info("Iniciando a geração de controles para o mês corrente.")
        # Placeholder para a lógica
        num_empresas_ativas = (await self.db.from_("Empresas").select("id", count='exact').eq("ativo", True).execute()).count
        return {"message": f"Simulação: {num_empresas_ativas} empresas ativas encontradas. A lógica de geração será implementada.", "count": num_empresas_ativas}

    async def atualizar_status_tarefa(self, tarefa_id: int, concluido: bool) -> Dict:
        """Atualiza o status de uma tarefa e a data de conclusão."""
        from datetime import datetime, timezone

        update_data = {
            "concluido": concluido,
            "data_conclusao": datetime.now(timezone.utc).isoformat() if concluido else None
        }

        response = await self.db.from_("TarefasControle").update(update_data).eq("id", tarefa_id).execute()

        if not response.data:
            raise ValueError(f"Tarefa com ID {tarefa_id} não encontrada.")

        return response.data[0]