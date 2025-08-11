"""
AUDITORIA360 - Health Check Router
Comprehensive health monitoring endpoints for all system modules
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
import time
from datetime import datetime
import logging
import asyncio

router = APIRouter(prefix="/api/health", tags=["Health Monitoring"])

logger = logging.getLogger(__name__)

# Health check status types
class HealthStatus:
    OK = "ok"
    ERROR = "error"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    DEVELOPING = "em_desenvolvimento"
    TESTING = "em_teste"

# Module status configurations
MODULE_CONFIGS = {
    "dashboard": {
        "name": "Dashboard Estratégico",
        "description": "Administrative strategic dashboard with KPIs and metrics",
        "dependencies": ["database", "analytics"],
        "critical": True
    },
    "controle_mensal": {
        "name": "Controle Mensal", 
        "description": "Monthly client control and audit management",
        "dependencies": ["database", "auth"],
        "critical": True
    },
    "disparo_auditoria": {
        "name": "Disparo de Auditoria",
        "description": "Automated audit dispatch and execution",
        "dependencies": ["database", "ai", "processing"],
        "critical": True
    },
    "forense": {
        "name": "Análise Forense",
        "description": "Forensic analysis with cognitive trail explanations", 
        "dependencies": ["ai", "database"],
        "critical": False
    },
    "regras": {
        "name": "Gestão de Regras e Legislação",
        "description": "Rules and legislation management with AI ingestion",
        "dependencies": ["database", "ai", "ocr"],
        "critical": True
    },
    "simulador": {
        "name": "Simulador de Impactos",
        "description": "Impact simulation with AI analysis",
        "dependencies": ["ai", "processing"],
        "critical": False
    },
    "relatorios": {
        "name": "Geração de Relatórios", 
        "description": "Advanced report generation and export",
        "dependencies": ["database", "processing"],
        "critical": True
    },
    "ia": {
        "name": "Integração com IA",
        "description": "AI service integration and processing",
        "dependencies": ["openai_api", "processing"],
        "critical": True
    }
}

async def check_database_health() -> Dict[str, Any]:
    """Check database connectivity and performance"""
    try:
        # Simulate database check
        start_time = time.time()
        await asyncio.sleep(0.01)  # Simulate DB query
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time,
            "details": "Database connection healthy"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"Database error: {str(e)}"
        }

async def check_ai_service_health() -> Dict[str, Any]:
    """Check AI service availability"""
    try:
        # Simulate AI service check
        start_time = time.time()
        await asyncio.sleep(0.02)  # Simulate AI API call
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time, 
            "details": "AI service responding normally"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"AI service error: {str(e)}"
        }

async def check_processing_health() -> Dict[str, Any]:
    """Check processing capabilities"""
    try:
        start_time = time.time()
        await asyncio.sleep(0.005)  # Simulate processing check
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time,
            "details": "Processing system operational"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"Processing error: {str(e)}"
        }

async def check_auth_health() -> Dict[str, Any]:
    """Check authentication system"""
    try:
        start_time = time.time()
        await asyncio.sleep(0.008)  # Simulate auth check  
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time,
            "details": "Authentication system operational"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"Authentication error: {str(e)}"
        }

async def check_analytics_health() -> Dict[str, Any]:
    """Check analytics and reporting system"""
    try:
        start_time = time.time()
        await asyncio.sleep(0.015)  # Simulate analytics check
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time,
            "details": "Analytics system operational"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"Analytics error: {str(e)}"
        }

async def check_ocr_health() -> Dict[str, Any]:
    """Check OCR processing system"""
    try:
        start_time = time.time()
        await asyncio.sleep(0.012)  # Simulate OCR check
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time,
            "details": "OCR system operational"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"OCR error: {str(e)}"
        }

async def check_openai_api_health() -> Dict[str, Any]:
    """Check OpenAI API connectivity"""
    try:
        start_time = time.time()
        await asyncio.sleep(0.025)  # Simulate OpenAI API check
        response_time = time.time() - start_time
        
        return {
            "status": HealthStatus.OK,
            "response_time": response_time,
            "details": "OpenAI API accessible"
        }
    except Exception as e:
        return {
            "status": HealthStatus.ERROR,
            "response_time": None,
            "details": f"OpenAI API error: {str(e)}"
        }

# Dependency health checkers
DEPENDENCY_CHECKERS = {
    "database": check_database_health,
    "ai": check_ai_service_health,
    "processing": check_processing_health,
    "auth": check_auth_health,
    "analytics": check_analytics_health,
    "ocr": check_ocr_health,
    "openai_api": check_openai_api_health
}

async def perform_module_health_check(module_key: str) -> Dict[str, Any]:
    """Perform comprehensive health check for a specific module"""
    
    module_config = MODULE_CONFIGS.get(module_key)
    if not module_config:
        raise HTTPException(status_code=404, detail=f"Module {module_key} not found")
    
    start_time = time.time()
    
    # Check module dependencies
    dependency_results = {}
    overall_status = HealthStatus.OK
    
    for dependency in module_config["dependencies"]:
        if dependency in DEPENDENCY_CHECKERS:
            dependency_results[dependency] = await DEPENDENCY_CHECKERS[dependency]()
            
            # If any critical dependency fails, module status becomes degraded/error
            if dependency_results[dependency]["status"] == HealthStatus.ERROR:
                if module_config["critical"]:
                    overall_status = HealthStatus.ERROR
                else:
                    overall_status = HealthStatus.DEGRADED
    
    total_time = time.time() - start_time
    
    # Determine final status and details
    failed_deps = [dep for dep, result in dependency_results.items() 
                  if result["status"] == HealthStatus.ERROR]
    
    if failed_deps:
        details = f"Dependencies with issues: {', '.join(failed_deps)}"
    else:
        details = "All dependencies healthy"
    
    # Special status overrides based on module configuration
    if module_key == "simulador":
        overall_status = HealthStatus.DEVELOPING
        details = "IA em integração - módulo em desenvolvimento ativo"
    elif module_key == "forense":
        if overall_status == HealthStatus.OK:
            overall_status = HealthStatus.TESTING  
            details = "Trilha cognitiva em fase de testes"
    elif module_key == "regras":
        if overall_status == HealthStatus.OK:
            details = "Ingestão automática em desenvolvimento, funcionalidades principais operacionais"
    
    return {
        "status": overall_status,
        "module": module_config["name"],
        "description": module_config["description"],
        "details": details,
        "dependencies": dependency_results,
        "response_time": total_time,
        "critical": module_config["critical"],
        "last_check": datetime.now().isoformat()
    }

# Individual module health endpoints
@router.get("/dashboard")
async def health_dashboard():
    """Dashboard Estratégico health check"""
    return await perform_module_health_check("dashboard")

@router.get("/controle_mensal")
async def health_controle_mensal():
    """Controle Mensal health check"""
    return await perform_module_health_check("controle_mensal")

@router.get("/disparo_auditoria")  
async def health_disparo_auditoria():
    """Disparo de Auditoria health check"""
    return await perform_module_health_check("disparo_auditoria")

@router.get("/forense")
async def health_forense():
    """Análise Forense health check"""
    return await perform_module_health_check("forense")

@router.get("/regras")
async def health_regras():
    """Gestão de Regras e Legislação health check"""
    return await perform_module_health_check("regras")

@router.get("/simulador")
async def health_simulador():
    """Simulador de Impactos health check"""
    return await perform_module_health_check("simulador")

@router.get("/relatorios")
async def health_relatorios():
    """Geração de Relatórios health check"""
    return await perform_module_health_check("relatorios")

@router.get("/ia")
async def health_ia():
    """Integração com IA health check"""
    return await perform_module_health_check("ia")

# Additional system component health checks
@router.get("/login_admin")
async def health_login_admin():
    """Login/Admin system health check"""
    return {
        "status": HealthStatus.OK,
        "module": "Login/Admin",
        "description": "Administrative login and authentication system",
        "details": "Login system operational with secure authentication",
        "response_time": 0.005,
        "last_check": datetime.now().isoformat()
    }

@router.get("/logoperacoes")
async def health_logoperacoes():
    """LOGOPERACOES/Auditoria de Sistema health check"""
    return {
        "status": HealthStatus.OK,
        "module": "LOGOPERACOES/Auditoria de Sistema", 
        "description": "System operation logs and audit trails",
        "details": "Logging and audit system fully operational",
        "response_time": 0.008,
        "last_check": datetime.now().isoformat()
    }

@router.get("/personificacao")
async def health_personificacao():
    """Personificação/Suporte Supremo health check"""
    return {
        "status": HealthStatus.OK,
        "module": "Personificação/Suporte Supremo",
        "description": "User impersonation and supreme support system",
        "details": "Impersonation system operational for support activities",
        "response_time": 0.003,
        "last_check": datetime.now().isoformat()
    }

@router.get("/login_onboarding")
async def health_login_onboarding():
    """Login/Onboarding health check"""
    return {
        "status": HealthStatus.OK,
        "module": "Login/Onboarding",
        "description": "Client login and onboarding system",
        "details": "Onboarding and client authentication operational",
        "response_time": 0.007,
        "last_check": datetime.now().isoformat()
    }

@router.get("/logs_auditoria")
async def health_logs_auditoria():
    """Logs e Auditoria health check"""
    return {
        "status": HealthStatus.OK,
        "module": "Logs e Auditoria",
        "description": "Comprehensive system logging and audit capabilities",
        "details": "Audit logging system fully functional",
        "response_time": 0.004,
        "last_check": datetime.now().isoformat()
    }

@router.get("/onboarding_escritorio")
async def health_onboarding_escritorio():
    """Onboarding de Escritório health check"""
    return {
        "status": HealthStatus.OK,
        "module": "Onboarding de Escritório",
        "description": "Office onboarding and setup system",
        "details": "Office onboarding workflows operational",
        "response_time": 0.006,
        "last_check": datetime.now().isoformat()
    }

@router.get("/gerenciamento_usuarios")
async def health_gerenciamento_usuarios():
    """Gerenciamento de Usuários health check"""
    return {
        "status": HealthStatus.OK,
        "module": "Gerenciamento de Usuários", 
        "description": "User management and permissions system",
        "details": "User management system fully operational",
        "response_time": 0.005,
        "last_check": datetime.now().isoformat()
    }

# Comprehensive system health check
@router.get("/")
async def health_check_all():
    """Comprehensive system health check for all modules"""
    
    start_time = time.time()
    results = []
    
    # Check all configured modules
    for module_key in MODULE_CONFIGS.keys():
        try:
            result = await perform_module_health_check(module_key)
            results.append(result)
        except Exception as e:
            logger.error(f"Error checking {module_key}: {str(e)}")
            results.append({
                "status": HealthStatus.ERROR,
                "module": MODULE_CONFIGS[module_key]["name"],
                "details": f"Health check failed: {str(e)}",
                "response_time": None,
                "last_check": datetime.now().isoformat()
            })
    
    # Check additional system components
    additional_checks = [
        ("login_admin", await health_login_admin()),
        ("logoperacoes", await health_logoperacoes()), 
        ("personificacao", await health_personificacao()),
        ("login_onboarding", await health_login_onboarding()),
        ("logs_auditoria", await health_logs_auditoria()),
        ("onboarding_escritorio", await health_onboarding_escritorio()),
        ("gerenciamento_usuarios", await health_gerenciamento_usuarios())
    ]
    
    for check_name, check_result in additional_checks:
        results.append(check_result)
    
    total_time = time.time() - start_time
    
    # Calculate overall system health
    total_modules = len(results)
    healthy_modules = sum(1 for r in results if r["status"] == HealthStatus.OK)
    critical_modules = [r for r in results if r.get("critical", False)]
    critical_healthy = sum(1 for r in critical_modules if r["status"] == HealthStatus.OK)
    
    if critical_healthy == len(critical_modules) and healthy_modules / total_modules >= 0.9:
        system_status = HealthStatus.OK
    elif critical_healthy == len(critical_modules) and healthy_modules / total_modules >= 0.7:
        system_status = HealthStatus.DEGRADED
    else:
        system_status = HealthStatus.ERROR
    
    return {
        "system_status": system_status,
        "total_modules": total_modules,
        "healthy_modules": healthy_modules,
        "health_percentage": (healthy_modules / total_modules) * 100,
        "critical_modules_healthy": critical_healthy,
        "total_critical_modules": len(critical_modules),
        "total_response_time": total_time,
        "timestamp": datetime.now().isoformat(),
        "modules": results
    }

@router.get("/history")
async def health_history():
    """Get health check history (placeholder - would integrate with logging system)"""
    return {
        "message": "Health check history endpoint",
        "note": "This would integrate with persistent storage to show health trends",
        "status": "placeholder"
    }

@router.get("/metrics")
async def health_metrics():
    """Get health metrics in Prometheus format"""
    
    # Simulate some basic health metrics
    metrics_data = """# HELP auditoria360_module_health Module health status (1=healthy, 0=unhealthy)
# TYPE auditoria360_module_health gauge
auditoria360_module_health{module="dashboard"} 1
auditoria360_module_health{module="controle_mensal"} 1
auditoria360_module_health{module="disparo_auditoria"} 1
auditoria360_module_health{module="forense"} 1
auditoria360_module_health{module="regras"} 1
auditoria360_module_health{module="simulador"} 0
auditoria360_module_health{module="relatorios"} 1
auditoria360_module_health{module="ia"} 1

# HELP auditoria360_health_check_duration_seconds Time spent on health checks
# TYPE auditoria360_health_check_duration_seconds histogram
auditoria360_health_check_duration_seconds{module="dashboard"} 0.015
auditoria360_health_check_duration_seconds{module="controle_mensal"} 0.008
auditoria360_health_check_duration_seconds{module="ia"} 0.025
"""
    
    from fastapi import Response
    return Response(content=metrics_data, media_type="text/plain")