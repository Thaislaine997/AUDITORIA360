"""
Notifications and Events API Router
Módulo 4: Notificações e Eventos
Enhanced with real-time notification system and Communication Gateway
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import logging

from src.models import get_db
from src.services.enhanced_notification_service import EnhancedNotificationService

logger = logging.getLogger(__name__)

# Mock User for testing without auth
class MockUser:
    def __init__(self):
        self.id = 1
        self.role = "contabilidade"
        self.username = "test_user"

def get_current_user_mock():
    """Mock current user for testing"""
    return MockUser()

router = APIRouter()


# Pydantic models for request/response
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    priority: str
    status: str
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    created_at: str
    read_at: Optional[str] = None

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str = "system"
    priority: str = "medium"
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    user_ids: List[int] = []


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """List user notifications"""
    # TODO: Implement actual database query
    # For now, return sample notifications based on user profile
    sample_notifications = []
    
    # Super Admin notifications
    if hasattr(current_user, 'role') and current_user.role == "super_admin":
        sample_notifications.extend([
            {
                "id": 1,
                "title": "Nova Contabilidade Cadastrada",
                "message": "A contabilidade 'Escritório Santos & Associados' se cadastrou na plataforma",
                "type": "system",
                "priority": "medium",
                "status": "pending" if unread_only else "pending",
                "action_url": "/admin/contabilidades/123",
                "action_text": "Ver Detalhes",
                "created_at": "2024-01-10T09:30:00Z",
                "read_at": None
            }
        ])
    
    # Contabilidade notifications
    if hasattr(current_user, 'role') and current_user.role == "contabilidade":
        sample_notifications.extend([
            {
                "id": 2,
                "title": "Novo Documento Recebido",
                "message": "Cliente 'Empresa ABC Ltda' enviou um novo documento: Nota Fiscal 001.pdf",
                "type": "system",
                "priority": "high",
                "status": "pending",
                "action_url": "/documents/456",
                "action_text": "Ver Documento",
                "created_at": "2024-01-10T14:15:00Z",
                "read_at": None
            },
            {
                "id": 3,
                "title": "Comentário Recebido",
                "message": "Cliente 'XYZ Comércio' deixou um comentário no relatório mensal",
                "type": "system",
                "priority": "medium",
                "status": "pending",
                "action_url": "/reports/789#comments",
                "action_text": "Ver Comentário",
                "created_at": "2024-01-10T11:45:00Z",
                "read_at": None
            }
        ])
    
    # Cliente Final notifications
    if hasattr(current_user, 'role') and current_user.role == "cliente":
        sample_notifications.extend([
            {
                "id": 4,
                "title": "Relatório Gerado",
                "message": "Sua contabilidade gerou o relatório financeiro de dezembro/2023",
                "type": "system",
                "priority": "medium",
                "status": "pending",
                "action_url": "/reports/101",
                "action_text": "Ver Relatório",
                "created_at": "2024-01-10T16:20:00Z",
                "read_at": None
            },
            {
                "id": 5,
                "title": "Aviso da Contabilidade",
                "message": "Documentos pendentes para fechamento da folha de janeiro",
                "type": "system",
                "priority": "high",
                "status": "pending",
                "action_url": "/documents/pending",
                "action_text": "Ver Pendências",
                "created_at": "2024-01-10T08:00:00Z",
                "read_at": None
            }
        ])
    
    return sample_notifications[:limit]


@router.get("/unread-count")
async def get_unread_count(
    current_user: MockUser = Depends(get_current_user_mock),
):
    """Get count of unread notifications for header badge"""
    # TODO: Implement actual database query
    # Mock data based on user role
    unread_count = 0
    
    if hasattr(current_user, 'role'):
        if current_user.role == "super_admin":
            unread_count = 1
        elif current_user.role == "contabilidade":
            unread_count = 2
        elif current_user.role == "cliente":
            unread_count = 2
    
    return {"unread_count": unread_count}


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Mark notification as read"""
    # TODO: Implement actual database update
    return {
        "message": f"Notification {notification_id} marked as read",
        "notification_id": notification_id,
        "read_at": datetime.now().isoformat()
    }


@router.put("/mark-all-read")
async def mark_all_notifications_read(
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Mark all notifications as read for current user"""
    # TODO: Implement actual database update
    return {
        "message": "All notifications marked as read",
        "marked_count": 5,  # Mock count
        "marked_at": datetime.now().isoformat()
    }


@router.post("/send")
async def send_notification(
    notification: NotificationCreate,
    current_user: MockUser = Depends(get_current_user_mock), 
    db: Session = Depends(get_db)
):
    """Send notification (admin only)"""
    if not hasattr(current_user, 'role') or current_user.role not in ["super_admin", "administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions"
        )
    
    # TODO: Implement actual notification sending
    return {
        "message": "Notification sent successfully",
        "notification_id": 999,
        "sent_to_count": len(notification.user_ids),
        "sent_at": datetime.now().isoformat()
    }


@router.get("/preferences")
async def get_notification_preferences(
    current_user: MockUser = Depends(get_current_user_mock), 
    db: Session = Depends(get_db)
):
    """Get user notification preferences"""
    # TODO: Implement actual database query
    return {
        "user_id": current_user.id if hasattr(current_user, 'id') else 1,
        "preferences": {
            "email_notifications": True,
            "push_notifications": True,
            "sms_notifications": False,
            "quiet_hours": {
                "enabled": True,
                "start": "22:00",
                "end": "08:00"
            },
            "notification_types": {
                "document_uploaded": True,
                "report_generated": True,
                "comment_received": True,
                "new_user_registered": True,
                "compliance_violation": True
            }
        }
    }


@router.put("/preferences")
async def update_notification_preferences(
    preferences: dict,
    current_user: MockUser = Depends(get_current_user_mock), 
    db: Session = Depends(get_db)
):
    """Update user notification preferences"""
    # TODO: Implement actual database update
    return {
        "message": "Notification preferences updated successfully",
        "user_id": current_user.id if hasattr(current_user, 'id') else 1,
        "updated_at": datetime.now().isoformat()
    }


@router.post("/test")
async def send_test_notification(
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db)
):
    """Send a test notification to current user (for testing purposes)"""
    # TODO: Implement actual test notification
    return {
        "message": "Test notification sent",
        "notification": {
            "title": "Notificação de Teste",
            "message": "Esta é uma notificação de teste do sistema AUDITORIA360",
            "type": "system",
            "priority": "low",
            "sent_at": datetime.now().isoformat()
        }
    }


# Communication Gateway endpoints
@router.post("/webhook/twilio")
async def twilio_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint for receiving messages from Twilio
    Endpoint para receber mensagens do Twilio via webhook
    """
    try:
        # Parse form data from Twilio webhook
        form_data = await request.form()
        webhook_data = dict(form_data)
        
        logger.info(f"Received Twilio webhook: {webhook_data}")
        
        # TODO: Add webhook signature validation for security
        # For now, process the webhook data directly
        
        # Initialize notification service (in production, this should be dependency injected)
        notification_service = EnhancedNotificationService()
        
        # Process the incoming message
        result = notification_service.process_incoming_message(
            webhook_data=webhook_data,
            provider_name="twilio"
        )
        
        if result.get("success"):
            return {
                "status": "success",
                "message": "Webhook processed successfully",
                "data": result
            }
        else:
            logger.error(f"Failed to process webhook: {result.get('error')}")
            return {
                "status": "error", 
                "message": result.get("error", "Unknown error")
            }
            
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )


@router.get("/gateway/status")
async def get_gateway_status(
    current_user: MockUser = Depends(get_current_user_mock)
):
    """
    Get status of communication gateway and providers
    Obter status do gateway de comunicação e provedores
    """
    try:
        # Initialize notification service
        notification_service = EnhancedNotificationService()
        
        # Get gateway status
        status_info = notification_service.get_gateway_status()
        
        return {
            "status": "success",
            "data": status_info
        }
        
    except Exception as e:
        logger.error(f"Failed to get gateway status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get gateway status: {str(e)}"
        )


@router.post("/send-enhanced")
async def send_enhanced_notification(
    notification_data: Dict[str, Any],
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db)
):
    """
    Send notification using the enhanced communication gateway
    Enviar notificação usando o gateway de comunicação aprimorado
    """
    if not hasattr(current_user, 'role') or current_user.role not in ["super_admin", "administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        # Initialize notification service
        notification_service = EnhancedNotificationService()
        
        # Extract required fields
        user_id = notification_data.get("user_id", current_user.id)
        title = notification_data.get("title", "Notificação")
        message = notification_data.get("message", "")
        destination = notification_data.get("destination", "")
        provider_name = notification_data.get("provider")
        
        # Map notification type
        from src.models.notification_models import NotificationType, NotificationPriority
        type_mapping = {
            "email": NotificationType.EMAIL,
            "sms": NotificationType.SMS,
            "system": NotificationType.SYSTEM
        }
        
        notification_type = type_mapping.get(
            notification_data.get("type", "system"),
            NotificationType.SYSTEM
        )
        
        priority_mapping = {
            "low": NotificationPriority.LOW,
            "medium": NotificationPriority.MEDIUM,
            "high": NotificationPriority.HIGH,
            "critical": NotificationPriority.CRITICAL
        }
        
        priority = priority_mapping.get(
            notification_data.get("priority", "medium"),
            NotificationPriority.MEDIUM
        )
        
        # Send notification
        result = notification_service.send_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            destination=destination,
            priority=priority,
            provider_name=provider_name,
            db=db
        )
        
        return {
            "status": "success",
            "message": "Enhanced notification sent successfully",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Failed to send enhanced notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send notification: {str(e)}"
        )


@router.get("/providers")
async def get_communication_providers(
    current_user: MockUser = Depends(get_current_user_mock)
):
    """
    Get available communication providers and their configuration status
    Obter provedores de comunicação disponíveis e status de configuração
    """
    try:
        # Initialize notification service
        notification_service = EnhancedNotificationService()
        
        # Get gateway status including providers
        status_info = notification_service.get_gateway_status()
        
        # Add configuration template for each provider
        providers_with_config = []
        for provider in status_info["providers"]:
            provider_info = {
                "name": provider["name"],
                "configured": provider["configured"],
                "supports": provider["supports"],
                "config_template": _get_provider_config_template(provider["name"])
            }
            providers_with_config.append(provider_info)
        
        return {
            "status": "success",
            "providers": providers_with_config,
            "total_providers": status_info["total_providers"],
            "configured_providers": status_info["configured_providers"]
        }
        
    except Exception as e:
        logger.error(f"Failed to get providers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get providers: {str(e)}"
        )


@router.post("/providers/configure")
async def configure_communication_provider(
    config_data: Dict[str, Any],
    current_user: MockUser = Depends(get_current_user_mock)
):
    """
    Configure a communication provider
    Configurar um provedor de comunicação
    """
    if not hasattr(current_user, 'role') or current_user.role not in ["super_admin", "administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        provider_name = config_data.get("provider")
        config = config_data.get("config", {})
        
        if not provider_name:
            raise ValueError("Provider name is required")
        
        # For demonstration, we'll just validate the configuration
        # In production, this would save to database or environment
        validation_result = _validate_provider_config(provider_name, config)
        
        return {
            "status": "success",
            "message": f"Provider {provider_name} configuration validated",
            "provider": provider_name,
            "validation": validation_result
        }
        
    except Exception as e:
        logger.error(f"Failed to configure provider: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to configure provider: {str(e)}"
        )


def _get_provider_config_template(provider_name: str) -> Dict[str, Any]:
    """Get configuration template for a provider"""
    templates = {
        "email": {
            "smtp_server": {
                "type": "string",
                "required": True,
                "description": "SMTP server address"
            },
            "smtp_port": {
                "type": "integer", 
                "required": True,
                "default": 587,
                "description": "SMTP server port"
            },
            "username": {
                "type": "string",
                "required": True,
                "description": "Email username"
            },
            "password": {
                "type": "password",
                "required": True,
                "description": "Email password"
            }
        },
        "twilio": {
            "account_sid": {
                "type": "string",
                "required": True,
                "description": "Twilio Account SID (format: ACxxxxxxxx)",
                "pattern": "^AC[0-9a-fA-F]{32}$"
            },
            "auth_token": {
                "type": "password",
                "required": True,
                "description": "Twilio Auth Token"
            },
            "from_sms": {
                "type": "string",
                "required": False,
                "description": "SMS phone number (format: +15551234567)",
                "pattern": "^\\+[1-9]\\d{1,14}$"
            },
            "from_whatsapp": {
                "type": "string",
                "required": False,
                "description": "WhatsApp number (format: whatsapp:+14155238886)",
                "pattern": "^whatsapp:\\+[1-9]\\d{1,14}$"
            }
        }
    }
    
    return templates.get(provider_name, {})


def _validate_provider_config(provider_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate provider configuration"""
    template = _get_provider_config_template(provider_name)
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check required fields
    for field, field_config in template.items():
        if field_config.get("required", False) and not config.get(field):
            validation_result["valid"] = False
            validation_result["errors"].append(f"Required field '{field}' is missing")
    
    # Provider-specific validation
    if provider_name == "twilio":
        account_sid = config.get("account_sid", "")
        if account_sid and not account_sid.startswith("AC"):
            validation_result["errors"].append("Twilio Account SID must start with 'AC'")
        
        # Check if at least one number is provided
        if not config.get("from_sms") and not config.get("from_whatsapp"):
            validation_result["warnings"].append("At least one phone number (SMS or WhatsApp) should be configured")
    
    return validation_result
