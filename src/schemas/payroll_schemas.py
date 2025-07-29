"""
Pydantic schemas for payroll management
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from src.models.payroll_models import PayrollStatus, PayrollType


# Employee schemas
class EmployeeBase(BaseModel):
    employee_id: str
    full_name: str
    cpf: str = Field(..., pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
    pis_pasep: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    hire_date: date
    termination_date: Optional[date] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Decimal = Field(..., gt=0)
    work_schedule: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    consent_given: bool = False


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    termination_date: Optional[date] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[Decimal] = None
    work_schedule: Optional[str] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    consent_given: bool
    consent_date: Optional[datetime]

    class Config:
        from_attributes = True


# Payroll Competency schemas
class PayrollCompetencyBase(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    type: PayrollType = PayrollType.MONTHLY
    description: Optional[str] = None


class PayrollCompetencyCreate(PayrollCompetencyBase):
    pass


class PayrollCompetencyUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[PayrollStatus] = None
    payment_date: Optional[date] = None
    due_date: Optional[date] = None


class PayrollCompetency(PayrollCompetencyBase):
    id: int
    status: PayrollStatus
    total_employees: int
    total_gross_amount: Decimal
    total_net_amount: Decimal
    total_deductions: Decimal
    calculation_date: Optional[datetime]
    payment_date: Optional[date]
    due_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]
    version: int
    validation_errors: Optional[Dict[str, Any]] = None
    divergences_count: int

    class Config:
        from_attributes = True


# Payroll Item schemas
class PayrollItemBase(BaseModel):
    base_salary: Decimal = Field(default=Decimal("0.00"), ge=0)
    overtime_hours: Decimal = Field(default=Decimal("0.00"), ge=0)
    overtime_value: Decimal = Field(default=Decimal("0.00"), ge=0)
    night_shift_hours: Decimal = Field(default=Decimal("0.00"), ge=0)
    night_shift_value: Decimal = Field(default=Decimal("0.00"), ge=0)
    bonuses: Decimal = Field(default=Decimal("0.00"), ge=0)
    commissions: Decimal = Field(default=Decimal("0.00"), ge=0)
    allowances: Decimal = Field(default=Decimal("0.00"), ge=0)

    # Vacation and 13th salary
    vacation_days: int = Field(default=0, ge=0)
    vacation_value: Decimal = Field(default=Decimal("0.00"), ge=0)
    vacation_bonus: Decimal = Field(default=Decimal("0.00"), ge=0)
    thirteenth_salary: Decimal = Field(default=Decimal("0.00"), ge=0)

    # Deductions
    union_contribution: Decimal = Field(default=Decimal("0.00"), ge=0)
    assistance_tax: Decimal = Field(default=Decimal("0.00"), ge=0)
    union_fee: Decimal = Field(default=Decimal("0.00"), ge=0)
    health_insurance: Decimal = Field(default=Decimal("0.00"), ge=0)
    life_insurance: Decimal = Field(default=Decimal("0.00"), ge=0)
    meal_voucher_discount: Decimal = Field(default=Decimal("0.00"), ge=0)
    transport_voucher_discount: Decimal = Field(default=Decimal("0.00"), ge=0)
    advance_payment: Decimal = Field(default=Decimal("0.00"), ge=0)
    other_deductions: Decimal = Field(default=Decimal("0.00"), ge=0)


class PayrollItemCreate(PayrollItemBase):
    competency_id: int
    employee_id: int


class PayrollItemUpdate(PayrollItemBase):
    pass


class PayrollItem(PayrollItemBase):
    id: int
    competency_id: int
    employee_id: int

    # Calculated tax withholdings
    inss_base: Decimal
    inss_rate: Decimal
    inss_amount: Decimal
    irrf_base: Decimal
    irrf_rate: Decimal
    irrf_amount: Decimal
    fgts_base: Decimal
    fgts_rate: Decimal
    fgts_amount: Decimal

    # Calculated totals
    gross_salary: Decimal
    total_deductions: Decimal
    net_salary: Decimal

    # Validation
    is_validated: bool
    validation_errors: Optional[Dict[str, Any]] = None
    has_divergences: bool
    divergence_notes: Optional[str] = None

    created_at: datetime
    updated_at: Optional[datetime]
    calculated_at: Optional[datetime]
    validated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PayrollItemWithEmployee(PayrollItem):
    employee: Employee


class PayrollCompetencyDetail(PayrollCompetency):
    payroll_items: List[PayrollItemWithEmployee] = []


# Import schemas
class PayrollImportBase(BaseModel):
    filename: str
    file_type: str = Field(..., pattern=r"^(CSV|XLSX|API)$")


class PayrollImportCreate(PayrollImportBase):
    file_size: Optional[int] = None
    file_path: Optional[str] = None


class PayrollImport(PayrollImportBase):
    id: int
    file_size: Optional[int]
    file_path: Optional[str]
    status: str
    total_rows: int
    processed_rows: int
    success_rows: int
    error_rows: int
    import_log: Optional[Dict[str, Any]] = None
    validation_errors: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Calculation request schemas
class PayrollCalculationRequest(BaseModel):
    competency_id: int
    employee_ids: Optional[List[int]] = None  # If None, calculate for all employees
    recalculate: bool = False  # Force recalculation even if already calculated


class PayrollCalculationResult(BaseModel):
    competency_id: int
    total_calculated: int
    successful: int
    failed: int
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []


# Validation schemas
class PayrollValidationRequest(BaseModel):
    competency_id: int
    validation_rules: Optional[List[str]] = None  # Specific rules to run


class PayrollValidationResult(BaseModel):
    competency_id: int
    is_valid: bool
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    divergences: List[Dict[str, Any]] = []


# Report schemas
class PayrollReportRequest(BaseModel):
    competency_id: int
    report_type: str = Field(..., pattern=r"^(summary|detailed|holerite|sintetic)$")
    employee_ids: Optional[List[int]] = None
    export_format: str = Field(default="PDF", pattern=r"^(PDF|XLSX|CSV)$")


class PayrollReportResponse(BaseModel):
    report_id: str
    file_url: str
    file_size: int
    generated_at: datetime
