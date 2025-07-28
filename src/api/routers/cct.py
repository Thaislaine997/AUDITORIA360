"""
CCT (Collective Labor Agreements) API Router
Módulo 3: Base de Convenções Coletivas (CCTs)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.models import get_db, User
from src.services.auth_service import get_current_user

router = APIRouter()

@router.post("/")
async def create_cct(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new CCT"""
    if current_user.role not in ["administrador", "rh", "sindicato"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return {"message": "CCT creation endpoint - implementation pending"}

@router.get("/")
async def list_ccts(
    skip: int = 0,
    limit: int = 100,
    union_id: Optional[int] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List CCTs with filtering"""
    return {"message": "CCT list endpoint - implementation pending"}

@router.get("/{cct_id}")
async def get_cct(
    cct_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get CCT by ID with clauses"""
    return {"message": "CCT get endpoint - implementation pending"}

@router.post("/{cct_id}/compare/{other_cct_id}")
async def compare_ccts(
    cct_id: int,
    other_cct_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two CCTs"""
    return {"message": "CCT comparison endpoint - implementation pending"}

@router.get("/unions")
async def list_unions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all unions"""
    return {"message": "Union list endpoint - implementation pending"}