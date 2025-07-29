"""
Collective Labor Agreement (CCT) Models for AUDITORIA360
Módulo 3: Base de Convenções Coletivas (CCTs)
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class CCTStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"

class CCTType(enum.Enum):
    COLLECTIVE_AGREEMENT = "collective_agreement"
    COLLECTIVE_CONVENTION = "collective_convention"
    TERM_OF_COMMITMENT = "term_of_commitment"
    AMENDMENT = "amendment"

class ClauseType(enum.Enum):
    SALARY = "salary"
    BENEFITS = "benefits"
    WORKING_HOURS = "working_hours"
    VACATION = "vacation"
    OVERTIME = "overtime"
    UNION_CONTRIBUTION = "union_contribution"
    HEALTH_SAFETY = "health_safety"
    TERMINATION = "termination"
    OTHER = "other"

class Union(Base):
    __tablename__ = "unions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True)
    registration_number = Column(String(50))
    
    # Contact information
    email = Column(String(255))
    phone = Column(String(20))
    website = Column(String(255))
    
    # Address
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    
    # Union details
    category = Column(String(255))  # Professional category
    base_territory = Column(String(255))  # Geographic coverage
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ccts = relationship("CCT", back_populates="union")
    
    # Use default __repr__ from BaseModel

class CCT(Base):
    __tablename__ = "ccts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    number = Column(String(100))
    registration_number = Column(String(100))
    
    # Union and employer information
    union_id = Column(Integer, ForeignKey("unions.id"), nullable=False)
    employer_entity = Column(String(255))  # Sindicate or employer entity
    
    # CCT details
    type = Column(Enum(CCTType), nullable=False)
    category = Column(String(255), nullable=False)  # Professional category
    economic_category = Column(String(255))  # Economic category (CNAE)
    
    # Validity period
    validity_start = Column(DateTime, nullable=False)
    validity_end = Column(DateTime, nullable=False)
    signature_date = Column(DateTime)
    publication_date = Column(DateTime)
    
    # Status and processing
    status = Column(Enum(CCTStatus), nullable=False, default=CCTStatus.DRAFT)
    is_published = Column(Boolean, default=False)
    
    # Document information
    original_document_id = Column(Integer, ForeignKey("documents.id"))
    pdf_path = Column(String(500))  # Path to PDF file in R2
    ocr_processed = Column(Boolean, default=False)
    ocr_text = Column(Text)
    ocr_confidence = Column(Float)
    
    # Indexing and search
    keywords = Column(JSON)  # Array of keywords for search
    summary = Column(Text)
    
    # Version control
    version = Column(Integer, default=1)
    parent_id = Column(Integer, ForeignKey("ccts.id"))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Automatic update tracking
    last_scraped = Column(DateTime(timezone=True))
    scraping_source = Column(String(255))
    automatic_update = Column(Boolean, default=False)
    
    # Relationships
    union = relationship("Union", back_populates="ccts")
    clauses = relationship("CCTClause", back_populates="cct")
    original_document = relationship("Document")
    parent = relationship("CCT", remote_side=[id])
    comparisons = relationship("CCTComparison", foreign_keys="CCTComparison.cct_id")
    
    # Use default __repr__ from BaseModel

class CCTClause(Base):
    __tablename__ = "cct_clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    cct_id = Column(Integer, ForeignKey("ccts.id"), nullable=False)
    
    # Clause identification
    clause_number = Column(String(20))
    title = Column(String(255), nullable=False)
    type = Column(Enum(ClauseType), nullable=False)
    
    # Clause content
    content = Column(Text, nullable=False)
    summary = Column(Text)
    
    # Financial information (when applicable)
    percentage_value = Column(Float)  # For percentage-based clauses
    fixed_value = Column(Float)       # For fixed value clauses
    minimum_value = Column(Float)
    maximum_value = Column(Float)
    
    # Validity and conditions
    effective_date = Column(DateTime)
    expiration_date = Column(DateTime)
    conditions = Column(Text)
    exceptions = Column(Text)
    
    # OCR and processing metadata
    confidence_score = Column(Float)
    page_number = Column(Integer)
    position_in_document = Column(Integer)
    
    # Keywords for search and matching
    keywords = Column(JSON)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    cct = relationship("CCT", back_populates="clauses")
    
    # Use default __repr__ from BaseModel

class CCTComparison(Base):
    __tablename__ = "cct_comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    cct_id = Column(Integer, ForeignKey("ccts.id"), nullable=False)
    compared_cct_id = Column(Integer, ForeignKey("ccts.id"), nullable=False)
    
    # Comparison metadata
    comparison_type = Column(String(50))  # version_comparison, cross_union, etc.
    comparison_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Comparison results
    differences_found = Column(Integer, default=0)
    similarities_found = Column(Integer, default=0)
    
    # Detailed comparison data
    differences = Column(JSON)  # Detailed differences as JSON
    similarities = Column(JSON)  # Common clauses as JSON
    analysis_summary = Column(Text)
    
    # Processing information
    processed_by_ai = Column(Boolean, default=False)
    ai_confidence = Column(Float)
    
    # Audit fields
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    cct = relationship("CCT", foreign_keys=[cct_id])
    compared_cct = relationship("CCT", foreign_keys=[compared_cct_id])
    created_by = relationship("User")
    
    # Use default __repr__ from BaseModel

class CCTUpdateLog(Base):
    __tablename__ = "cct_update_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    cct_id = Column(Integer, ForeignKey("ccts.id"), nullable=False)
    
    # Update information
    update_type = Column(String(50))  # manual, automatic, scraping
    update_source = Column(String(255))
    changes_detected = Column(JSON)
    
    # Processing details
    processing_status = Column(String(20), default="pending")
    processing_log = Column(JSON)
    error_message = Column(Text)
    
    # Audit fields
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    updated_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    cct = relationship("CCT")
    updated_by = relationship("User")
    
    # Use default __repr__ from BaseModel