"""
Client and Configuration Models for AUDITORIA360
Implements advanced client management with AI features
"""

import enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class ClientStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    CHURN_RISK = "churn_risk"


class ConfigurationStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ChurnRiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Client(Base):
    """Enhanced client model with AI features"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(20))
    document_number = Column(String(50))  # CNPJ/CPF
    
    # Business information
    business_segment = Column(String(100))  # "Startups", "Varejo", "Serviços de Saúde"
    tax_regime = Column(String(50))  # "Simples Nacional", "Lucro Presumido", etc.
    annual_revenue = Column(Float)
    
    # Status and risk analysis
    status = Column(Enum(ClientStatus), default=ClientStatus.ACTIVE)
    churn_risk_score = Column(Float, default=0.0)  # 0-1 score
    churn_risk_level = Column(Enum(ChurnRiskLevel), default=ChurnRiskLevel.LOW)
    last_risk_analysis = Column(DateTime(timezone=True))
    
    # Activity tracking for AI analysis
    last_interaction = Column(DateTime(timezone=True))
    total_configurations = Column(Integer, default=0)
    failed_sends_count = Column(Integer, default=0)
    successful_sends_count = Column(Integer, default=0)
    
    # LGPD Compliance
    data_consent_given = Column(Boolean, default=False)
    data_consent_date = Column(DateTime(timezone=True))
    communication_consent = Column(Boolean, default=False)
    consent_proof_id = Column(String(255))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    configurations = relationship("ClientConfiguration", back_populates="client")
    risk_analysis_history = relationship("ChurnRiskAnalysis", back_populates="client")
    anomaly_detections = relationship("ComplianceAnomaly", back_populates="client")
    created_by = relationship("User")


class ClientConfiguration(Base):
    """Configuration management with versioning and rollback"""
    __tablename__ = "client_configurations"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Configuration data
    configuration_data = Column(JSON)  # Flexible JSON configuration
    version = Column(Integer, default=1)
    status = Column(Enum(ConfigurationStatus), default=ConfigurationStatus.DRAFT)
    
    # Template and automation
    is_template = Column(Boolean, default=False)
    template_name = Column(String(255))
    conditional_logic = Column(JSON)  # Rules for conditional application
    
    # Audit and rollback
    parent_version_id = Column(Integer, ForeignKey("client_configurations.id"))
    rollback_reason = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    activated_at = Column(DateTime(timezone=True))
    
    # Relationships
    client = relationship("Client", back_populates="configurations")
    created_by = relationship("User")
    parent_version = relationship("ClientConfiguration", remote_side=[id])
    child_versions = relationship("ClientConfiguration")


class ConfigurationTemplate(Base):
    """Templates with conditional logic for automatic configuration"""
    __tablename__ = "configuration_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Target criteria
    business_segment = Column(String(100))
    tax_regime = Column(String(50))
    revenue_min = Column(Float)
    revenue_max = Column(Float)
    
    # Template configuration
    template_data = Column(JSON)
    conditional_rules = Column(JSON)  # IF-THEN logic rules
    
    # AI suggestions
    suggested_documents = Column(JSON)  # Documents commonly used by similar clients
    success_rate = Column(Float, default=0.0)  # Success rate when applied
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")


class ChurnRiskAnalysis(Base):
    """AI-powered churn risk analysis tracking"""
    __tablename__ = "churn_risk_analysis"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Risk scoring
    risk_score = Column(Float, nullable=False)  # 0-1 score
    risk_level = Column(Enum(ChurnRiskLevel), nullable=False)
    confidence_score = Column(Float)  # AI model confidence
    
    # Risk factors (JSON with weights and factors)
    risk_factors = Column(JSON)
    recommendations = Column(JSON)  # AI-generated recommendations
    
    # Analysis metadata
    model_version = Column(String(50))
    analysis_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="risk_analysis_history")


class ComplianceAnomaly(Base):
    """AI-detected compliance anomalies"""
    __tablename__ = "compliance_anomalies"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Anomaly details
    anomaly_type = Column(String(100))  # "missing_document", "pattern_change", etc.
    severity = Column(String(50))  # "low", "medium", "high", "critical"
    description = Column(Text)
    
    # Detection details
    expected_pattern = Column(JSON)
    actual_pattern = Column(JSON)
    confidence_score = Column(Float)
    
    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)
    resolved_by_user_id = Column(Integer, ForeignKey("users.id"))
    
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="anomaly_detections")
    resolved_by = relationship("User")


class SimulationSession(Base):
    """Track simulation mode sessions for testing configurations"""
    __tablename__ = "simulation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))
    
    # Simulation details
    session_name = Column(String(255))
    configuration_data = Column(JSON)  # Configuration being tested
    
    # Results
    simulation_results = Column(JSON)  # Results of the simulation
    validation_errors = Column(JSON)  # Any errors found
    is_successful = Column(Boolean, default=False)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User")
    client = relationship("Client")


class AIInsight(Base):
    """Store AI-generated insights and suggestions"""
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    
    # Insight details
    insight_type = Column(String(100))  # "optimization", "suggestion", "summary", etc.
    title = Column(String(255))
    description = Column(Text)
    confidence_score = Column(Float)
    
    # Context
    related_resource = Column(String(100))  # "client", "configuration", "user"
    related_resource_id = Column(Integer)
    generated_for_user_id = Column(Integer, ForeignKey("users.id"))
    
    # AI metadata
    model_version = Column(String(50))
    generation_prompt = Column(Text)
    
    # Status
    is_implemented = Column(Boolean, default=False)
    implementation_notes = Column(Text)
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    generated_for_user = relationship("User")