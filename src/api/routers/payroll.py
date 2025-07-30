"""
Payroll Management API Router
Módulo 1: Gestão de Folha de Pagamento
Performance optimized with async operations and caching
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.models import User, get_db
from src.schemas.payroll_schemas import (
    Employee,
    EmployeeCreate,
    EmployeeUpdate,
    PayrollCalculationRequest,
    PayrollCalculationResult,
    PayrollCompetency,
    PayrollCompetencyCreate,
    PayrollCompetencyDetail,
    PayrollCompetencyUpdate,
    PayrollImport,
    PayrollItem,
    PayrollItemUpdate,
    PayrollReportRequest,
    PayrollReportResponse,
    PayrollValidationRequest,
    PayrollValidationResult,
)
from src.services.auth_service import get_current_user
from src.services.payroll_service import (
    calculate_payroll_async,
    create_employee,
    create_payroll_competency,
    generate_payroll_report,
    get_employee_by_id,
    get_employees,
    get_payroll_competencies,
    get_payroll_competency_by_id,
    get_payroll_statistics_async,
    import_payroll_data,
    update_employee,
    update_payroll_competency,
    validate_payroll,
)
from src.services.cache_service import cached_response

router = APIRouter()


# Employee management endpoints
@router.post("/employees", response_model=Employee)
async def create_new_employee(
    employee_data: EmployeeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new employee (RH/Admin only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    employee = create_employee(db, employee_data, current_user.id)
    return employee


@router.get("/employees", response_model=List[Employee])
@cached_response("payroll_employees", ttl_seconds=300)
async def read_employees(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    department: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of employees - OPTIMIZED with caching"""
    employees = get_employees(
        db, skip=skip, limit=limit, is_active=is_active, department=department
    )
    return employees


@router.get("/employees/{employee_id}", response_model=Employee)
async def read_employee(
    employee_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get employee by ID"""
    employee = get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee


@router.put("/employees/{employee_id}", response_model=Employee)
async def update_employee_by_id(
    employee_id: int,
    employee_update: EmployeeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update employee by ID (RH/Admin only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    employee = update_employee(db, employee_id, employee_update)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee


# Payroll competency endpoints
@router.post("/competencies", response_model=PayrollCompetency)
async def create_new_competency(
    competency_data: PayrollCompetencyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new payroll competency (RH/Admin only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    competency = create_payroll_competency(db, competency_data, current_user.id)
    return competency


@router.get("/competencies", response_model=List[PayrollCompetency])
async def read_competencies(
    skip: int = 0,
    limit: int = 100,
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of payroll competencies"""
    competencies = get_payroll_competencies(
        db, skip=skip, limit=limit, year=year, month=month
    )
    return competencies


@router.get("/competencies/{competency_id}", response_model=PayrollCompetencyDetail)
async def read_competency(
    competency_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get payroll competency with items by ID"""
    competency = get_payroll_competency_by_id(db, competency_id, include_items=True)
    if competency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payroll competency not found"
        )
    return competency


@router.put("/competencies/{competency_id}", response_model=PayrollCompetency)
async def update_competency_by_id(
    competency_id: int,
    competency_update: PayrollCompetencyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update payroll competency by ID (RH/Admin only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    competency = update_payroll_competency(db, competency_id, competency_update)
    if competency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payroll competency not found"
        )
    return competency


# Payroll calculation endpoints
@router.post("/calculate", response_model=PayrollCalculationResult)
async def calculate_payroll_competency(
    calculation_request: PayrollCalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Calculate payroll for a competency (RH/Admin only) - ASYNC optimized"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    result = await calculate_payroll_async(db, calculation_request, current_user.id)
    return result


# New performance endpoint for payroll statistics
@router.get("/competencies/{competency_id}/statistics")
@cached_response("payroll_statistics", ttl_seconds=600)
async def get_competency_statistics(
    competency_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get payroll statistics for a competency - OPTIMIZED with caching"""
    statistics = await get_payroll_statistics_async(db, competency_id)
    return {
        "competency_id": competency_id,
        "statistics": statistics,
        "cached": True
    }


@router.post("/validate", response_model=PayrollValidationResult)
async def validate_payroll_competency(
    validation_request: PayrollValidationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Validate payroll calculations (RH/Admin/Contador)"""
    if current_user.role not in ["administrador", "rh", "contador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    result = validate_payroll(db, validation_request)
    return result


# Import endpoints
@router.post("/import", response_model=PayrollImport)
async def import_payroll_file(
    file: UploadFile = File(...),
    competency_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Import payroll data from CSV/XLSX file (RH/Admin only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Validate file type
    allowed_types = [
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV and XLSX files are allowed.",
        )

    import_result = await import_payroll_data(db, file, competency_id, current_user.id)
    return import_result


@router.get("/imports", response_model=List[PayrollImport])
async def read_imports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get list of payroll imports"""
    # Implementation would fetch import history
    return []


# Report generation endpoints
@router.post("/reports/generate", response_model=PayrollReportResponse)
async def generate_report(
    report_request: PayrollReportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate payroll report"""
    if current_user.role not in ["administrador", "rh", "contador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    report = generate_payroll_report(db, report_request, current_user.id)
    return report


# Payroll item specific endpoints
@router.get("/competencies/{competency_id}/items", response_model=List[PayrollItem])
async def read_payroll_items(
    competency_id: int,
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get payroll items for a competency"""
    # Implementation would fetch payroll items
    return []


@router.get("/items/{item_id}", response_model=PayrollItem)
async def read_payroll_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get payroll item by ID"""
    # Implementation would fetch specific payroll item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Payroll item not found"
    )


@router.put("/items/{item_id}", response_model=PayrollItem)
async def update_payroll_item(
    item_id: int,
    item_update: PayrollItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update payroll item by ID (RH/Admin only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    # Implementation would update payroll item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Payroll item not found"
    )
