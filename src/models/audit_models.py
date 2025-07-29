"""
Audit and Compliance Models for AUDITORIA360
Módulo 5: Auditoria e Compliance
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class AuditType(enum.Enum):
    PERIODIC = "periodic"
    EVENT_TRIGGERED = "event_triggered"
    MANUAL = "manual"
    COMPLIANCE_CHECK = "compliance_check"

class AuditStatus(enum.Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ComplianceStatus(enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    NEEDS_REVIEW = "needs_review"

class ViolationType(enum.Enum):
    SALARY_BELOW_MINIMUM = "salary_below_minimum"
    OVERTIME_VIOLATION = "overtime_violation"
    MISSING_UNION_CONTRIBUTION = "missing_union_contribution"
    VACATION_VIOLATION = "vacation_violation"
    THIRTEENTH_SALARY_ERROR = "thirteenth_salary_error"
    TAX_CALCULATION_ERROR = "tax_calculation_error"
    CCT_CLAUSE_VIOLATION = "cct_clause_violation"
    MISSING_DOCUMENTATION = "missing_documentation"
    DATA_INCONSISTENCY = "data_inconsistency"
    OTHER = "other"

class RuleSeverity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuditExecution(Base):
    __tablename__ = "audit_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(Enum(AuditType), nullable=False)
    
    # Scope definition
    target_module = Column(String(50))  # payroll, cct, documents, all
    target_period_start = Column(DateTime)
    target_period_end = Column(DateTime)
    target_criteria = Column(JSON)  # Additional criteria for audit scope
    
    # Execution details
    status = Column(Enum(AuditStatus), nullable=False, default=AuditStatus.SCHEDULED)
    scheduled_for = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Results summary
    total_items_checked = Column(Integer, default=0)
    compliant_items = Column(Integer, default=0)
    non_compliant_items = Column(Integer, default=0)
    warnings_found = Column(Integer, default=0)
    critical_violations = Column(Integer, default=0)
    
    # Processing information
    rules_executed = Column(JSON)  # List of rule IDs executed
    execution_log = Column(JSON)   # Detailed execution log
    error_message = Column(Text)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")
    findings = relationship("AuditFinding", back_populates="audit_execution")
    
    # Use default __repr__ from BaseModel

class ComplianceRule(Base):
    __tablename__ = "compliance_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    
    # Rule configuration
    category = Column(String(100), nullable=False)  # salary, tax, union, etc.
    severity = Column(Enum(RuleSeverity), nullable=False)
    violation_type = Column(Enum(ViolationType), nullable=False)
    
    # Rule logic
    rule_expression = Column(Text, nullable=False)  # SQL or Python expression
    rule_parameters = Column(JSON)  # Parameters for the rule
    expected_result = Column(String(100))  # Expected result type
    
    # CCT Integration
    related_cct_clause_types = Column(JSON)  # Types of CCT clauses this rule checks
    legal_reference = Column(Text)  # Legal basis for the rule
    
    # Status and versioning
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    parent_rule_id = Column(Integer, ForeignKey("compliance_rules.id"))
    
    # Execution settings
    auto_execute = Column(Boolean, default=True)
    execution_frequency = Column(String(20))  # daily, weekly, monthly, on_demand
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")
    parent_rule = relationship("ComplianceRule", remote_side=[id])
    findings = relationship("AuditFinding", back_populates="rule")
    
    # Use default __repr__ from BaseModel

class AuditFinding(Base):
    __tablename__ = "audit_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    audit_execution_id = Column(Integer, ForeignKey("audit_executions.id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("compliance_rules.id"), nullable=False)
    
    # Finding details
    violation_type = Column(Enum(ViolationType), nullable=False)
    severity = Column(Enum(RuleSeverity), nullable=False)
    status = Column(Enum(ComplianceStatus), nullable=False)
    
    # Context information
    entity_type = Column(String(50), nullable=False)  # payroll_item, employee, cct_clause
    entity_id = Column(String(100), nullable=False)
    entity_reference = Column(String(255))  # Human-readable reference
    
    # Finding description
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text)
    
    # Values and calculations
    expected_value = Column(String(255))
    actual_value = Column(String(255))
    difference = Column(Float)
    percentage_difference = Column(Float)
    
    # Impact assessment
    financial_impact = Column(Float)
    risk_level = Column(String(20))
    legal_implications = Column(Text)
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by_id = Column(Integer, ForeignKey("users.id"))
    resolution_notes = Column(Text)
    
    # Evidence and documentation
    evidence = Column(JSON)  # Supporting evidence for the finding
    screenshots = Column(JSON)  # Paths to screenshot files
    
    # Audit fields
    found_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    audit_execution = relationship("AuditExecution", back_populates="findings")
    rule = relationship("ComplianceRule", back_populates="findings")
    resolved_by = relationship("User")
    
    # Use default __repr__ from BaseModel

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Report scope
    audit_execution_id = Column(Integer, ForeignKey("audit_executions.id"))
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Report content
    executive_summary = Column(Text)
    total_findings = Column(Integer, default=0)
    critical_findings = Column(Integer, default=0)
    resolved_findings = Column(Integer, default=0)
    pending_findings = Column(Integer, default=0)
    
    # Financial impact
    total_financial_impact = Column(Float, default=0.0)
    potential_savings = Column(Float, default=0.0)
    cost_of_non_compliance = Column(Float, default=0.0)
    
    # Report files
    report_file_path = Column(String(500))  # Path to generated report file
    file_format = Column(String(10))  # PDF, XLSX, CSV
    file_size = Column(Integer)
    
    # Distribution
    recipients = Column(JSON)  # List of users/emails who received the report
    sent_at = Column(DateTime(timezone=True))
    
    # Status
    is_published = Column(Boolean, default=False)
    is_confidential = Column(Boolean, default=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    audit_execution = relationship("AuditExecution")
    created_by = relationship("User")
    
    # Use default __repr__ from BaseModel

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Assessment scope
    assessment_type = Column(String(50), nullable=False)  # payroll, compliance, operational
    target_entity_type = Column(String(50))  # employee, department, company
    target_entity_id = Column(String(100))
    
    # Risk scoring
    probability_score = Column(Integer)  # 1-5 scale
    impact_score = Column(Integer)       # 1-5 scale
    overall_risk_score = Column(Float)   # Calculated risk score
    risk_level = Column(String(20))      # low, medium, high, critical
    
    # Assessment results
    risk_factors = Column(JSON)          # List of identified risk factors
    mitigation_strategies = Column(JSON) # Recommended mitigation strategies
    action_items = Column(JSON)          # Specific action items
    
    # Timeline
    assessment_date = Column(DateTime(timezone=True), nullable=False)
    next_assessment_date = Column(DateTime(timezone=True))
    
    # Status
    status = Column(String(20), default="active")  # active, mitigated, accepted
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")
    
    # Use default __repr__ from BaseModel