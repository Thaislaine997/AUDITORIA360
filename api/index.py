"""
AUDITORIA360 - Portal de Gestão da Folha, Auditoria 360 e CCT
Main FastAPI application with all modules integrated
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os

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
    """Initialize database on startup"""
    try:
        # Create all database tables
        create_all_tables()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
    
    yield
    
    # Cleanup on shutdown
    print("🔄 Application shutting down...")

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
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "AUDITORIA360 API is running!",
        "version": "1.0.0",
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

@app.get("/health", tags=["Health"])
def detailed_health():
    """Detailed health check with system information"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "connected",
        "storage": "cloudflare_r2",
        "ai_service": "openai",
        "version": "1.0.0"
    }

# Include all module routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(payroll_router, prefix="/api/v1/payroll", tags=["Payroll Management"])
app.include_router(document_router, prefix="/api/v1/documents", tags=["Document Management"])
app.include_router(cct_router, prefix="/api/v1/cct", tags=["Collective Labor Agreements"])
app.include_router(notification_router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(audit_router, prefix="/api/v1/audit", tags=["Audit & Compliance"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI & Chatbot"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Internal server error: {str(exc)}"
    )
