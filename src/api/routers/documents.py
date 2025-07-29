"""
Document Management API Router
Módulo 2: Gestão de Documentos
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.models import User, get_db
from src.services.auth_service import get_current_user

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "other",
    title: Optional[str] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a document to R2 storage"""
    # Implementation placeholder
    return {"message": "Document upload endpoint - implementation pending"}


@router.get("/")
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List documents with filtering"""
    return {"message": "Document list endpoint - implementation pending"}


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get document by ID"""
    return {"message": "Document get endpoint - implementation pending"}


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete document by ID"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return {"message": "Document delete endpoint - implementation pending"}
