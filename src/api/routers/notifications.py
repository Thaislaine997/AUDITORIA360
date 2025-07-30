"""
Notifications and Events API Router
Módulo 4: Notificações e Eventos
Enhanced with real-time notification system
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from src.models import get_db

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
