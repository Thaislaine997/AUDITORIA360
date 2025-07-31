"""
Payroll Management Models for AUDITORIA360
Módulo 1: Gestão de Folha de Pagamento
"""

import enum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class PayrollStatus(enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    VALIDATED = "validated"
    APPROVED = "approved"
    PAID = "paid"
    CLOSED = "closed"


class PayrollType(enum.Enum):
    MONTHLY = "monthly"
    THIRTEENTH = "thirteenth"
    VACATION = "vacation"
    BONUS = "bonus"
    TERMINATION = "termination"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    
    # 7 essential fields as required
    nome = Column(String(255), nullable=False)  # nome (full_name)
    codigo = Column(String(50), unique=True, nullable=False, index=True)  # código (employee_id)
    admissao = Column(DateTime, nullable=False)  # admissão (hire_date)
    salario = Column(Float, nullable=False)  # salário (salary)
    dependentes = Column(Integer, default=0)  # dependentes (number of dependents)
    cpf = Column(String(14), unique=True, nullable=False)  # cpf
    cargo = Column(String(100), nullable=False)  # cargo (position)
    cbo = Column(String(10))  # cbo (Brazilian Occupation Classification)

    # Status and audit fields (minimal required)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    payroll_items = relationship("PayrollItem", back_populates="employee")

    # Use default __repr__ from BaseModel


class PayrollCompetency(Base):
    __tablename__ = "payroll_competencies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    type = Column(Enum(PayrollType), nullable=False, default=PayrollType.MONTHLY)
    description = Column(String(255))

    # Processing information
    status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.DRAFT)
    total_employees = Column(Integer, default=0)
    total_gross_amount = Column(Float, default=0.0)
    total_net_amount = Column(Float, default=0.0)
    total_deductions = Column(Float, default=0.0)

    # Important dates
    calculation_date = Column(DateTime)
    payment_date = Column(DateTime)
    due_date = Column(DateTime)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))

    # Version control
    version = Column(Integer, default=1)
    parent_id = Column(Integer, ForeignKey("payroll_competencies.id"))

    # Validation and divergences
    validation_errors = Column(JSON)  # Store validation errors as JSON
    divergences_count = Column(Integer, default=0)

    # Relationships
    payroll_items = relationship("PayrollItem", back_populates="competency")
    parent = relationship("PayrollCompetency", remote_side=[id])

    # Use default __repr__ from BaseModel


class PayrollItem(Base):
    __tablename__ = "payroll_items"

    id = Column(Integer, primary_key=True, index=True)
    competency_id = Column(
        Integer, ForeignKey("payroll_competencies.id"), nullable=False
    )
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    # Salary components
    base_salary = Column(Float, default=0.0)
    overtime_hours = Column(Float, default=0.0)
    overtime_value = Column(Float, default=0.0)
    night_shift_hours = Column(Float, default=0.0)
    night_shift_value = Column(Float, default=0.0)
    bonuses = Column(Float, default=0.0)
    commissions = Column(Float, default=0.0)
    allowances = Column(Float, default=0.0)

    # Vacation and 13th salary
    vacation_days = Column(Integer, default=0)
    vacation_value = Column(Float, default=0.0)
    vacation_bonus = Column(Float, default=0.0)
    thirteenth_salary = Column(Float, default=0.0)

    # Deductions - Tax withholdings
    inss_base = Column(Float, default=0.0)
    inss_rate = Column(Float, default=0.0)
    inss_amount = Column(Float, default=0.0)
    irrf_base = Column(Float, default=0.0)
    irrf_rate = Column(Float, default=0.0)
    irrf_amount = Column(Float, default=0.0)
    fgts_base = Column(Float, default=0.0)
    fgts_rate = Column(Float, default=0.0)
    fgts_amount = Column(Float, default=0.0)

    # Union deductions
    union_contribution = Column(Float, default=0.0)
    assistance_tax = Column(Float, default=0.0)
    union_fee = Column(Float, default=0.0)

    # Other deductions
    health_insurance = Column(Float, default=0.0)
    life_insurance = Column(Float, default=0.0)
    meal_voucher_discount = Column(Float, default=0.0)
    transport_voucher_discount = Column(Float, default=0.0)
    advance_payment = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)

    # Calculated totals
    gross_salary = Column(Float, default=0.0)
    total_deductions = Column(Float, default=0.0)
    net_salary = Column(Float, default=0.0)

    # Validation and audit
    is_validated = Column(Boolean, default=False)
    validation_errors = Column(JSON)
    has_divergences = Column(Boolean, default=False)
    divergence_notes = Column(Text)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    calculated_at = Column(DateTime(timezone=True))
    validated_at = Column(DateTime(timezone=True))
    validated_by_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    competency = relationship("PayrollCompetency", back_populates="payroll_items")
    employee = relationship("Employee", back_populates="payroll_items")

    # Use default __repr__ from BaseModel


class PayrollImport(Base):
    __tablename__ = "payroll_imports"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)  # CSV, XLSX, API
    file_size = Column(Integer)
    file_path = Column(String(500))  # Path in R2 storage

    # Import status
    status = Column(
        String(20), default="pending"
    )  # pending, processing, completed, failed
    total_rows = Column(Integer, default=0)
    processed_rows = Column(Integer, default=0)
    success_rows = Column(Integer, default=0)
    error_rows = Column(Integer, default=0)

    # Import results
    import_log = Column(JSON)  # Detailed import log
    validation_errors = Column(JSON)  # Validation errors

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    imported_by_id = Column(Integer, ForeignKey("users.id"))

    # Use default __repr__ from BaseModel
