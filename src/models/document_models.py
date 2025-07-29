"""
Document Management Models for AUDITORIA360
Módulo 2: Gestão de Documentos
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class DocumentType(enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    TXT = "txt"
    OTHER = "other"

class DocumentCategory(enum.Enum):
    PAYROLL = "payroll"
    CCT = "cct"
    EMPLOYEE = "employee"
    CONTRACT = "contract"
    COMPLIANCE = "compliance"
    AUDIT = "audit"
    REPORT = "report"
    OTHER = "other"

class DocumentStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    APPROVED = "approved"
    ARCHIVED = "archived"
    DELETED = "deleted"

class AccessLevel(enum.Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # Path in R2 storage
    file_size = Column(Integer, nullable=False)
    file_type = Column(Enum(DocumentType), nullable=False)
    mime_type = Column(String(100))
    
    # Document metadata
    title = Column(String(255))
    description = Column(Text)
    category = Column(Enum(DocumentCategory), nullable=False)
    tags = Column(JSON)  # Array of tags for search
    
    # Security and access control
    access_level = Column(Enum(AccessLevel), nullable=False, default=AccessLevel.INTERNAL)
    is_encrypted = Column(Boolean, default=False)
    encryption_key_id = Column(String(100))
    
    # Document relationships
    related_employee_id = Column(Integer, ForeignKey("employees.id"))
    related_competency_id = Column(Integer, ForeignKey("payroll_competencies.id"))
    parent_document_id = Column(Integer, ForeignKey("documents.id"))
    
    # Processing status
    status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.UPLOADED)
    ocr_processed = Column(Boolean, default=False)
    ocr_text = Column(Text)
    ocr_confidence = Column(Float)
    
    # Version control
    version = Column(Integer, default=1)
    checksum = Column(String(64))  # SHA-256 checksum
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    
    # LGPD Compliance
    retention_date = Column(DateTime(timezone=True))
    anonymization_date = Column(DateTime(timezone=True))
    contains_personal_data = Column(Boolean, default=False)
    
    # Relationships
    uploaded_by = relationship("User")
    versions = relationship("DocumentVersion", back_populates="document")
    access_logs = relationship("DocumentAccess", back_populates="document")
    parent = relationship("Document", remote_side=[id])
    
    # Use default __repr__ from BaseModel

class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    checksum = Column(String(64))
    
    # Change information
    change_description = Column(Text)
    change_reason = Column(String(255))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    document = relationship("Document", back_populates="versions")
    created_by = relationship("User")
    
    # Use default __repr__ from BaseModel

class DocumentAccess(Base):
    __tablename__ = "document_access"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Access details
    action = Column(String(50), nullable=False)  # view, download, edit, delete
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Access metadata
    duration_seconds = Column(Integer)  # How long the document was accessed
    page_count = Column(Integer)  # For PDF documents
    
    # Audit fields
    accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="access_logs")
    user = relationship("User")
    
    # Use default __repr__ from BaseModel

class DocumentShare(Base):
    __tablename__ = "document_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    shared_with_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shared_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Share permissions
    can_view = Column(Boolean, default=True)
    can_download = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)
    can_share = Column(Boolean, default=False)
    
    # Share validity
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True))
    
    # Relationships
    document = relationship("Document")
    shared_with = relationship("User", foreign_keys=[shared_with_user_id])
    shared_by = relationship("User", foreign_keys=[shared_by_user_id])
    
    # Use default __repr__ from BaseModel

class DocumentTemplate(Base):
    __tablename__ = "document_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(Enum(DocumentCategory), nullable=False)
    template_path = Column(String(500), nullable=False)  # Path to template file
    
    # Template metadata
    required_fields = Column(JSON)  # Fields required to generate document
    default_values = Column(JSON)   # Default values for fields
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")
    
    # Use default __repr__ from BaseModel