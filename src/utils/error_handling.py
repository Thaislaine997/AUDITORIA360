"""
Sistema centralizado de tratamento de erros.
Fornece classes e utilitários para manejo consistente de erros em todo o sistema.
"""

import logging
import traceback
import sys
from typing import Dict, Any, Optional, Union, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class ErrorSeverity(Enum):
    """Níveis de severidade de erro."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categorias de erro do sistema."""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    CONFIGURATION = "configuration"
    PERFORMANCE = "performance"
    SYSTEM = "system"
    BUSINESS_LOGIC = "business_logic"
    USER_INPUT = "user_input"


@dataclass
class ErrorContext:
    """Contexto adicional para erros."""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    endpoint: Optional[str] = None
    operation: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ApplicationError:
    """Estrutura padronizada de erro da aplicação."""
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    timestamp: datetime = field(default_factory=datetime.now)
    error_code: Optional[str] = None
    details: Optional[str] = None
    context: Optional[ErrorContext] = None
    original_exception: Optional[Exception] = None
    stack_trace: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o erro para dicionário."""
        return {
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat(),
            "error_code": self.error_code,
            "details": self.details,
            "context": self.context.__dict__ if self.context else None,
            "stack_trace": self.stack_trace
        }


class ErrorHandler:
    """Manipulador centralizado de erros."""
    
    def __init__(self, logger_name: str = "auditoria360"):
        self.logger = logging.getLogger(logger_name)
        self.error_handlers: Dict[ErrorCategory, List[Callable]] = {}
        self.error_log: List[ApplicationError] = []
        self.max_error_log_size = 1000
    
    def register_error_handler(self, category: ErrorCategory, handler: Callable[[ApplicationError], None]) -> None:
        """
        Registra um manipulador para uma categoria específica de erro.
        
        Args:
            category: Categoria do erro
            handler: Função que processará o erro
        """
        if category not in self.error_handlers:
            self.error_handlers[category] = []
        self.error_handlers[category].append(handler)
    
    def handle_error(self, error: ApplicationError) -> None:
        """
        Processa um erro através do sistema.
        
        Args:
            error: Erro a ser processado
        """
        try:
            # Adiciona ao log de erros
            self._add_to_error_log(error)
            
            # Log do erro
            self._log_error(error)
            
            # Executa handlers específicos da categoria
            if error.category in self.error_handlers:
                for handler in self.error_handlers[error.category]:
                    try:
                        handler(error)
                    except Exception as e:
                        self.logger.error(f"Erro ao executar handler para {error.category}: {e}")
            
        except Exception as e:
            self.logger.critical(f"Falha crítica no sistema de tratamento de erros: {e}")
    
    def create_error(self, 
                    message: str,
                    category: ErrorCategory,
                    severity: ErrorSeverity,
                    error_code: Optional[str] = None,
                    details: Optional[str] = None,
                    context: Optional[ErrorContext] = None,
                    original_exception: Optional[Exception] = None) -> ApplicationError:
        """
        Cria um erro padronizado.
        
        Args:
            message: Mensagem do erro
            category: Categoria do erro
            severity: Severidade do erro
            error_code: Código opcional do erro
            details: Detalhes adicionais
            context: Contexto do erro
            original_exception: Exceção original se houver
            
        Returns:
            ApplicationError: Erro criado
        """
        stack_trace = None
        if original_exception:
            stack_trace = ''.join(traceback.format_exception(
                type(original_exception), 
                original_exception, 
                original_exception.__traceback__
            ))
        
        return ApplicationError(
            message=message,
            category=category,
            severity=severity,
            error_code=error_code,
            details=details,
            context=context,
            original_exception=original_exception,
            stack_trace=stack_trace
        )
    
    def _add_to_error_log(self, error: ApplicationError) -> None:
        """Adiciona erro ao log interno."""
        self.error_log.append(error)
        
        # Mantém tamanho máximo do log
        if len(self.error_log) > self.max_error_log_size:
            self.error_log = self.error_log[-self.max_error_log_size:]
    
    def _log_error(self, error: ApplicationError) -> None:
        """Registra o erro no sistema de logging."""
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(error.severity, logging.ERROR)
        
        log_message = f"[{error.category.value}] {error.message}"
        if error.error_code:
            log_message = f"[{error.error_code}] {log_message}"
        
        extra_info = {
            "category": error.category.value,
            "severity": error.severity.value,
            "error_code": error.error_code,
            "timestamp": error.timestamp.isoformat()
        }
        
        if error.context:
            extra_info.update(error.context.__dict__)
        
        self.logger.log(log_level, log_message, extra=extra_info)
        
        if error.details:
            self.logger.log(log_level, f"Details: {error.details}")
        
        if error.stack_trace and error.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            self.logger.log(log_level, f"Stack trace:\n{error.stack_trace}")
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """
        Obtém resumo dos erros das últimas horas.
        
        Args:
            hours: Número de horas para análise
            
        Returns:
            dict: Resumo dos erros
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = [e for e in self.error_log if e.timestamp > cutoff_time]
        
        summary = {
            "total_errors": len(recent_errors),
            "by_category": {},
            "by_severity": {},
            "critical_errors": []
        }
        
        for error in recent_errors:
            # Por categoria
            cat = error.category.value
            summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1
            
            # Por severidade
            sev = error.severity.value
            summary["by_severity"][sev] = summary["by_severity"].get(sev, 0) + 1
            
            # Erros críticos
            if error.severity == ErrorSeverity.CRITICAL:
                summary["critical_errors"].append(error.to_dict())
        
        return summary


class RetryHandler:
    """Manipulador de tentativas com backoff exponencial."""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
    
    def retry_with_backoff(self, 
                          func: Callable,
                          max_attempts: int = 3,
                          base_delay: float = 1.0,
                          max_delay: float = 60.0,
                          backoff_factor: float = 2.0,
                          exceptions: tuple = (Exception,),
                          error_category: ErrorCategory = ErrorCategory.SYSTEM) -> Any:
        """
        Executa função com retry e backoff exponencial.
        
        Args:
            func: Função a ser executada
            max_attempts: Número máximo de tentativas
            base_delay: Delay inicial em segundos
            max_delay: Delay máximo em segundos
            backoff_factor: Fator de multiplicação do delay
            exceptions: Tupla de exceções que justificam retry
            error_category: Categoria do erro para logging
            
        Returns:
            Resultado da função ou levanta exceção final
        """
        last_exception = None
        delay = base_delay
        
        for attempt in range(max_attempts):
            try:
                return func()
            except exceptions as e:
                last_exception = e
                
                if attempt == max_attempts - 1:
                    # Última tentativa - registra erro e levanta exceção
                    error = self.error_handler.create_error(
                        message=f"Falha após {max_attempts} tentativas: {str(e)}",
                        category=error_category,
                        severity=ErrorSeverity.HIGH,
                        details=f"Função: {func.__name__ if hasattr(func, '__name__') else 'unknown'}",
                        original_exception=e
                    )
                    self.error_handler.handle_error(error)
                    raise e
                
                # Registra tentativa falha
                error = self.error_handler.create_error(
                    message=f"Tentativa {attempt + 1} falhou: {str(e)}",
                    category=error_category,
                    severity=ErrorSeverity.MEDIUM,
                    details=f"Tentando novamente em {delay} segundos",
                    original_exception=e
                )
                self.error_handler.handle_error(error)
                
                # Aguarda antes da próxima tentativa
                import time
                time.sleep(delay)
                delay = min(delay * backoff_factor, max_delay)
        
        # Nunca deve chegar aqui, mas por segurança
        if last_exception:
            raise last_exception


class ValidationError(Exception):
    """Exceção para erros de validação."""
    
    def __init__(self, message: str, field: Optional[str] = None, 
                 validation_code: Optional[str] = None):
        self.message = message
        self.field = field
        self.validation_code = validation_code
        super().__init__(message)


class BusinessLogicError(Exception):
    """Exceção para erros de lógica de negócio."""
    
    def __init__(self, message: str, business_rule: Optional[str] = None):
        self.message = message
        self.business_rule = business_rule
        super().__init__(message)


class ExternalServiceError(Exception):
    """Exceção para erros de serviços externos."""
    
    def __init__(self, message: str, service_name: Optional[str] = None, 
                 status_code: Optional[int] = None):
        self.message = message
        self.service_name = service_name
        self.status_code = status_code
        super().__init__(message)


# Instância global do manipulador de erros
error_handler = ErrorHandler()
retry_handler = RetryHandler(error_handler)


def handle_exceptions(category: ErrorCategory = ErrorCategory.SYSTEM,
                     severity: ErrorSeverity = ErrorSeverity.HIGH,
                     reraise: bool = True):
    """
    Decorator para tratamento automático de exceções.
    
    Args:
        category: Categoria do erro
        severity: Severidade do erro
        reraise: Se deve re-levantar a exceção
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error = error_handler.create_error(
                    message=f"Erro em {func.__name__}: {str(e)}",
                    category=category,
                    severity=severity,
                    details=f"Args: {args}, Kwargs: {kwargs}",
                    original_exception=e
                )
                error_handler.handle_error(error)
                
                if reraise:
                    raise
                return None
        return wrapper
    return decorator


def safe_execute(func: Callable, 
                default_value: Any = None,
                category: ErrorCategory = ErrorCategory.SYSTEM) -> Any:
    """
    Executa função de forma segura, retornando valor padrão em caso de erro.
    
    Args:
        func: Função a ser executada
        default_value: Valor padrão em caso de erro
        category: Categoria do erro
        
    Returns:
        Resultado da função ou valor padrão
    """
    try:
        return func()
    except Exception as e:
        error = error_handler.create_error(
            message=f"Execução segura falhou: {str(e)}",
            category=category,
            severity=ErrorSeverity.MEDIUM,
            original_exception=e
        )
        error_handler.handle_error(error)
        return default_value