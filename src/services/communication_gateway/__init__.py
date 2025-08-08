"""
Communication Gateway Module for AUDITORIA360
Módulo 4: Gateway de Comunicação com padrão de provedores
"""

from .gateway import CommunicationGateway, create_default_gateway
from .github_integration import GitHubIntegrationService
from .providers import (
    CommunicationProviderInterface,
    EmailProvider,
    MessageStatus,
    MessageType,
    TwilioProvider,
)

__all__ = [
    "CommunicationProviderInterface",
    "EmailProvider",
    "TwilioProvider",
    "MessageType",
    "MessageStatus",
    "CommunicationGateway",
    "create_default_gateway",
    "GitHubIntegrationService",
]
