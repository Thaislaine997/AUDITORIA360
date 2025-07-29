"""
API routers package - imports all module routers
Performance optimized with compliance router
"""

from .ai import router as ai_router
from .audit import router as audit_router
from .auth import router as auth_router
from .cct import router as cct_router
from .documents import router as document_router
from .notifications import router as notification_router
from .payroll import router as payroll_router

__all__ = [
    "auth_router",
    "payroll_router",
    "document_router",
    "cct_router",
    "notification_router",
    "audit_router",
    "ai_router",
]
