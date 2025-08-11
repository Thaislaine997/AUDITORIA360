"""
NotificacaoService - The "Digital Nervous System" of AUDITORIA360
Implementation of Phase 3 from the Grand Tomo Architecture

This service implements an event-driven notification system that proactively
communicates with users before they even realize they need help.
"""

import asyncio
import json
import logging
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID

from portal_demandas.db import (
    get_db,
    LogOperacoesDB,
    NotificacoesDB,
    AlertasPrazosDB,
    AtendimentosSuporteDB,
    AtendimentosSuporteInteracoesDB
)

logger = logging.getLogger(__name__)


class NotificacaoService:
    """
    🔔 The "Proactive Communication Engine"
    
    This service creates a system that:
    1. Listens to database events via PostgreSQL NOTIFY
    2. Creates intelligent notifications based on system events
    3. Manages deadline alerts and proactive warnings
    4. Provides integrated support ticket management
    
    Philosophy: Communicate before problems become crises,
    and offer help before users ask for it.
    """
    
    def __init__(self):
        self.notification_queue = asyncio.Queue()
        
    async def servico_notificador(self, event_payload: Dict[str, Any]):
        """
        Event-driven notification orchestrator
        
        This is the central nervous system that listens to all database events
        and decides what notifications need to be created.
        
        Args:
            event_payload: Event data from PostgreSQL NOTIFY
        """
        logger.info(f"🎯 Processando evento de notificação: {event_payload.get('type')}")
        
        try:
            event_type = event_payload.get("tipo")
            dados = event_payload.get("dados", {})
            
            # Route events to appropriate handlers
            if event_type == 'AUDITORIA_FOLHA_CONCLUIDA':
                await self._handle_auditoria_concluida(dados)
            elif event_type == 'VENCIMENTO_CCT_PROXIMO':
                await self._handle_vencimento_cct(dados)
            elif event_type == 'DIVERGENCIA_FISCAL_DETECTADA':
                await self._handle_divergencia_fiscal(dados)
            elif event_type == 'REGRAS_PUBLICADAS':
                await self._handle_regras_publicadas(dados)
            elif event_type == 'PROCESSAMENTO_DOCUMENTO_ERRO':
                await self._handle_erro_processamento(dados)
            else:
                logger.warning(f"⚠️ Tipo de evento não reconhecido: {event_type}")
                
        except Exception as e:
            logger.error(f"❌ Erro no serviço de notificações: {e}")
    
    async def _handle_auditoria_concluida(self, dados: Dict[str, Any]):
        """
        Handle payroll audit completion events
        
        Creates notifications based on audit results and severity
        """
        logger.info("📊 Processando conclusão de auditoria de folha")
        
        with next(get_db()) as db:
            try:
                status_auditoria = dados.get("status", "")
                divergencias = dados.get("divergencias", [])
                empresa_id = dados.get("empresa_id")
                responsavel_id = dados.get("responsavel_id")
                
                # Determine notification type based on audit results
                if "CRITICO" in status_auditoria or any("CRITICO" in str(d) for d in divergencias):
                    # Critical issues - high priority notification
                    await self._criar_notificacao(
                        db,
                        usuario_id=responsavel_id,
                        tipo_notificacao='ALERTA',
                        titulo='🚨 Divergências Críticas na Folha de Pagamento',
                        mensagem=f"A auditoria da empresa encontrou {len(divergencias)} divergências críticas que requerem ação imediata.",
                        link_acao=f"/auditoria/folha/{dados.get('processamento_id')}",
                        prioridade='CRITICA',
                        origem_notificacao='AUDITORIA_ENGINE'
                    )
                    
                    # Also create deadline alert for resolution
                    await self._criar_alerta_prazo(
                        db,
                        empresa_id=empresa_id,
                        tipo_prazo='CORRECAO_AUDITORIA_CRITICA',
                        descricao='Correção de divergências críticas na folha',
                        data_vencimento=date.today() + timedelta(days=2),
                        dias_antecedencia=1,
                        referencia_id=dados.get('processamento_id'),
                        tipo_referencia='ProcessamentosFolha'
                    )
                    
                elif len(divergencias) > 0:
                    # Regular issues - medium priority
                    await self._criar_notificacao(
                        db,
                        usuario_id=responsavel_id,
                        tipo_notificacao='ALERTA',
                        titulo='⚠️ Divergências Encontradas na Auditoria',
                        mensagem=f"A auditoria encontrou {len(divergencias)} divergências que precisam ser analisadas.",
                        link_acao=f"/auditoria/folha/{dados.get('processamento_id')}",
                        prioridade='ALTA',
                        origem_notificacao='AUDITORIA_ENGINE'
                    )
                else:
                    # Clean audit - success notification
                    await self._criar_notificacao(
                        db,
                        usuario_id=responsavel_id,
                        tipo_notificacao='SUCESSO',
                        titulo='✅ Auditoria de Folha Concluída com Sucesso',
                        mensagem='A auditoria não encontrou divergências. Folha está em conformidade.',
                        link_acao=f"/auditoria/folha/{dados.get('processamento_id')}",
                        prioridade='MEDIA',
                        origem_notificacao='AUDITORIA_ENGINE'
                    )
                
                db.commit()
                logger.info("✅ Notificações de auditoria criadas com sucesso")
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro ao processar auditoria concluída: {e}")
    
    async def _handle_vencimento_cct(self, dados: Dict[str, Any]):
        """
        Handle CCT expiration alerts
        """
        logger.info("📅 Processando vencimento de CCT")
        
        with next(get_db()) as db:
            try:
                cct_id = dados.get("cct_id")
                empresa_id = dados.get("empresa_id")
                data_vencimento = dados.get("data_vencimento")
                
                # Find responsible users for the company
                responsaveis = self._obter_responsaveis_empresa(db, empresa_id)
                
                for responsavel_id in responsaveis:
                    await self._criar_notificacao(
                        db,
                        usuario_id=responsavel_id,
                        tipo_notificacao='ALERTA',
                        titulo='📋 Convenção Coletiva Próxima do Vencimento',
                        mensagem=f'A CCT da empresa vence em {data_vencimento}. É necessário verificar renovação ou nova negociação.',
                        link_acao=f"/cct/{cct_id}",
                        prioridade='ALTA',
                        origem_notificacao='CCT_MONITOR'
                    )
                
                db.commit()
                logger.info("📋 Alertas de vencimento de CCT enviados")
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro ao processar vencimento CCT: {e}")
    
    async def _handle_divergencia_fiscal(self, dados: Dict[str, Any]):
        """
        Handle tax declaration divergence alerts
        """
        logger.info("💰 Processando divergência fiscal detectada")
        
        with next(get_db()) as db:
            try:
                empresa_id = dados.get("empresa_id")
                tipo_divergencia = dados.get("tipo_divergencia")
                valor_diferenca = dados.get("valor_diferenca")
                
                responsaveis = self._obter_responsaveis_empresa(db, empresa_id)
                
                for responsavel_id in responsaveis:
                    await self._criar_notificacao(
                        db,
                        usuario_id=responsavel_id,
                        tipo_notificacao='ERRO',
                        titulo='🚨 Divergência Fiscal Detectada',
                        mensagem=f'Detectada divergência do tipo {tipo_divergencia} no valor de R$ {valor_diferenca}. Verificação urgente necessária.',
                        link_acao=f"/declaracoes-fiscais/{empresa_id}",
                        prioridade='CRITICA',
                        origem_notificacao='FISCAL_CROSS_REFERENCE'
                    )
                
                db.commit()
                logger.info("💰 Alertas de divergência fiscal enviados")
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro ao processar divergência fiscal: {e}")
    
    async def _handle_regras_publicadas(self, dados: Dict[str, Any]):
        """
        Handle business rules publication notifications
        """
        logger.info("📚 Processando publicação de regras")
        
        with next(get_db()) as db:
            try:
                documento_id = dados.get("documento_id")
                total_regras = dados.get("total_regras")
                contabilidade_id = dados.get("contabilidade_id")
                
                # Notify all users in the contabilidade
                usuarios_contabilidade = self._obter_usuarios_contabilidade(db, contabilidade_id)
                
                for usuario_id in usuarios_contabilidade:
                    await self._criar_notificacao(
                        db,
                        usuario_id=usuario_id,
                        tipo_notificacao='INFO',
                        titulo='📖 Nova Base de Conhecimento Disponível',
                        mensagem=f'Foram publicadas {total_regras} novas regras de negócio na base de conhecimento.',
                        link_acao=f"/conhecimento/documento/{documento_id}",
                        prioridade='MEDIA',
                        origem_notificacao='KNOWLEDGE_BASE'
                    )
                
                db.commit()
                logger.info("📚 Notificações de regras publicadas enviadas")
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro ao processar publicação de regras: {e}")
    
    async def _handle_erro_processamento(self, dados: Dict[str, Any]):
        """
        Handle document processing errors
        """
        logger.info("⚠️ Processando erro de processamento de documento")
        
        with next(get_db()) as db:
            try:
                documento_id = dados.get("documento_id")
                erro_mensagem = dados.get("erro_mensagem")
                usuario_id = dados.get("usuario_id")
                
                await self._criar_notificacao(
                    db,
                    usuario_id=usuario_id,
                    tipo_notificacao='ERRO',
                    titulo='❌ Erro no Processamento de Documento',
                    mensagem=f'Falha no processamento do documento: {erro_mensagem}',
                    link_acao=f"/documentos/{documento_id}",
                    prioridade='ALTA',
                    origem_notificacao='DOCUMENT_PROCESSOR'
                )
                
                # Automatically create support ticket for processing errors
                await self._criar_ticket_suporte_automatico(
                    db,
                    contabilidade_id=dados.get("contabilidade_id"),
                    usuario_solicitante=usuario_id,
                    assunto=f"Erro no processamento de documento {documento_id}",
                    descricao=f"Erro automático reportado: {erro_mensagem}",
                    categoria='TECNICO',
                    prioridade='ALTA'
                )
                
                db.commit()
                logger.info("⚠️ Erro de processamento tratado com notificação e ticket")
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro ao processar erro de processamento: {e}")
    
    async def monitorar_prazos(self):
        """
        Monitor deadlines and create proactive alerts
        
        This method runs periodically to check for upcoming deadlines
        and create alerts before they become critical.
        """
        logger.info("⏰ Executando monitoramento de prazos")
        
        with next(get_db()) as db:
            try:
                # Get all active alerts that are approaching their deadline
                alertas_proximos = self._obter_alertas_proximos(db)
                
                for alerta in alertas_proximos:
                    # Check if we should trigger the alert
                    if self._deve_disparar_alerta(alerta):
                        await self._disparar_alerta_prazo(db, alerta)
                
                db.commit()
                logger.info(f"⏰ Monitoramento concluído: {len(alertas_proximos)} alertas processados")
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro no monitoramento de prazos: {e}")
    
    async def criar_ticket_suporte(
        self,
        contabilidade_id: int,
        usuario_solicitante: UUID,
        assunto: str,
        descricao: str,
        categoria: str = 'GERAL',
        prioridade: str = 'MEDIA'
    ) -> Dict[str, Any]:
        """
        Create a new support ticket
        """
        logger.info(f"🎫 Criando ticket de suporte: {assunto}")
        
        with next(get_db()) as db:
            try:
                # Generate ticket number
                numero_ticket = self._gerar_numero_ticket(db)
                
                # Create the ticket
                ticket = AtendimentosSuporteDB(
                    contabilidade_id=contabilidade_id,
                    usuario_solicitante=usuario_solicitante,
                    numero_ticket=numero_ticket,
                    assunto=assunto,
                    descricao=descricao,
                    categoria=categoria,
                    prioridade=prioridade,
                    status='ABERTO'
                )
                
                db.add(ticket)
                db.flush()  # Get the ID
                
                # Create initial interaction
                interacao = AtendimentosSuporteInteracoesDB(
                    atendimento_id=ticket.id,
                    usuario_id=usuario_solicitante,
                    tipo_interacao='COMENTARIO',
                    conteudo=f"Ticket criado: {descricao}",
                    visivel_cliente=True
                )
                
                db.add(interacao)
                db.commit()
                
                logger.info(f"✅ Ticket {numero_ticket} criado com sucesso")
                
                return {
                    "ticket_id": ticket.id,
                    "numero_ticket": numero_ticket,
                    "status": "created",
                    "link": f"/suporte/ticket/{ticket.id}"
                }
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro ao criar ticket: {e}")
                raise e
    
    # ========== PRIVATE HELPER METHODS ==========
    
    async def _criar_notificacao(
        self,
        db,
        usuario_id: UUID,
        tipo_notificacao: str,
        titulo: str,
        mensagem: str,
        link_acao: Optional[str] = None,
        prioridade: str = 'MEDIA',
        origem_notificacao: Optional[str] = None
    ):
        """Create a notification in the database"""
        notificacao = NotificacoesDB(
            usuario_id=usuario_id,
            tipo_notificacao=tipo_notificacao,
            titulo=titulo,
            mensagem=mensagem,
            link_acao=link_acao,
            prioridade=prioridade,
            origem_notificacao=origem_notificacao
        )
        
        db.add(notificacao)
        logger.info(f"📱 Notificação criada: {titulo}")
    
    async def _criar_alerta_prazo(
        self,
        db,
        empresa_id: int,
        tipo_prazo: str,
        descricao: str,
        data_vencimento: date,
        dias_antecedencia: int,
        referencia_id: Optional[int] = None,
        tipo_referencia: Optional[str] = None
    ):
        """Create a deadline alert"""
        alerta = AlertasPrazosDB(
            empresa_id=empresa_id,
            tipo_prazo=tipo_prazo,
            descricao=descricao,
            data_vencimento=data_vencimento,
            dias_antecedencia=dias_antecedencia,
            referencia_id=referencia_id,
            tipo_referencia=tipo_referencia
        )
        
        db.add(alerta)
        logger.info(f"⏰ Alerta de prazo criado: {descricao}")
    
    async def _criar_ticket_suporte_automatico(
        self,
        db,
        contabilidade_id: int,
        usuario_solicitante: UUID,
        assunto: str,
        descricao: str,
        categoria: str,
        prioridade: str
    ):
        """Create an automatic support ticket"""
        numero_ticket = self._gerar_numero_ticket(db)
        
        ticket = AtendimentosSuporteDB(
            contabilidade_id=contabilidade_id,
            usuario_solicitante=usuario_solicitante,
            numero_ticket=numero_ticket,
            assunto=f"[AUTO] {assunto}",
            descricao=f"Ticket criado automaticamente pelo sistema:\n\n{descricao}",
            categoria=categoria,
            prioridade=prioridade,
            status='ABERTO',
            tags=['automatico', 'sistema']
        )
        
        db.add(ticket)
        logger.info(f"🤖 Ticket automático criado: {numero_ticket}")
    
    def _obter_responsaveis_empresa(self, db, empresa_id: int) -> List[UUID]:
        """Get responsible users for a company"""
        # In real implementation, query the database for company responsibles
        # For now, return mock data
        return [UUID('12345678-1234-5678-9012-123456789012')]
    
    def _obter_usuarios_contabilidade(self, db, contabilidade_id: int) -> List[UUID]:
        """Get all users from a contabilidade"""
        # In real implementation, query profiles table
        # For now, return mock data
        return [UUID('12345678-1234-5678-9012-123456789012')]
    
    def _obter_alertas_proximos(self, db) -> List:
        """Get alerts that are approaching their deadline"""
        # In real implementation, query AlertasPrazos table
        # For now, return empty list
        return []
    
    def _deve_disparar_alerta(self, alerta) -> bool:
        """Check if an alert should be triggered"""
        # In real implementation, check dates and last trigger
        return False
    
    async def _disparar_alerta_prazo(self, db, alerta):
        """Trigger a deadline alert"""
        logger.info(f"⚠️ Disparando alerta de prazo: {alerta.descricao}")
    
    def _gerar_numero_ticket(self, db) -> str:
        """Generate sequential ticket number"""
        # In real implementation, use sequence or counter
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"TK{timestamp}"


# Singleton instance for the application
notificacao_service = NotificacaoService()