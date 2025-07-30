"""
Communication Provider Interface and Implementations
Padrão Adapter para diferentes provedores de comunicação
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class MessageType(Enum):
    EMAIL = "email"
    SMS = "sms" 
    WHATSAPP = "whatsapp"
    SYSTEM = "system"


class MessageStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class CommunicationProviderInterface(ABC):
    """Interface abstrata para provedores de comunicação"""
    
    @abstractmethod
    def send_message(
        self, 
        to: str, 
        message: str, 
        message_type: MessageType,
        subject: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Envia uma mensagem através do provedor
        
        Args:
            to: Destinatário (email, telefone, etc)
            message: Conteúdo da mensagem
            message_type: Tipo da mensagem
            subject: Assunto (opcional, usado para email)
            **kwargs: Parâmetros específicos do provedor
            
        Returns:
            Dict com status da operação e dados do provedor
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Retorna o nome do provedor"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Verifica se o provedor está configurado corretamente"""
        pass


class EmailProvider(CommunicationProviderInterface):
    """Provedor de email - encapsula lógica existente"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        logger.info("EmailProvider initialized")
    
    def send_message(
        self, 
        to: str, 
        message: str, 
        message_type: MessageType,
        subject: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Implementa envio de email"""
        if message_type != MessageType.EMAIL:
            raise ValueError(f"EmailProvider only supports EMAIL messages, got {message_type}")
        
        # TODO: Integrar com sistema de email existente
        # Por ora, simula o envio
        logger.info(f"Sending email to {to} with subject: {subject}")
        
        return {
            "provider": "email",
            "status": MessageStatus.SENT.value,
            "external_id": f"email_{hash(to + message)}", 
            "message": "Email sent successfully (mock)",
            "to": to,
            "subject": subject
        }
    
    def get_provider_name(self) -> str:
        return "email"
    
    def is_configured(self) -> bool:
        # TODO: Verificar configuração real do email
        return True


class TwilioProvider(CommunicationProviderInterface):
    """Provedor Twilio para SMS e WhatsApp"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._client = None
        
        # Configurações necessárias
        self.account_sid = self.config.get("account_sid")
        self.auth_token = self.config.get("auth_token") 
        self.from_whatsapp = self.config.get("from_whatsapp")  # formato: whatsapp:+14155238886
        self.from_sms = self.config.get("from_sms")  # formato: +15017122661
        
        logger.info("TwilioProvider initialized")
    
    @property
    def client(self):
        """Lazy loading do cliente Twilio"""
        if self._client is None and self.is_configured():
            try:
                from twilio.rest import Client
                self._client = Client(self.account_sid, self.auth_token)
            except ImportError:
                logger.error("Twilio library not installed")
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                raise
        return self._client
    
    def send_message(
        self, 
        to: str, 
        message: str, 
        message_type: MessageType,
        subject: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Implementa envio via Twilio"""
        if message_type not in [MessageType.SMS, MessageType.WHATSAPP]:
            raise ValueError(f"TwilioProvider only supports SMS and WhatsApp, got {message_type}")
        
        if not self.is_configured():
            raise ValueError("TwilioProvider is not properly configured")
        
        try:
            # Determina o número de origem baseado no tipo
            if message_type == MessageType.WHATSAPP:
                from_number = self.from_whatsapp
                to_number = f"whatsapp:{to}" if not to.startswith("whatsapp:") else to
            else:  # SMS
                from_number = self.from_sms
                to_number = to
            
            # Envia mensagem via Twilio
            twilio_message = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            logger.info(f"Message sent via Twilio: {twilio_message.sid}")
            
            return {
                "provider": "twilio",
                "status": MessageStatus.SENT.value,
                "external_id": twilio_message.sid,
                "message": "Message sent successfully via Twilio",
                "to": to,
                "type": message_type.value,
                "twilio_status": twilio_message.status
            }
            
        except Exception as e:
            logger.error(f"Failed to send message via Twilio: {e}")
            return {
                "provider": "twilio", 
                "status": MessageStatus.FAILED.value,
                "error": str(e),
                "to": to,
                "type": message_type.value
            }
    
    def get_provider_name(self) -> str:
        return "twilio"
    
    def is_configured(self) -> bool:
        """Verifica se todas as configurações necessárias estão presentes"""
        required_configs = ["account_sid", "auth_token"]
        has_required = all(self.config.get(key) for key in required_configs)
        
        # Precisa de pelo menos um número (SMS ou WhatsApp) 
        has_numbers = bool(self.from_sms or self.from_whatsapp)
        
        return has_required and has_numbers
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa webhook do Twilio para mensagens recebidas
        
        Args:
            webhook_data: Dados do webhook da Twilio
            
        Returns:
            Dict com dados processados da mensagem
        """
        try:
            # Extrai informações da mensagem recebida
            from_number = webhook_data.get("From", "")
            body = webhook_data.get("Body", "")
            message_sid = webhook_data.get("MessageSid", "")
            
            # Determina o tipo baseado no número
            is_whatsapp = from_number.startswith("whatsapp:")
            message_type = MessageType.WHATSAPP if is_whatsapp else MessageType.SMS
            
            # Limpa o prefixo whatsapp: se presente
            clean_number = from_number.replace("whatsapp:", "") if is_whatsapp else from_number
            
            logger.info(f"Received {message_type.value} message from {clean_number}: {body}")
            
            return {
                "provider": "twilio",
                "message_sid": message_sid,
                "from_number": clean_number,
                "body": body,
                "type": message_type.value,
                "timestamp": webhook_data.get("DateSent"),
                "status": "received"
            }
            
        except Exception as e:
            logger.error(f"Failed to process Twilio webhook: {e}")
            return {
                "provider": "twilio",
                "error": str(e),
                "status": "error"
            }