"""
Communication Gateway - Central orchestrator for all communication providers
Gateway central para orquestração de todos os provedores de comunicação
"""

from typing import Dict, List, Optional, Any
from .providers import (
    CommunicationProviderInterface, 
    EmailProvider, 
    TwilioProvider,
    MessageType,
    MessageStatus
)
import logging

logger = logging.getLogger(__name__)


class CommunicationGateway:
    """
    Gateway central de comunicação que gerencia múltiplos provedores
    Implementa o padrão Strategy para seleção de provedores
    """
    
    def __init__(self):
        self.providers: Dict[str, CommunicationProviderInterface] = {}
        self.default_provider_by_type: Dict[MessageType, str] = {}
        logger.info("CommunicationGateway initialized")
    
    def register_provider(
        self, 
        provider: CommunicationProviderInterface,
        is_default_for: Optional[List[MessageType]] = None
    ) -> None:
        """
        Registra um provedor no gateway
        
        Args:
            provider: Instância do provedor
            is_default_for: Lista de tipos de mensagem para os quais este é o provedor padrão
        """
        provider_name = provider.get_provider_name()
        self.providers[provider_name] = provider
        
        if is_default_for:
            for msg_type in is_default_for:
                self.default_provider_by_type[msg_type] = provider_name
        
        logger.info(f"Provider {provider_name} registered successfully")
    
    def send_message(
        self,
        to: str,
        message: str,
        message_type: MessageType,
        provider_name: Optional[str] = None,
        subject: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Envia mensagem através do provedor apropriado
        
        Args:
            to: Destinatário
            message: Conteúdo da mensagem  
            message_type: Tipo da mensagem
            provider_name: Nome específico do provedor (opcional)
            subject: Assunto (para emails)
            **kwargs: Parâmetros adicionais
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # Determina qual provedor usar
            if provider_name:
                if provider_name not in self.providers:
                    raise ValueError(f"Provider {provider_name} not found")
                provider = self.providers[provider_name]
            else:
                # Usa provedor padrão para o tipo de mensagem
                default_provider_name = self.default_provider_by_type.get(message_type)
                if not default_provider_name:
                    raise ValueError(f"No default provider configured for {message_type}")
                provider = self.providers[default_provider_name]
            
            # Verifica se o provedor está configurado
            if not provider.is_configured():
                raise ValueError(f"Provider {provider.get_provider_name()} is not properly configured")
            
            # Envia a mensagem
            result = provider.send_message(
                to=to,
                message=message,
                message_type=message_type,
                subject=subject,
                **kwargs
            )
            
            logger.info(f"Message sent successfully via {provider.get_provider_name()}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {
                "status": MessageStatus.FAILED.value,
                "error": str(e),
                "provider": provider_name or "unknown"
            }
    
    def get_available_providers(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de provedores disponíveis e seus status
        
        Returns:
            Lista com informações dos provedores
        """
        providers_info = []
        for name, provider in self.providers.items():
            providers_info.append({
                "name": name,
                "configured": provider.is_configured(),
                "supports": self._get_supported_message_types(provider)
            })
        return providers_info
    
    def get_provider_by_name(self, name: str) -> Optional[CommunicationProviderInterface]:
        """
        Retorna provedor pelo nome
        
        Args:
            name: Nome do provedor
            
        Returns:
            Instância do provedor ou None se não encontrado
        """
        return self.providers.get(name)
    
    def _get_supported_message_types(self, provider: CommunicationProviderInterface) -> List[str]:
        """
        Determina quais tipos de mensagem um provedor suporta
        
        Args:
            provider: Instância do provedor
            
        Returns:
            Lista de tipos de mensagem suportados
        """
        if isinstance(provider, EmailProvider):
            return ["email"]
        elif isinstance(provider, TwilioProvider):
            return ["sms", "whatsapp"]
        else:
            return ["unknown"]


# Factory function para criar gateway pré-configurado
def create_default_gateway(config: Optional[Dict[str, Any]] = None) -> CommunicationGateway:
    """
    Cria um gateway com provedores padrão configurados
    
    Args:
        config: Configurações dos provedores
        
    Returns:
        Gateway configurado
    """
    gateway = CommunicationGateway()
    
    # Configuração padrão
    if config is None:
        config = {}
    
    # Registra EmailProvider como padrão para emails
    email_config = config.get("email", {})
    email_provider = EmailProvider(email_config)
    gateway.register_provider(email_provider, is_default_for=[MessageType.EMAIL])
    
    # Registra TwilioProvider se configurado
    twilio_config = config.get("twilio", {})
    if twilio_config:
        twilio_provider = TwilioProvider(twilio_config)
        if twilio_provider.is_configured():
            gateway.register_provider(
                twilio_provider, 
                is_default_for=[MessageType.SMS, MessageType.WHATSAPP]
            )
    
    return gateway