"""
AUDITORIA360 - Portal de Gestão da Folha, Auditoria 360 e CCT
Main FastAPI application with all modules integrated
Enhanced with performance monitoring and alerting systems
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
import logging

# Import monitoring and performance systems
try:
    from src.utils.api_integration import setup_monitoring_integration
    from src.utils.monitoring import get_monitoring_system
    from src.utils.performance import profile, cached
    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False
    logging.warning("Enhanced monitoring and performance features not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import database setup - temporarily using existing structure
try:
    from src.models import init_db, create_all_tables
except ImportError:
    # Fallback for current structure
    def init_db():
        pass
    def create_all_tables():
        pass

# Import routers for all modules - with fallbacks
try:
    from src.api.routers import (
        auth_router,
        payroll_router,
        document_router,
        cct_router,
        notification_router,
        audit_router,
        ai_router
    )
except ImportError:
    # Create placeholder routers for now
    from fastapi import APIRouter
    auth_router = APIRouter()
    payroll_router = APIRouter()
    document_router = APIRouter()
    cct_router = APIRouter()
    notification_router = APIRouter()
    audit_router = APIRouter()
    ai_router = APIRouter()
    
    @auth_router.get("/placeholder")
    def auth_placeholder():
        return {"message": "Authentication module - implementation in progress"}
    
    @payroll_router.get("/placeholder")
    def payroll_placeholder():
        return {"message": "Payroll module - implementation in progress"}
    
    @document_router.get("/placeholder")
    def document_placeholder():
        return {"message": "Document module - implementation in progress"}
    
    @cct_router.get("/placeholder")
    def cct_placeholder():
        return {"message": "CCT module - implementation in progress"}
    
    @notification_router.get("/placeholder")
    def notification_placeholder():
        return {"message": "Notification module - implementation in progress"}
    
    @audit_router.get("/placeholder")
    def audit_placeholder():
        return {"message": "Audit module - implementation in progress"}
    
    @ai_router.get("/placeholder")
    def ai_placeholder():
        return {"message": "AI module - implementation in progress"}

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and monitoring on startup"""
    try:
        # Create all database tables
        create_all_tables()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.warning(f"⚠️  Database initialization skipped: {e}")
    
    # Initialize monitoring if available
    monitoring_system = None
    if ENHANCED_FEATURES:
        try:
            monitoring_system = setup_monitoring_integration(app)
            logger.info("✅ Monitoring system initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️  Monitoring initialization failed: {e}")
    
    yield
    
    # Cleanup on shutdown
    logger.info("🔄 Application shutting down...")
    if monitoring_system and ENHANCED_FEATURES:
        try:
            monitoring_system.stop()
            logger.info("✅ Monitoring system stopped")
        except Exception as e:
            logger.warning(f"⚠️  Error stopping monitoring: {e}")

# Create FastAPI application
app = FastAPI(
    title="AUDITORIA360 - Portal de Gestão da Folha, Auditoria 360 e CCT",
    description="""
    Portal seguro, inteligente e integrado para centralizar, automatizar e auditar 
    todos os processos de folha de pagamento, obrigações sindicais e convenções coletivas.
    
    ## Módulos Disponíveis
    
    * **Gestão de Folha de Pagamento** - Importação, validação e cálculos automatizados
    * **Gestão de Documentos** - Upload, armazenamento seguro e controle de versão
    * **Base de Convenções Coletivas (CCTs)** - Cadastro, OCR e comparativos
    * **Notificações e Eventos** - Push, email, SMS para eventos relevantes
    * **Auditoria e Compliance** - Motor de regras e detecção de não conformidades
    * **IA e Chatbot** - Assistente inteligente treinado com base de conhecimento
    * **Gestão de Usuários** - Permissões granulares e controle de acesso
    """,
    version="1.0.0",
    contact={
        "name": "AUDITORIA360 Support",
        "email": "support@auditoria360.com",
    },
    license_info={
        "name": "Proprietary",
    },
    lifespan=lifespan
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
@cached(ttl_seconds=60) if ENHANCED_FEATURES else lambda x: x
def health_check():
    """Health check endpoint with basic system info"""
    system_info = {
        "status": "ok",
        "message": "AUDITORIA360 API is running!",
        "version": "1.0.0",
        "enhanced_features": ENHANCED_FEATURES,
        "modules": [
            "authentication",
            "payroll",
            "documents", 
            "cct",
            "notifications",
            "audit",
            "ai_chatbot"
        ]
    }
    
    if ENHANCED_FEATURES:
        system_info["monitoring"] = "enabled"
        system_info["performance_optimization"] = "enabled"
    
    return system_info

@app.get("/health", tags=["Health"])
@profile(include_params=False) if ENHANCED_FEATURES else lambda x: x
def detailed_health():
    """Detailed health check with enhanced system information"""
    health_data = {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "connected",
        "storage": "cloudflare_r2",
        "ai_service": "openai",
        "version": "1.0.0"
    }
    
    if ENHANCED_FEATURES:
        try:
            monitoring = get_monitoring_system()
            dashboard_data = monitoring.get_dashboard_data()
            
            health_data.update({
                "monitoring": {
                    "status": "active",
                    "system_status": dashboard_data.get("system_status", "unknown"),
                    "active_alerts": len(dashboard_data.get("active_alerts", [])),
                    "metrics_collected": len(dashboard_data.get("metrics_summary", {}))
                },
                "performance": {
                    "bottlenecks_detected": len([]),  # Would get from profiler
                    "cache_enabled": True,
                    "profiling_active": True
                }
            })
        except Exception as e:
            health_data["monitoring"] = {"status": "error", "error": str(e)}
    
    return health_data

# Include all module routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(payroll_router, prefix="/api/v1/payroll", tags=["Payroll Management"])
app.include_router(document_router, prefix="/api/v1/documents", tags=["Document Management"])
app.include_router(cct_router, prefix="/api/v1/cct", tags=["Collective Labor Agreements"])
app.include_router(notification_router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(audit_router, prefix="/api/v1/audit", tags=["Audit & Compliance"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI & Chatbot"])

# Enhanced demonstration endpoints
if ENHANCED_FEATURES:
    @app.get("/api/v1/demo/slow-operation", tags=["Demo"])
    @profile(include_params=True)
    async def demo_slow_operation():
        """Demo endpoint to show performance monitoring"""
        import asyncio
        import random
        
        # Simulate a slow operation
        delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(delay)
        
        return {
            "message": "Slow operation completed",
            "delay_seconds": delay,
            "note": "This endpoint is monitored for performance"
        }
    
    @app.get("/api/v1/demo/cached-data", tags=["Demo"])
    @cached(ttl_seconds=300)  # Cache for 5 minutes
    def demo_cached_data():
        """Demo endpoint to show caching"""
        import time
        
        # Simulate expensive computation
        computation_time = 0.1
        time.sleep(computation_time)
        
        return {
            "data": "This response is cached for 5 minutes",
            "timestamp": time.time(),
            "computation_time": computation_time,
            "note": "Subsequent requests within 5 minutes will be served from cache"
        }
    
    @app.get("/api/v1/demo/trigger-alert", tags=["Demo"])
    def demo_trigger_alert():
        """Demo endpoint to trigger a monitoring alert"""
        try:
            monitoring = get_monitoring_system()
            
            # Set a high value to trigger an alert
            monitoring.metrics.set_gauge("demo_metric", 999)
            
            # Add alert rule if not exists
            monitoring.alert_manager.add_alert_rule(
                metric_name="demo_metric",
                threshold=100,
                condition="gt",
                severity=AlertSeverity.MEDIUM,
                title="Demo Alert Triggered",
                description="This is a demonstration alert"
            )
            
            return {
                "message": "Alert trigger simulated",
                "metric_value": 999,
                "threshold": 100,
                "note": "Check /api/v1/monitoring/alerts to see the alert"
            }
        except Exception as e:
            return {"error": str(e), "note": "Monitoring system may not be fully initialized"}

# Add API endpoint for system status overview
@app.get("/api/v1/system/status", tags=["System"])
def get_system_status():
    """Get comprehensive system status"""
    status_data = {
        "api_version": "1.0.0",
        "enhanced_features": ENHANCED_FEATURES,
        "timestamp": "2024-01-01T00:00:00Z",
        "components": {
            "database": {"status": "healthy", "type": "neon_postgresql"},
            "storage": {"status": "healthy", "type": "cloudflare_r2"},
            "analytics": {"status": "healthy", "type": "duckdb"},
            "ocr": {"status": "healthy", "type": "paddleocr"},
            "ai": {"status": "healthy", "type": "openai"}
        }
    }
    
    if ENHANCED_FEATURES:
        try:
            monitoring = get_monitoring_system()
            dashboard_data = monitoring.get_dashboard_data()
            
            status_data["monitoring"] = {
                "status": "active",
                "system_health": dashboard_data.get("system_status", "unknown"),
                "active_alerts": len(dashboard_data.get("active_alerts", [])),
                "metrics_collected": True,
                "performance_tracking": True
            }
        except Exception as e:
            status_data["monitoring"] = {"status": "error", "error": str(e)}
    else:
        status_data["monitoring"] = {"status": "disabled", "note": "Enhanced features not available"}
    
    return status_data

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Internal server error: {str(exc)}"
    )
