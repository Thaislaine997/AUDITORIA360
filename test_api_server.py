"""
Standalone API server for testing new features without complex dependencies
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Import routers
try:
    from src.api.routers.auth import router as auth_router
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False

try:
    from src.api.routers.core_business import router as core_business_router
    CORE_BUSINESS_AVAILABLE = True
except ImportError:
    CORE_BUSINESS_AVAILABLE = False

app = FastAPI(
    title="AUDITORIA360 - Feature Test API", 
    description="Test implementation for new features",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers if available
if AUTH_AVAILABLE:
    app.include_router(auth_router, prefix="/auth", tags=["authentication"])

if CORE_BUSINESS_AVAILABLE:
    app.include_router(core_business_router, prefix="/api/core", tags=["core-business"])

# Mock User for testing
class MockUser:
    def __init__(self):
        self.id = 1
        self.role = "contabilidade"
        self.username = "test_user"

# Pydantic models
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

class ReportTemplateResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: str
    is_default: bool
    is_active: bool
    usage_count: int
    created_at: str

# Notifications endpoints
@app.get("/api/v1/notifications/unread-count")
async def get_unread_count():
    """Get count of unread notifications for header badge"""
    return {"unread_count": 2}

@app.get("/api/v1/notifications/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
):
    """List user notifications"""
    sample_notifications = [
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
    ]
    return sample_notifications[:limit]

@app.put("/api/v1/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    """Mark notification as read"""
    return {
        "message": f"Notification {notification_id} marked as read",
        "notification_id": notification_id,
        "read_at": datetime.now().isoformat()
    }

# Reports endpoints
@app.get("/api/v1/reports/", response_model=List[ReportTemplateResponse])
async def list_report_templates(
    skip: int = 0,
    limit: int = 100,
    template_type: Optional[str] = None,
):
    """List available report templates"""
    return [
        {
            "id": 1,
            "name": "Relatório Financeiro Básico",
            "description": "Template padrão para relatórios financeiros",
            "type": "financial",
            "is_default": True,
            "is_active": True,
            "usage_count": 15,
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "name": "Análise de Despesas Detalhada",
            "description": "Template customizado para análise detalhada de despesas",
            "type": "financial",
            "is_default": False,
            "is_active": True,
            "usage_count": 8,
            "created_at": "2024-01-05T10:30:00Z"
        }
    ]

@app.get("/api/v1/reports/block-types/available")
async def get_available_block_types():
    """Get list of available block types for report templates"""
    return {
        "block_types": [
            {
                "type": "header",
                "name": "Cabeçalho",
                "description": "Cabeçalho do relatório com logo e informações básicas",
                "icon": "header"
            },
            {
                "type": "expense_analysis",
                "name": "Análise de Despesas",
                "description": "Gráficos e tabelas de análise de despesas",
                "icon": "chart-bar"
            },
            {
                "type": "balance_sheet",
                "name": "Balanço Patrimonial Simplificado",
                "description": "Resumo do balanço patrimonial",
                "icon": "balance-scale"
            },
            {
                "type": "monthly_revenue_chart",
                "name": "Gráfico de Faturamento Mensal",
                "description": "Gráfico de evolução do faturamento",
                "icon": "chart-line"
            }
        ]
    }

@app.get("/api/v1/reports/{template_id}")
async def get_report_template(template_id: int):
    """Get detailed information about a specific report template"""
    if template_id == 1:
        return {
            "id": 1,
            "name": "Relatório Financeiro Básico",
            "description": "Template padrão para relatórios financeiros",
            "type": "financial",
            "is_default": True,
            "is_active": True,
            "usage_count": 15,
            "created_at": "2024-01-01T00:00:00Z",
            "blocks": [
                {
                    "id": 1,
                    "block_type": "header",
                    "title": "Cabeçalho do Relatório",
                    "position_order": 1,
                    "width_percentage": 100.0,
                    "config": {"show_logo": True, "show_date": True}
                },
                {
                    "id": 2,
                    "block_type": "expense_analysis",
                    "title": "Análise de Despesas",
                    "position_order": 2,
                    "width_percentage": 100.0,
                    "config": {"chart_type": "bar", "period": "monthly"}
                }
            ]
        }
    else:
        return {"detail": "Template not found"}

# Document export endpoints
@app.get("/api/v1/documents/export/csv")
async def export_documents_csv(category: Optional[str] = None):
    """Export documents list to CSV format"""
    csv_data = """ID,Title,Category,Upload Date,Size,Uploaded By
1,Nota Fiscal 001.pdf,fiscal,2024-01-10T09:30:00Z,2.5 MB,Cliente ABC
2,Contrato Social.pdf,legal,2024-01-08T14:15:00Z,1.8 MB,Empresa XYZ"""
    
    return {
        "filename": "documents_export.csv",
        "content_type": "text/csv",
        "data": csv_data,
        "exported_at": datetime.now().isoformat(),
        "record_count": 2
    }

@app.get("/api/v1/documents/export/pdf")
async def export_documents_pdf(category: Optional[str] = None):
    """Export documents list to PDF format"""
    return {
        "filename": "documents_export.pdf",
        "content_type": "application/pdf",
        "message": "PDF export ready for download",
        "exported_at": datetime.now().isoformat(),
        "record_count": 2,
        "download_url": "/api/v1/documents/download/documents_export.pdf"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "features": ["notifications", "report_templates", "export"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)