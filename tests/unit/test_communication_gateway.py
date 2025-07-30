"""
Tests for Communication Gateway Module
Testes para o módulo de Gateway de Comunicação
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from src.services.communication_gateway.providers import (
    EmailProvider,
    TwilioProvider, 
    MessageType,
    MessageStatus
)
from src.services.communication_gateway.gateway import CommunicationGateway, create_default_gateway
from src.services.communication_gateway.github_integration import GitHubIntegrationService


class TestEmailProvider:
    """Tests for EmailProvider"""
    
    def test_email_provider_initialization(self):
        """Test EmailProvider initialization"""
        config = {"smtp_server": "smtp.example.com"}
        provider = EmailProvider(config)
        
        assert provider.get_provider_name() == "email"
        assert provider.is_configured() is True
        assert provider.config == config
    
    def test_email_provider_send_message_success(self):
        """Test successful email sending"""
        provider = EmailProvider()
        
        result = provider.send_message(
            to="test@example.com",
            message="Test message",
            message_type=MessageType.EMAIL,
            subject="Test Subject"
        )
        
        assert result["provider"] == "email"
        assert result["status"] == MessageStatus.SENT.value
        assert result["to"] == "test@example.com"
        assert result["subject"] == "Test Subject"
        assert "external_id" in result
    
    def test_email_provider_invalid_message_type(self):
        """Test EmailProvider with invalid message type"""
        provider = EmailProvider()
        
        with pytest.raises(ValueError, match="EmailProvider only supports EMAIL messages"):
            provider.send_message(
                to="test@example.com",
                message="Test message",
                message_type=MessageType.SMS
            )


class TestTwilioProvider:
    """Tests for TwilioProvider"""
    
    def test_twilio_provider_initialization(self):
        """Test TwilioProvider initialization"""
        config = {
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_sms": "+15551234567",
            "from_whatsapp": "whatsapp:+14155238886"
        }
        provider = TwilioProvider(config)
        
        assert provider.get_provider_name() == "twilio"
        assert provider.is_configured() is True
        assert provider.account_sid == "AC123"
        assert provider.auth_token == "token123"
    
    def test_twilio_provider_not_configured(self):
        """Test TwilioProvider without proper configuration"""
        config = {"account_sid": "AC123"}  # Missing auth_token
        provider = TwilioProvider(config)
        
        assert provider.is_configured() is False
    
    def test_twilio_provider_send_sms_success(self):
        """Test successful SMS sending via Twilio"""
        config = {
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_sms": "+15551234567"
        }
        provider = TwilioProvider(config)
        
        # Setup mock client
        mock_client = Mock()
        mock_message = Mock()
        mock_message.sid = "SM123456789"
        mock_message.status = "sent"
        mock_client.messages.create.return_value = mock_message
        
        # Directly set the mock client
        provider._client = mock_client
        
        result = provider.send_message(
            to="+5511999999999",
            message="Test SMS message",
            message_type=MessageType.SMS
        )
        
        assert result["provider"] == "twilio"
        assert result["status"] == MessageStatus.SENT.value
        assert result["external_id"] == "SM123456789"
        assert result["type"] == "sms"
        
        # Verify Twilio client was called correctly
        mock_client.messages.create.assert_called_once_with(
            body="Test SMS message",
            from_="+15551234567",
            to="+5511999999999"
        )
    
    def test_twilio_provider_send_whatsapp_success(self):
        """Test successful WhatsApp sending via Twilio"""
        config = {
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_whatsapp": "whatsapp:+14155238886"
        }
        provider = TwilioProvider(config)
        
        # Setup mock client
        mock_client = Mock()
        mock_message = Mock()
        mock_message.sid = "SM123456789"
        mock_message.status = "sent"
        mock_client.messages.create.return_value = mock_message
        
        # Directly set the mock client
        provider._client = mock_client
        
        result = provider.send_message(
            to="+5511999999999",
            message="Test WhatsApp message",
            message_type=MessageType.WHATSAPP
        )
        
        assert result["provider"] == "twilio"
        assert result["status"] == MessageStatus.SENT.value
        assert result["type"] == "whatsapp"
        
        # Verify Twilio client was called with whatsapp prefix
        mock_client.messages.create.assert_called_once_with(
            body="Test WhatsApp message",
            from_="whatsapp:+14155238886",
            to="whatsapp:+5511999999999"
        )
    
    def test_twilio_provider_invalid_message_type(self):
        """Test TwilioProvider with invalid message type"""
        config = {
            "account_sid": "AC123",
            "auth_token": "token123",
            "from_sms": "+15551234567"
        }
        provider = TwilioProvider(config)
        
        with pytest.raises(ValueError, match="TwilioProvider only supports SMS and WhatsApp"):
            provider.send_message(
                to="+5511999999999",
                message="Test message",
                message_type=MessageType.EMAIL
            )
    
    def test_twilio_webhook_processing(self):
        """Test webhook processing for incoming messages"""
        provider = TwilioProvider()
        
        webhook_data = {
            "From": "whatsapp:+5511999999999",
            "Body": "Hello from WhatsApp",
            "MessageSid": "SM123456789",
            "DateSent": "2024-01-01T12:00:00Z"
        }
        
        result = provider.process_webhook(webhook_data)
        
        assert result["provider"] == "twilio"
        assert result["message_sid"] == "SM123456789"
        assert result["from_number"] == "+5511999999999"  # whatsapp prefix removed
        assert result["body"] == "Hello from WhatsApp"
        assert result["type"] == "whatsapp"
        assert result["status"] == "received"


class TestCommunicationGateway:
    """Tests for CommunicationGateway"""
    
    def test_gateway_initialization(self):
        """Test gateway initialization"""
        gateway = CommunicationGateway()
        
        assert len(gateway.providers) == 0
        assert len(gateway.default_provider_by_type) == 0
    
    def test_register_provider(self):
        """Test provider registration"""
        gateway = CommunicationGateway()
        provider = EmailProvider()
        
        gateway.register_provider(provider, is_default_for=[MessageType.EMAIL])
        
        assert "email" in gateway.providers
        assert gateway.default_provider_by_type[MessageType.EMAIL] == "email"
    
    def test_send_message_with_default_provider(self):
        """Test sending message with default provider"""
        gateway = CommunicationGateway()
        provider = EmailProvider()
        gateway.register_provider(provider, is_default_for=[MessageType.EMAIL])
        
        result = gateway.send_message(
            to="test@example.com",
            message="Test message",
            message_type=MessageType.EMAIL,
            subject="Test Subject"
        )
        
        assert result["provider"] == "email"
        assert result["status"] == MessageStatus.SENT.value
    
    def test_send_message_with_specific_provider(self):
        """Test sending message with specific provider"""
        gateway = CommunicationGateway()
        email_provider = EmailProvider()
        gateway.register_provider(email_provider)
        
        result = gateway.send_message(
            to="test@example.com",
            message="Test message",
            message_type=MessageType.EMAIL,
            provider_name="email",
            subject="Test Subject"
        )
        
        assert result["provider"] == "email"
        assert result["status"] == MessageStatus.SENT.value
    
    def test_send_message_provider_not_found(self):
        """Test sending message with non-existent provider"""
        gateway = CommunicationGateway()
        
        result = gateway.send_message(
            to="test@example.com",
            message="Test message",
            message_type=MessageType.EMAIL,
            provider_name="nonexistent"
        )
        
        assert result["status"] == MessageStatus.FAILED.value
        assert "not found" in result["error"]
    
    def test_get_available_providers(self):
        """Test getting available providers info"""
        gateway = CommunicationGateway()
        email_provider = EmailProvider()
        gateway.register_provider(email_provider)
        
        providers = gateway.get_available_providers()
        
        assert len(providers) == 1
        assert providers[0]["name"] == "email"
        assert providers[0]["configured"] is True
        assert "email" in providers[0]["supports"]


class TestGitHubIntegrationService:
    """Tests for GitHubIntegrationService"""
    
    def test_github_service_initialization(self):
        """Test GitHub service initialization"""
        config = {
            "github_token": "ghp_123",
            "repo_owner": "testuser",
            "repo_name": "testrepo"
        }
        service = GitHubIntegrationService(config)
        
        assert service.is_configured() is True
        assert service.github_token == "ghp_123"
        assert service.repo_owner == "testuser"
        assert service.repo_name == "testrepo"
    
    def test_github_service_not_configured(self):
        """Test GitHub service without configuration"""
        service = GitHubIntegrationService()
        
        assert service.is_configured() is False
    
    @patch('src.services.communication_gateway.github_integration.requests.post')
    def test_create_issue_success(self, mock_post):
        """Test successful GitHub issue creation"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "number": 123,
            "html_url": "https://github.com/testuser/testrepo/issues/123"
        }
        mock_post.return_value = mock_response
        
        config = {
            "github_token": "ghp_123",
            "repo_owner": "testuser", 
            "repo_name": "testrepo"
        }
        service = GitHubIntegrationService(config)
        
        message_data = {
            "from_number": "+5511999999999",
            "body": "Test message",
            "type": "whatsapp",
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        result = service.create_issue_from_message(message_data, "twilio")
        
        assert result["success"] is True
        assert result["issue_number"] == 123
        assert "github.com" in result["issue_url"]
        
        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "repos/testuser/testrepo/issues" in call_args[0][0]
        
        # Check issue data
        issue_data = call_args[1]["json"]
        assert "Nova mensagem via Twilio" in issue_data["title"]
        assert "via-twilio-whatsapp" in issue_data["labels"]
    
    def test_get_labels_for_message(self):
        """Test label generation for different message types"""
        service = GitHubIntegrationService()
        
        # Test WhatsApp labels
        labels = service._get_labels_for_message("twilio", "whatsapp")
        assert "via-twilio-whatsapp" in labels
        assert "mensagem-recebida" in labels
        
        # Test SMS labels
        labels = service._get_labels_for_message("twilio", "sms")
        assert "via-twilio-sms" in labels
        assert "gateway-comunicacao" in labels
    
    def test_send_response_message(self):
        """Test response message generation"""
        service = GitHubIntegrationService()
        
        response = service.send_response_message(123)
        
        assert "Issue #123" in response["response_message"]
        assert response["issue_number"] == 123
        assert response["auto_generated"] is True


class TestCreateDefaultGateway:
    """Tests for default gateway factory"""
    
    def test_create_default_gateway_empty_config(self):
        """Test creating gateway with empty config"""
        gateway = create_default_gateway()
        
        providers = gateway.get_available_providers()
        assert len(providers) >= 1  # At least email provider
        
        # Check email provider is registered
        email_provider = gateway.get_provider_by_name("email")
        assert email_provider is not None
        assert isinstance(email_provider, EmailProvider)
    
    def test_create_default_gateway_with_twilio_config(self):
        """Test creating gateway with Twilio configuration"""
        config = {
            "twilio": {
                "account_sid": "AC123",
                "auth_token": "token123",
                "from_sms": "+15551234567"
            }
        }
        
        gateway = create_default_gateway(config)
        
        providers = gateway.get_available_providers()
        assert len(providers) == 2  # Email + Twilio
        
        # Check both providers are registered
        email_provider = gateway.get_provider_by_name("email")
        twilio_provider = gateway.get_provider_by_name("twilio")
        
        assert email_provider is not None
        assert twilio_provider is not None
        assert isinstance(twilio_provider, TwilioProvider)