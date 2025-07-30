"""
Communication Gateway Module for AUDITORIA360
Módulo 4: Gateway de Comunicação com padrão de provedores
"""

from .providers import CommunicationProviderInterface, EmailProvider, TwilioProvider, MessageType, MessageStatus
from .gateway import CommunicationGateway, create_default_gateway
from .github_integration import GitHubIntegrationService

__all__ = [
    "CommunicationProviderInterface",
    "EmailProvider", 
    "TwilioProvider",
    "MessageType",
    "MessageStatus",
    "CommunicationGateway",
    "create_default_gateway",
    "GitHubIntegrationService"
]