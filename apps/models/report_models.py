"""
Report Templates and Dynamic Reports Models for AUDITORIA360
Support for customizable report generation system
"""

import enum
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class ReportType(enum.Enum):
    """Types of reports that can be generated"""
    FINANCIAL = "financial"
    PAYROLL = "payroll"
    COMPLIANCE = "compliance"
    AUDIT = "audit"
    CUSTOM = "custom"


class BlockType(enum.Enum):
    """Types of content blocks that can be added to reports"""
    HEADER = "header"
    TEXT = "text"
    TABLE = "table"
    CHART = "chart"
    EXPENSE_ANALYSIS = "expense_analysis"
    BALANCE_SHEET = "balance_sheet"
    MONTHLY_REVENUE_CHART = "monthly_revenue_chart"
    PAYROLL_SUMMARY = "payroll_summary"
    COMPLIANCE_STATUS = "compliance_status"
    FOOTER = "footer"


class ReportTemplate(Base):
    """Template for customizable reports"""
    __tablename__ = "report_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Template configuration
    type = Column(Enum(ReportType), nullable=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Layout configuration
    layout_config = Column(JSON)  # Store layout settings, margins, etc.
    
    # Template ownership and sharing
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For sharing within organization
    is_public = Column(Boolean, default=False)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_id])
    blocks = relationship("ReportBlock", back_populates="template", cascade="all, delete-orphan")
    generated_reports = relationship("GeneratedReport", back_populates="template")


class ReportBlock(Base):
    """Individual content blocks within a report template"""
    __tablename__ = "report_blocks"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("report_templates.id"), nullable=False)
    
    # Block identification
    block_type = Column(Enum(BlockType), nullable=False)
    title = Column(String(255))
    
    # Layout and positioning
    position_order = Column(Integer, nullable=False)  # Order in the report
    width_percentage = Column(Float, default=100.0)  # Width as percentage
    height_pixels = Column(Integer)  # Optional fixed height
    
    # Block configuration
    config = Column(JSON)  # Block-specific configuration
    data_source = Column(String(255))  # Where to get data from
    query_params = Column(JSON)  # Parameters for data queries
    
    # Styling
    style_config = Column(JSON)  # CSS-like styling options
    
    # Conditional display
    display_conditions = Column(JSON)  # When to show this block
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    template = relationship("ReportTemplate", back_populates="blocks")


class GeneratedReport(Base):
    """History of generated reports using templates"""
    __tablename__ = "generated_reports"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("report_templates.id"), nullable=False)
    
    # Report identification
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Generation context
    generated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    generated_for_client_id = Column(Integer, ForeignKey("users.id"))  # Client the report was generated for
    
    # Report data
    report_data = Column(JSON)  # Snapshot of data used in generation
    parameters = Column(JSON)  # Parameters used for generation
    
    # Output information
    file_path = Column(String(500))  # Path to generated PDF/file
    file_size = Column(Integer)  # File size in bytes
    page_count = Column(Integer)  # Number of pages in generated report
    
    # Status and tracking
    generation_status = Column(String(50), default="pending")  # pending, generating, completed, failed
    generation_started_at = Column(DateTime(timezone=True))
    generation_completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Access tracking
    download_count = Column(Integer, default=0)
    last_downloaded_at = Column(DateTime(timezone=True))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    template = relationship("ReportTemplate", back_populates="generated_reports")
    generated_by = relationship("User", foreign_keys=[generated_by_id])
    generated_for_client = relationship("User", foreign_keys=[generated_for_client_id])


class ReportDataSource(Base):
    """Configuration for report data sources"""
    __tablename__ = "report_data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    
    # Data source configuration
    source_type = Column(String(50), nullable=False)  # database, api, file, etc.
    connection_config = Column(JSON)  # Connection details
    query_template = Column(Text)  # SQL query or API endpoint template
    
    # Data processing
    data_transformation = Column(JSON)  # How to transform the data
    cache_duration_minutes = Column(Integer, default=60)  # How long to cache data
    
    # Access control
    required_permissions = Column(JSON)  # Permissions needed to access this data source
    
    # Status
    is_active = Column(Boolean, default=True)
    last_tested_at = Column(DateTime(timezone=True))
    test_status = Column(String(50))  # success, failed, not_tested
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")