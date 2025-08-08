"""
Enhanced Notification Service using Communication Gateway
Serviço de notificações aprimorado usando o Gateway de Comunicação
"""

import logging
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from src.models.notification_models import (
    Notification,
    NotificationPriority,
    NotificationStatus,
    NotificationType,
)
from src.services.communication_gateway import (
    MessageStatus,
    MessageType,
    create_default_gateway,
)
from src.services.communication_gateway.github_integration import (
    GitHubIntegrationService,
)

logger = logging.getLogger(__name__)


class EnhancedNotificationService:
    """
    Serviço de notificações que utiliza o Communication Gateway
    Substitui gradualmente o sistema de notificações legado
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

        # Inicializa o gateway de comunicação
        self.gateway = create_default_gateway(self.config.get("providers", {}))

        # Inicializa integração com GitHub
        github_config = self.config.get("github", {})
        self.github_service = GitHubIntegrationService(github_config)

        logger.info("EnhancedNotificationService initialized")

    def send_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        destination: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        provider_name: Optional[str] = None,
        db: Optional[Session] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Envia notificação usando o gateway de comunicação

        Args:
            user_id: ID do usuário destinatário
            title: Título da notificação
            message: Conteúdo da mensagem
            notification_type: Tipo da notificação
            destination: Destino (email, telefone)
            priority: Prioridade da notificação
            provider_name: Provedor específico a usar
            db: Sessão do banco de dados
            **kwargs: Parâmetros adicionais

        Returns:
            Dict com resultado do envio
        """
        try:
            # Mapeia tipo de notificação para tipo de mensagem
            message_type = self._map_notification_type_to_message_type(
                notification_type
            )

            # Envia através do gateway
            result = self.gateway.send_message(
                to=destination,
                message=message,
                message_type=message_type,
                provider_name=provider_name,
                subject=title if message_type == MessageType.EMAIL else None,
                **kwargs,
            )

            # Salva no banco se sessão fornecida
            if db:
                notification_record = self._create_notification_record(
                    user_id=user_id,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    priority=priority,
                    result=result,
                )
                db.add(notification_record)
                db.commit()
                result["notification_id"] = notification_record.id

            logger.info(f"Notification sent successfully to {destination}")
            return result

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return {"status": MessageStatus.FAILED.value, "error": str(e)}

    def process_incoming_message(
        self, webhook_data: Dict[str, Any], provider_name: str = "twilio"
    ) -> Dict[str, Any]:
        """
        Processa mensagem recebida via webhook

        Args:
            webhook_data: Dados do webhook
            provider_name: Nome do provedor

        Returns:
            Dict com resultado do processamento
        """
        try:
            # Obtém o provedor
            provider = self.gateway.get_provider_by_name(provider_name)
            if not provider:
                raise ValueError(f"Provider {provider_name} not found")

            # Processa webhook específico do provedor
            if hasattr(provider, "process_webhook"):
                message_data = provider.process_webhook(webhook_data)
            else:
                message_data = webhook_data

            # Cria Issue no GitHub se configurado
            github_result = None
            if self.github_service.is_configured():
                github_result = self.github_service.create_issue_from_message(
                    message_data, provider_name
                )

            # Gera resposta automática
            response_data = None
            if github_result and github_result.get("success"):
                response_data = self.github_service.send_response_message(
                    github_result["issue_number"]
                )

                # Envia resposta se possível
                if provider_name == "twilio" and response_data:
                    self._send_auto_response(message_data, response_data)

            logger.info(f"Incoming message processed successfully from {provider_name}")

            return {
                "success": True,
                "message_data": message_data,
                "github_result": github_result,
                "response_data": response_data,
            }

        except Exception as e:
            logger.error(f"Failed to process incoming message: {e}")
            return {"success": False, "error": str(e)}

    def _send_auto_response(
        self, original_message: Dict[str, Any], response_data: Dict[str, Any]
    ) -> None:
        """Envia resposta automática para mensagem recebida"""
        try:
            from_number = original_message.get("from_number")
            message_type_str = original_message.get("type", "sms")
            response_message = response_data.get("response_message")

            if from_number and response_message:
                message_type = (
                    MessageType.WHATSAPP
                    if message_type_str == "whatsapp"
                    else MessageType.SMS
                )

                self.gateway.send_message(
                    to=from_number,
                    message=response_message,
                    message_type=message_type,
                    provider_name="twilio",
                )

                logger.info(f"Auto-response sent to {from_number}")

        except Exception as e:
            logger.error(f"Failed to send auto-response: {e}")

    def _map_notification_type_to_message_type(
        self, notification_type: NotificationType
    ) -> MessageType:
        """Mapeia tipo de notificação para tipo de mensagem do gateway"""
        mapping = {
            NotificationType.EMAIL: MessageType.EMAIL,
            NotificationType.SMS: MessageType.SMS,
            NotificationType.PUSH: MessageType.SYSTEM,
            NotificationType.SYSTEM: MessageType.SYSTEM,
        }
        return mapping.get(notification_type, MessageType.SYSTEM)

    def _create_notification_record(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        priority: NotificationPriority,
        result: Dict[str, Any],
    ) -> Notification:
        """Cria registro de notificação no banco de dados"""

        # Mapeia status do gateway para status da notificação
        gateway_status = result.get("status", "failed")
        if gateway_status == "sent":
            status = NotificationStatus.SENT
        elif gateway_status == "delivered":
            status = NotificationStatus.DELIVERED
        elif gateway_status == "failed":
            status = NotificationStatus.FAILED
        else:
            status = NotificationStatus.PENDING

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            priority=priority,
            status=status,
            external_id=result.get("external_id"),
            provider=result.get("provider"),
            error_message=result.get("error") if gateway_status == "failed" else None,
        )

        return notification

    def get_gateway_status(self) -> Dict[str, Any]:
        """
        Retorna status do gateway e provedores configurados

        Returns:
            Dict com informações de status
        """
        providers = self.gateway.get_available_providers()

        return {
            "gateway_initialized": True,
            "providers": providers,
            "github_configured": self.github_service.is_configured(),
            "total_providers": len(providers),
            "configured_providers": len([p for p in providers if p["configured"]]),
        }
