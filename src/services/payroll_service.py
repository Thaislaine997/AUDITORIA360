"""
Payroll service for AUDITORIA360
Performance optimized with caching and async operations
"""

import asyncio
import logging
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload, selectinload

from src.models import Employee, PayrollCompetency, PayrollItem
from src.schemas.payroll_schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    PayrollCalculationRequest,
    PayrollCalculationResult,
    PayrollCompetencyCreate,
    PayrollCompetencyUpdate,
    PayrollReportRequest,
    PayrollReportResponse,
    PayrollValidationRequest,
    PayrollValidationResult,
)
from src.services.cache_service import cached_query, cache_service, CacheKeys

logger = logging.getLogger(__name__)


def create_employee(
    db: Session, employee_data: EmployeeCreate, created_by_id: int
) -> Employee:
    """Create a new employee"""
    # Check if employee ID already exists
    existing_employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_data.employee_id)
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Employee ID already exists"
        )

    db_employee = Employee(**employee_data.dict(), created_by_id=created_by_id)

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


@cached_query("employees", ttl_seconds=300)
def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    department: Optional[str] = None,
) -> List[Employee]:
    """Get list of employees with optional filtering - OPTIMIZED with caching"""
    query = db.query(Employee)

    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)

    if department:
        query = query.filter(Employee.department == department)

    # Add indices optimization query
    return query.offset(skip).limit(limit).all()


@cached_query("employee_by_id", ttl_seconds=600)
def get_employee_by_id(db: Session, employee_id: int) -> Optional[Employee]:
    """Get employee by ID - OPTIMIZED with caching"""
    return db.query(Employee).filter(Employee.id == employee_id).first()


async def get_employees_with_payroll_async(
    db: Session, competency_id: int
) -> List[Employee]:
    """
    Get employees with their payroll items for a competency - ASYNC optimized
    Eliminates N+1 query problem
    """
    
    def _get_employees_with_payroll():
        return (
            db.query(Employee)
            .join(PayrollItem, Employee.id == PayrollItem.employee_id)
            .filter(PayrollItem.competency_id == competency_id)
            .options(
                selectinload(Employee.payroll_items).joinedload(PayrollItem.competency)
            )
            .all()
        )
    
    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _get_employees_with_payroll)


def update_employee(
    db: Session, employee_id: int, employee_update: EmployeeUpdate
) -> Optional[Employee]:
    """Update employee by ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return None

    update_data = employee_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


def create_payroll_competency(
    db: Session, competency_data: PayrollCompetencyCreate, created_by_id: int
) -> PayrollCompetency:
    """Create a new payroll competency"""
    # Check if competency already exists for this year/month/type
    existing_competency = (
        db.query(PayrollCompetency)
        .filter(
            PayrollCompetency.year == competency_data.year,
            PayrollCompetency.month == competency_data.month,
            PayrollCompetency.type == competency_data.type,
        )
        .first()
    )

    if existing_competency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payroll competency already exists for this period",
        )

    db_competency = PayrollCompetency(
        **competency_data.dict(), created_by_id=created_by_id
    )

    db.add(db_competency)
    db.commit()
    db.refresh(db_competency)

    return db_competency


@cached_query("payroll_competencies", ttl_seconds=300)
def get_payroll_competencies(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> List[PayrollCompetency]:
    """Get list of payroll competencies with optional filtering - OPTIMIZED"""
    query = db.query(PayrollCompetency)

    if year:
        query = query.filter(PayrollCompetency.year == year)

    if month:
        query = query.filter(PayrollCompetency.month == month)

    return query.offset(skip).limit(limit).all()


@cached_query("payroll_competency_detail", ttl_seconds=600)
def get_payroll_competency_by_id(
    db: Session, competency_id: int, include_items: bool = False
) -> Optional[PayrollCompetency]:
    """Get payroll competency by ID - OPTIMIZED with eager loading"""
    query = db.query(PayrollCompetency).filter(PayrollCompetency.id == competency_id)
    
    if include_items:
        # Use joinedload to avoid N+1 problem
        query = query.options(
            joinedload(PayrollCompetency.payroll_items).joinedload(PayrollItem.employee)
        )

    competency = query.first()
    return competency


async def get_payroll_statistics_async(db: Session, competency_id: int) -> dict:
    """
    Get payroll statistics for a competency - ASYNC optimized
    Uses raw SQL for better performance on aggregations
    """
    
    def _get_statistics():
        sql = text("""
            SELECT 
                COUNT(*) as total_employees,
                SUM(gross_salary) as total_gross,
                SUM(net_salary) as total_net,
                SUM(total_deductions) as total_deductions,
                AVG(gross_salary) as avg_gross_salary,
                COUNT(CASE WHEN has_divergences = true THEN 1 END) as divergences_count
            FROM payroll_items 
            WHERE competency_id = :competency_id
        """)
        
        result = db.execute(sql, {"competency_id": competency_id}).fetchone()
        
        if result:
            return {
                "total_employees": result.total_employees or 0,
                "total_gross": float(result.total_gross or 0),
                "total_net": float(result.total_net or 0),
                "total_deductions": float(result.total_deductions or 0),
                "avg_gross_salary": float(result.avg_gross_salary or 0),
                "divergences_count": result.divergences_count or 0,
            }
        return {}
    
    # Cache the results
    cache_key = CacheKeys.query_result("payroll_stats", str(competency_id))
    cached_result = cache_service.get(cache_key)
    
    if cached_result:
        return cached_result
    
    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _get_statistics)
    
    # Cache for 10 minutes
    cache_service.set(cache_key, result, 600)
    return result


def update_payroll_competency(
    db: Session, competency_id: int, competency_update: PayrollCompetencyUpdate
) -> Optional[PayrollCompetency]:
    """Update payroll competency by ID"""
    competency = (
        db.query(PayrollCompetency)
        .filter(PayrollCompetency.id == competency_id)
        .first()
    )

    if not competency:
        return None

    update_data = competency_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(competency, field, value)

    db.commit()
    db.refresh(competency)
    return competency


async def calculate_payroll_async(
    db: Session, calculation_request: PayrollCalculationRequest, user_id: int
) -> PayrollCalculationResult:
    """
    Calculate payroll for a competency - ASYNC optimized version
    Processes calculations in batches to improve performance
    """
    
    def _calculate_batch(batch_employees: List[Employee], competency: PayrollCompetency) -> dict:
        """Calculate payroll for a batch of employees"""
        results = {
            "successful": 0,
            "failed": 0,
            "errors": [],
            "warnings": []
        }
        
        for employee in batch_employees:
            try:
                # Placeholder calculation logic - would implement actual calculation
                # This would include INSS, FGTS, IRRF calculations based on CCT rules
                
                # Simulate calculation time
                import time
                time.sleep(0.01)  # Simulate processing time
                
                results["successful"] += 1
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Employee {employee.id}: {str(e)}")
        
        return results
    
    competency = get_payroll_competency_by_id(db, calculation_request.competency_id)
    if not competency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payroll competency not found"
        )

    # Get employees for this competency
    employees = await get_employees_with_payroll_async(db, calculation_request.competency_id)
    
    # Process in batches of 50 employees for better performance
    batch_size = 50
    batches = [employees[i:i + batch_size] for i in range(0, len(employees), batch_size)]
    
    total_results = {
        "successful": 0,
        "failed": 0,
        "errors": [],
        "warnings": []
    }
    
    # Process batches concurrently
    loop = asyncio.get_event_loop()
    tasks = []
    
    for batch in batches:
        task = loop.run_in_executor(None, _calculate_batch, batch, competency)
        tasks.append(task)
    
    batch_results = await asyncio.gather(*tasks)
    
    # Aggregate results
    for result in batch_results:
        total_results["successful"] += result["successful"]
        total_results["failed"] += result["failed"]
        total_results["errors"].extend(result["errors"])
        total_results["warnings"].extend(result["warnings"])
    
    # Invalidate related caches
    cache_service.clear_pattern(f"payroll_competency_detail:*{calculation_request.competency_id}*")
    cache_service.clear_pattern(f"payroll_stats:*{calculation_request.competency_id}*")
    
    return PayrollCalculationResult(
        competency_id=calculation_request.competency_id,
        total_calculated=len(employees),
        successful=total_results["successful"],
        failed=total_results["failed"],
        errors=total_results["errors"],
        warnings=total_results["warnings"],
    )


def calculate_payroll(
    db: Session, calculation_request: PayrollCalculationRequest, user_id: int
) -> PayrollCalculationResult:
    """
    Calculate payroll for a competency - Synchronous wrapper for backward compatibility
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(
            calculate_payroll_async(db, calculation_request, user_id)
        )
    finally:
        loop.close()


def validate_payroll(
    db: Session, validation_request: PayrollValidationRequest
) -> PayrollValidationResult:
    """Validate payroll calculations"""
    # This is a placeholder implementation
    # In a real implementation, this would:
    # 1. Get the competency and its items
    # 2. Apply validation rules
    # 3. Check for compliance with CCT rules
    # 4. Return validation results

    competency = get_payroll_competency_by_id(db, validation_request.competency_id)
    if not competency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payroll competency not found"
        )

    return PayrollValidationResult(
        competency_id=validation_request.competency_id,
        is_valid=True,  # Placeholder
        errors=[],
        warnings=[],
        divergences=[],
    )


async def import_payroll_data(db: Session, file, competency_id: int, user_id: int):
    """Import payroll data from file"""
    # This is a placeholder implementation
    # In a real implementation, this would:
    # 1. Save file to temporary location
    # 2. Parse CSV/XLSX file
    # 3. Validate data
    # 4. Create/update employee and payroll item records
    # 5. Return import results

    return {
        "message": "Payroll import - implementation pending",
        "filename": file.filename,
        "status": "pending",
    }


def generate_payroll_report(
    db: Session, report_request: PayrollReportRequest, user_id: int
) -> PayrollReportResponse:
    """Generate payroll report"""
    # This is a placeholder implementation
    # In a real implementation, this would:
    # 1. Get competency and payroll data
    # 2. Generate report based on type
    # 3. Save to R2 storage
    # 4. Return download URL

    from datetime import datetime

    return PayrollReportResponse(
        report_id="placeholder-report-id",
        file_url="/api/v1/reports/download/placeholder-report-id",
        file_size=1024,
        generated_at=datetime.utcnow(),
    )
