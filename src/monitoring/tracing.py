"""
Distributed tracing implementation for AUDITORIA360
Simple tracing implementation using correlation IDs and request tracking
"""

import contextvars
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging


# Context variable for trace ID
trace_id_context: contextvars.ContextVar[str] = contextvars.ContextVar('trace_id', default=None)


@dataclass
class Span:
    """Represents a single span in a trace"""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    operation_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "OK"  # OK, ERROR, TIMEOUT
    
    def finish(self):
        """Finish the span and calculate duration"""
        self.end_time = datetime.now()
        if self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def set_tag(self, key: str, value: Any):
        """Set a tag on the span"""
        self.tags[key] = value
        
    def log(self, message: str, fields: Dict[str, Any] = None):
        """Add a log entry to the span"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "fields": fields or {}
        }
        self.logs.append(log_entry)
        
    def set_error(self, error: Exception):
        """Mark span as error and add error details"""
        self.status = "ERROR"
        self.set_tag("error", True)
        self.set_tag("error.type", type(error).__name__)
        self.set_tag("error.message", str(error))


class TraceCollector:
    """Collects and stores trace data"""
    
    def __init__(self):
        self.traces: Dict[str, List[Span]] = {}
        self.max_traces = 1000  # Keep last 1000 traces
        
    def add_span(self, span: Span):
        """Add a span to the trace collection"""
        if span.trace_id not in self.traces:
            self.traces[span.trace_id] = []
        
        self.traces[span.trace_id].append(span)
        
        # Cleanup old traces if needed
        if len(self.traces) > self.max_traces:
            oldest_trace = min(self.traces.keys(), key=lambda k: min(s.start_time for s in self.traces[k]))
            del self.traces[oldest_trace]
    
    def get_trace(self, trace_id: str) -> List[Span]:
        """Get all spans for a trace"""
        return self.traces.get(trace_id, [])
    
    def get_recent_traces(self, limit: int = 50) -> Dict[str, List[Span]]:
        """Get recent traces"""
        sorted_traces = sorted(
            self.traces.items(),
            key=lambda x: max(s.start_time for s in x[1]),
            reverse=True
        )
        return dict(sorted_traces[:limit])


class Tracer:
    """Simple tracer implementation"""
    
    def __init__(self, service_name: str = "auditoria360"):
        self.service_name = service_name
        self.collector = TraceCollector()
        self.logger = logging.getLogger(f"{service_name}.tracing")
        
    def start_trace(self, operation_name: str, trace_id: Optional[str] = None) -> str:
        """Start a new trace"""
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        trace_id_context.set(trace_id)
        span = self.start_span(operation_name)
        span.set_tag("service.name", self.service_name)
        span.set_tag("trace.root", True)
        
        return trace_id
    
    def start_span(self, operation_name: str, parent_span_id: Optional[str] = None) -> Span:
        """Start a new span"""
        trace_id = trace_id_context.get()
        if trace_id is None:
            trace_id = self.start_trace(f"auto-trace-{operation_name}")
        
        span = Span(
            span_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            operation_name=operation_name,
            start_time=datetime.now()
        )
        
        # Log span start
        self.logger.debug(
            f"Span started: {operation_name}",
            extra={
                "trace_id": trace_id,
                "span_id": span.span_id,
                "parent_span_id": parent_span_id,
                "operation": operation_name
            }
        )
        
        return span
    
    def finish_span(self, span: Span):
        """Finish a span and add it to collector"""
        span.finish()
        self.collector.add_span(span)
        
        # Log span completion
        self.logger.debug(
            f"Span finished: {span.operation_name}",
            extra={
                "trace_id": span.trace_id,
                "span_id": span.span_id,
                "duration": span.duration,
                "status": span.status
            }
        )
    
    def get_current_trace_id(self) -> Optional[str]:
        """Get current trace ID"""
        return trace_id_context.get()


class TracingMiddleware:
    """Middleware for automatic request tracing"""
    
    def __init__(self, tracer: Tracer):
        self.tracer = tracer
        
    async def trace_request(self, request, call_next):
        """Trace an HTTP request"""
        # Extract trace ID from headers if present
        trace_id = request.headers.get("X-Trace-ID")
        
        # Start trace
        if trace_id:
            trace_id_context.set(trace_id)
            span = self.tracer.start_span(f"{request.method} {request.url.path}")
        else:
            trace_id = self.tracer.start_trace(f"{request.method} {request.url.path}")
            span = self.tracer.start_span(f"{request.method} {request.url.path}")
        
        # Set request tags
        span.set_tag("http.method", request.method)
        span.set_tag("http.url", str(request.url))
        span.set_tag("http.scheme", request.url.scheme)
        span.set_tag("http.host", request.url.hostname)
        span.set_tag("http.path", request.url.path)
        
        try:
            response = await call_next(request)
            
            # Set response tags
            span.set_tag("http.status_code", response.status_code)
            if response.status_code >= 400:
                span.status = "ERROR"
                span.set_tag("error", True)
            
            return response
            
        except Exception as e:
            span.set_error(e)
            raise
        finally:
            self.tracer.finish_span(span)


def trace_function(operation_name: Optional[str] = None):
    """Decorator for tracing functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            span = tracer.start_span(op_name)
            span.set_tag("function.name", func.__name__)
            span.set_tag("function.module", func.__module__)
            
            try:
                result = func(*args, **kwargs)
                span.set_tag("function.result_type", type(result).__name__)
                return result
            except Exception as e:
                span.set_error(e)
                raise
            finally:
                tracer.finish_span(span)
                
        return wrapper
    return decorator


def trace_database_operation(operation: str, table: str, query: Optional[str] = None):
    """Trace database operations"""
    tracer = get_tracer()
    span = tracer.start_span(f"db.{operation}")
    
    span.set_tag("db.operation", operation)
    span.set_tag("db.table", table)
    if query:
        span.set_tag("db.query", query[:200])  # Truncate long queries
    
    return span


def trace_external_call(service: str, operation: str, url: Optional[str] = None):
    """Trace external service calls"""
    tracer = get_tracer()
    span = tracer.start_span(f"external.{service}")
    
    span.set_tag("external.service", service)
    span.set_tag("external.operation", operation)
    if url:
        span.set_tag("external.url", url)
    
    return span


# Global tracer instance
_tracer = None


def get_tracer() -> Tracer:
    """Get global tracer instance"""
    global _tracer
    if _tracer is None:
        _tracer = Tracer()
    return _tracer


def setup_tracing(service_name: str = "auditoria360") -> Tracer:
    """Setup distributed tracing"""
    global _tracer
    _tracer = Tracer(service_name)
    return _tracer