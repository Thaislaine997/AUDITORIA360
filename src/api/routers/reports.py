"""
Report Templates API Router
Handles customizable report template management
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

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
class ReportBlockCreate(BaseModel):
    block_type: str
    title: Optional[str] = None
    position_order: int
    width_percentage: float = 100.0
    config: Optional[dict] = None
    data_source: Optional[str] = None


class ReportTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    layout_config: Optional[dict] = None
    blocks: List[ReportBlockCreate] = []


class ReportTemplateResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: str
    is_default: bool
    is_active: bool
    usage_count: int
    created_at: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ReportTemplateResponse])
async def list_report_templates(
    skip: int = 0,
    limit: int = 100,
    template_type: Optional[str] = None,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """List available report templates for the current user"""
    # TODO: Implement actual database query
    # For now, return sample data
    return [
        {
            "id": 1,
            "name": "Relatório Financeiro Básico",
            "description": "Template padrão para relatórios financeiros",
            "type": "financial",
            "is_default": True,
            "is_active": True,
            "usage_count": 15,
            "created_at": "2024-01-01T00:00:00Z",
        },
        {
            "id": 2,
            "name": "Análise de Despesas Detalhada",
            "description": "Template customizado para análise detalhada de despesas",
            "type": "financial",
            "is_default": False,
            "is_active": True,
            "usage_count": 8,
            "created_at": "2024-01-05T10:30:00Z",
        },
    ]


@router.post("/", response_model=ReportTemplateResponse)
async def create_report_template(
    template: ReportTemplateCreate,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Create a new report template"""
    # Check if user has permission (only contabilidade role)
    if not hasattr(current_user, "role") or current_user.role != "contabilidade":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only accounting users can create report templates",
        )

    # TODO: Implement actual database creation
    # For now, return mock response
    return {
        "id": 999,
        "name": template.name,
        "description": template.description,
        "type": template.type,
        "is_default": False,
        "is_active": True,
        "usage_count": 0,
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.get("/{template_id}")
async def get_report_template(
    template_id: int,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Get detailed information about a specific report template"""
    # TODO: Implement actual database query
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
                    "config": {"show_logo": True, "show_date": True},
                },
                {
                    "id": 2,
                    "block_type": "expense_analysis",
                    "title": "Análise de Despesas",
                    "position_order": 2,
                    "width_percentage": 100.0,
                    "config": {"chart_type": "bar", "period": "monthly"},
                },
                {
                    "id": 3,
                    "block_type": "balance_sheet",
                    "title": "Balanço Patrimonial Simplificado",
                    "position_order": 3,
                    "width_percentage": 100.0,
                    "config": {"simplified": True},
                },
            ],
        }
    else:
        raise HTTPException(status_code=404, detail="Template not found")


@router.put("/{template_id}")
async def update_report_template(
    template_id: int,
    template: ReportTemplateCreate,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Update an existing report template"""
    # Check if user has permission
    if not hasattr(current_user, "role") or current_user.role != "contabilidade":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only accounting users can update report templates",
        )

    # TODO: Implement actual database update
    return {"message": f"Template {template_id} updated successfully"}


@router.delete("/{template_id}")
async def delete_report_template(
    template_id: int,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Delete a report template"""
    # Check if user has permission
    if not hasattr(current_user, "role") or current_user.role != "contabilidade":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only accounting users can delete report templates",
        )

    # TODO: Implement actual database deletion
    return {"message": f"Template {template_id} deleted successfully"}


@router.post("/{template_id}/generate")
async def generate_report(
    template_id: int,
    client_id: Optional[int] = None,
    parameters: Optional[dict] = None,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Generate a report using the specified template"""
    # TODO: Implement actual report generation
    return {
        "message": f"Report generation started using template {template_id}",
        "report_id": 999,
        "status": "generating",
        "estimated_completion": "2024-01-01T00:05:00Z",
    }


@router.get("/{template_id}/blocks")
async def get_template_blocks(
    template_id: int,
    current_user: MockUser = Depends(get_current_user_mock),
    db: Session = Depends(get_db),
):
    """Get all blocks for a specific template"""
    # TODO: Implement actual database query
    return {
        "template_id": template_id,
        "blocks": [
            {
                "id": 1,
                "block_type": "header",
                "title": "Cabeçalho do Relatório",
                "position_order": 1,
                "width_percentage": 100.0,
            },
            {
                "id": 2,
                "block_type": "expense_analysis",
                "title": "Análise de Despesas",
                "position_order": 2,
                "width_percentage": 100.0,
            },
        ],
    }


@router.get("/block-types/available")
async def get_available_block_types():
    """Get list of available block types for report templates"""
    return {
        "block_types": [
            {
                "type": "header",
                "name": "Cabeçalho",
                "description": "Cabeçalho do relatório com logo e informações básicas",
                "icon": "header",
            },
            {
                "type": "expense_analysis",
                "name": "Análise de Despesas",
                "description": "Gráficos e tabelas de análise de despesas",
                "icon": "chart-bar",
            },
            {
                "type": "balance_sheet",
                "name": "Balanço Patrimonial Simplificado",
                "description": "Resumo do balanço patrimonial",
                "icon": "balance-scale",
            },
            {
                "type": "monthly_revenue_chart",
                "name": "Gráfico de Faturamento Mensal",
                "description": "Gráfico de evolução do faturamento",
                "icon": "chart-line",
            },
            {
                "type": "payroll_summary",
                "name": "Resumo da Folha",
                "description": "Resumo da folha de pagamento",
                "icon": "users",
            },
            {
                "type": "footer",
                "name": "Rodapé",
                "description": "Rodapé do relatório",
                "icon": "footer",
            },
        ]
    }
