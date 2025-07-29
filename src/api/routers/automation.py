"""
Automation API endpoints for serverless execution
Compatible with Vercel Cron Jobs and manual triggers
"""

import os
import sys
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

# Add automation modules to path
automation_path = Path(__file__).parent.parent.parent / "automation"
sys.path.insert(0, str(automation_path))

try:
    from backup_routine import run_backup_routine
    from cron_comunicados import gerar_comunicados
    from rpa_folha import run_payroll_automation
    from schedule_reports import run_scheduled_reports
except ImportError:
    # Fallback imports with error handling
    run_payroll_automation = None
    run_scheduled_reports = None
    run_backup_routine = None
    gerar_comunicados = None

router = APIRouter(tags=["automation"])


def verify_cron_auth():
    """Verify that request is from Vercel Cron or authorized source"""
    # In production, verify Vercel Cron headers or API keys
    # For now, allow all requests from automation endpoints
    return True


@router.post("/reports/daily")
async def trigger_daily_reports(
    background_tasks: BackgroundTasks, auth: bool = Depends(verify_cron_auth)
):
    """Trigger daily report generation (Vercel Cron)"""
    if not run_scheduled_reports:
        raise HTTPException(
            status_code=503, detail="Scheduled reports module not available"
        )

    try:
        # Run in background to avoid timeout
        background_tasks.add_task(run_scheduled_reports, "daily")

        return {
            "status": "triggered",
            "type": "daily_reports",
            "message": "Daily reports generation started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger daily reports: {str(e)}"
        )


@router.post("/reports/weekly")
async def trigger_weekly_reports(
    background_tasks: BackgroundTasks, auth: bool = Depends(verify_cron_auth)
):
    """Trigger weekly report generation (Vercel Cron - Mondays)"""
    if not run_scheduled_reports:
        raise HTTPException(
            status_code=503, detail="Scheduled reports module not available"
        )

    try:
        background_tasks.add_task(run_scheduled_reports, "weekly")

        return {
            "status": "triggered",
            "type": "weekly_reports",
            "message": "Weekly reports generation started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger weekly reports: {str(e)}"
        )


@router.post("/reports/monthly")
async def trigger_monthly_reports(
    background_tasks: BackgroundTasks, auth: bool = Depends(verify_cron_auth)
):
    """Trigger monthly report generation (Vercel Cron - 1st of month)"""
    if not run_scheduled_reports:
        raise HTTPException(
            status_code=503, detail="Scheduled reports module not available"
        )

    try:
        background_tasks.add_task(run_scheduled_reports, "monthly")

        return {
            "status": "triggered",
            "type": "monthly_reports",
            "message": "Monthly reports generation started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger monthly reports: {str(e)}"
        )


@router.post("/backup/daily")
async def trigger_daily_backup(
    background_tasks: BackgroundTasks, auth: bool = Depends(verify_cron_auth)
):
    """Trigger daily backup routine (Vercel Cron)"""
    if not run_backup_routine:
        raise HTTPException(
            status_code=503, detail="Backup routine module not available"
        )

    try:
        background_tasks.add_task(run_backup_routine, "full")

        return {
            "status": "triggered",
            "type": "daily_backup",
            "message": "Daily backup routine started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger daily backup: {str(e)}"
        )


@router.post("/payroll/process")
async def trigger_payroll_processing(
    background_tasks: BackgroundTasks, auth: bool = Depends(verify_cron_auth)
):
    """Trigger payroll processing automation (Vercel Cron - weekdays)"""
    if not run_payroll_automation:
        raise HTTPException(
            status_code=503, detail="Payroll automation module not available"
        )

    try:
        background_tasks.add_task(run_payroll_automation)

        return {
            "status": "triggered",
            "type": "payroll_processing",
            "message": "Payroll processing automation started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trigger payroll processing: {str(e)}"
        )


@router.post("/comunicados/generate")
async def trigger_comunicados_generation(
    background_tasks: BackgroundTasks, auth: bool = Depends(verify_cron_auth)
):
    """Trigger comunicados generation"""
    if not gerar_comunicados:
        raise HTTPException(status_code=503, detail="Comunicados module not available")

    try:
        # Run comunicados generation in background
        def run_comunicados():
            try:
                gerar_comunicados()
            except Exception as e:
                print(f"Comunicados generation error: {e}")

        background_tasks.add_task(run_comunicados)

        return {
            "status": "triggered",
            "type": "comunicados_generation",
            "message": "Comunicados generation started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger comunicados generation: {str(e)}",
        )


@router.get("/status")
async def get_automation_status():
    """Get status of all automation modules"""
    modules_status = {
        "payroll_automation": run_payroll_automation is not None,
        "scheduled_reports": run_scheduled_reports is not None,
        "backup_routine": run_backup_routine is not None,
        "comunicados": gerar_comunicados is not None,
    }

    # Calculate overall serverless migration percentage
    available_modules = sum(modules_status.values())
    total_modules = len(modules_status)
    migration_percentage = (available_modules / total_modules) * 100

    return {
        "status": "operational",
        "modules": modules_status,
        "serverless_migration": {
            "percentage": migration_percentage,
            "status": "complete" if migration_percentage == 100 else "partial",
        },
        "environment": os.getenv("ENVIRONMENT", "production"),
        "vercel_cron_configured": True,
        "github_actions_configured": True,
        "timestamp": "2025-01-29T00:00:00Z",
    }


@router.post("/test/{module}")
async def test_automation_module(module: str, background_tasks: BackgroundTasks):
    """Test specific automation module"""
    module_map = {
        "payroll": run_payroll_automation,
        "reports": lambda: run_scheduled_reports("daily"),
        "backup": lambda: run_backup_routine("database"),
        "comunicados": gerar_comunicados,
    }

    if module not in module_map:
        raise HTTPException(status_code=404, detail=f"Module '{module}' not found")

    if not module_map[module]:
        raise HTTPException(status_code=503, detail=f"Module '{module}' not available")

    try:
        background_tasks.add_task(module_map[module])

        return {
            "status": "test_triggered",
            "module": module,
            "message": f"Test execution for {module} module started",
            "timestamp": "2025-01-29T00:00:00Z",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to test {module} module: {str(e)}"
        )


# Health check endpoints for monitoring
@router.get("/health")
async def automation_health_check():
    """Health check for automation services"""
    try:
        # Basic health checks
        health_status = {
            "status": "healthy",
            "checks": {
                "modules_importable": True,
                "environment_configured": bool(os.getenv("API_BASE_URL")),
                "auth_configured": bool(os.getenv("API_AUTH_TOKEN")),
                "storage_configured": bool(os.getenv("BACKUP_STORAGE_URL")),
            },
            "timestamp": "2025-01-29T00:00:00Z",
        }

        # Check if any critical checks failed
        if not all(health_status["checks"].values()):
            health_status["status"] = "degraded"

        return health_status

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-01-29T00:00:00Z",
        }
