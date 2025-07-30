"""
Prometheus metrics exporter for AUDITORIA360 monitoring system
Implements Prometheus metrics exposition endpoint for Grafana integration
"""

import json
import time
from typing import Dict, List
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CollectorRegistry

from .metrics import MetricsCollector, MetricType


class PrometheusExporter:
    """Exports AUDITORIA360 metrics in Prometheus format"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.registry = CollectorRegistry()
        self._prometheus_metrics = {}
        self._setup_business_metrics()
        
    def _setup_business_metrics(self):
        """Setup business metrics for AUDITORIA360"""
        # Business KPI metrics
        self._prometheus_metrics['auditorias_processadas_total'] = Counter(
            'auditorias_processadas_total',
            'Total number of audits processed',
            ['audit_type', 'status'],
            registry=self.registry
        )
        
        self._prometheus_metrics['usuarios_ativos'] = Gauge(
            'usuarios_ativos_total',
            'Total active users',
            ['user_type'],
            registry=self.registry
        )
        
        self._prometheus_metrics['relatorios_gerados'] = Counter(
            'relatorios_gerados_total',
            'Total reports generated',
            ['report_type'],
            registry=self.registry
        )
        
        self._prometheus_metrics['tempo_processamento_auditoria'] = Histogram(
            'auditoria_processamento_duracao_segundos',
            'Audit processing duration in seconds',
            ['audit_type'],
            buckets=(1, 5, 10, 30, 60, 300, 600, 1800),
            registry=self.registry
        )
        
        # Technical performance metrics
        self._prometheus_metrics['http_requests_total'] = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status_code'],
            registry=self.registry
        )
        
        self._prometheus_metrics['http_request_duration'] = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0),
            registry=self.registry
        )
        
        self._prometheus_metrics['database_connections'] = Gauge(
            'database_connections_active',
            'Active database connections',
            ['database', 'pool'],
            registry=self.registry
        )
        
        # System resource metrics
        self._prometheus_metrics['system_cpu'] = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage percentage',
            registry=self.registry
        )
        
        self._prometheus_metrics['system_memory'] = Gauge(
            'system_memory_usage_percent',
            'System memory usage percentage',
            registry=self.registry
        )
        
        self._prometheus_metrics['system_disk'] = Gauge(
            'system_disk_usage_percent',
            'System disk usage percentage',
            ['mount_point'],
            registry=self.registry
        )
        
        # Compliance and security metrics
        self._prometheus_metrics['compliance_checks'] = Counter(
            'compliance_checks_total',
            'Total compliance checks performed',
            ['check_type', 'result'],
            registry=self.registry
        )
        
        self._prometheus_metrics['security_events'] = Counter(
            'security_events_total',
            'Total security events',
            ['event_type', 'severity'],
            registry=self.registry
        )
        
    def update_business_metrics(self, business_data: Dict):
        """Update business KPI metrics from application data"""
        try:
            # Update audit metrics
            if 'auditorias_processadas' in business_data:
                for audit in business_data['auditorias_processadas']:
                    self._prometheus_metrics['auditorias_processadas_total'].labels(
                        audit_type=audit.get('type', 'unknown'),
                        status=audit.get('status', 'unknown')
                    ).inc()
                    
            # Update active users
            if 'usuarios_ativos' in business_data:
                for user_type, count in business_data['usuarios_ativos'].items():
                    self._prometheus_metrics['usuarios_ativos'].labels(
                        user_type=user_type
                    ).set(count)
                    
            # Update report generation
            if 'relatorios_gerados' in business_data:
                for report in business_data['relatorios_gerados']:
                    self._prometheus_metrics['relatorios_gerados'].labels(
                        report_type=report.get('type', 'unknown')
                    ).inc()
                    
            # Update audit processing time
            if 'audit_processing_times' in business_data:
                for audit_time in business_data['audit_processing_times']:
                    self._prometheus_metrics['tempo_processamento_auditoria'].labels(
                        audit_type=audit_time.get('type', 'unknown')
                    ).observe(audit_time.get('duration', 0))
                    
        except Exception as e:
            print(f"Error updating business metrics: {e}")
            
    def update_technical_metrics(self):
        """Update technical metrics from metrics collector"""
        try:
            metrics_summary = self.metrics_collector.get_metrics_summary(hours=1)
            
            # Update system metrics
            if 'system_cpu_percent' in metrics_summary:
                self._prometheus_metrics['system_cpu'].set(
                    metrics_summary['system_cpu_percent']['latest']
                )
                
            if 'system_memory_percent' in metrics_summary:
                self._prometheus_metrics['system_memory'].set(
                    metrics_summary['system_memory_percent']['latest']
                )
                
            if 'system_disk_percent' in metrics_summary:
                self._prometheus_metrics['system_disk'].labels(
                    mount_point='/'
                ).set(metrics_summary['system_disk_percent']['latest'])
                
        except Exception as e:
            print(f"Error updating technical metrics: {e}")
            
    def record_http_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics"""
        self._prometheus_metrics['http_requests_total'].labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code)
        ).inc()
        
        self._prometheus_metrics['http_request_duration'].labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
    def record_compliance_check(self, check_type: str, result: str):
        """Record compliance check metrics"""
        self._prometheus_metrics['compliance_checks'].labels(
            check_type=check_type,
            result=result
        ).inc()
        
    def record_security_event(self, event_type: str, severity: str):
        """Record security event metrics"""
        self._prometheus_metrics['security_events'].labels(
            event_type=event_type,
            severity=severity
        ).inc()
        
    def get_metrics_output(self) -> str:
        """Get metrics in Prometheus format"""
        # Update technical metrics before generating output
        self.update_technical_metrics()
        
        return generate_latest(self.registry)
        
    def get_content_type(self) -> str:
        """Get the content type for Prometheus metrics"""
        return CONTENT_TYPE_LATEST


# Global prometheus exporter instance
_prometheus_exporter = None


def get_prometheus_exporter(metrics_collector: MetricsCollector) -> PrometheusExporter:
    """Get global prometheus exporter instance"""
    global _prometheus_exporter
    if _prometheus_exporter is None:
        _prometheus_exporter = PrometheusExporter(metrics_collector)
    return _prometheus_exporter