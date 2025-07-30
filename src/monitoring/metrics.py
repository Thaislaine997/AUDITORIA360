"""
Metrics collection and management for AUDITORIA360 monitoring system
"""

import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class MetricType(Enum):
    """Types of metrics"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Metric data structure"""
    name: str
    value: Union[int, float]
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    help_text: Optional[str] = None


class MetricsCollector:
    """Collects and stores application metrics"""

    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = {}
        self._lock = threading.Lock()
        self.retention_hours = 24

    def record_metric(
        self,
        name: str,
        value: Union[int, float],
        metric_type: MetricType,
        labels: Dict[str, str] = None,
        help_text: str = None,
    ):
        """Record a metric value"""
        with self._lock:
            if name not in self.metrics:
                self.metrics[name] = []

            metric = Metric(
                name=name,
                value=value,
                metric_type=metric_type,
                timestamp=datetime.now(),
                labels=labels or {},
                help_text=help_text,
            )

            self.metrics[name].append(metric)
            self._cleanup_old_metrics(name)

    def increment_counter(self, name: str, labels: Dict[str, str] = None):
        """Increment a counter metric"""
        current = self.get_latest_value(name) or 0
        self.record_metric(name, current + 1, MetricType.COUNTER, labels)

    def set_gauge(self, name: str, value: Union[int, float], labels: Dict[str, str] = None):
        """Set a gauge metric value"""
        self.record_metric(name, value, MetricType.GAUGE, labels)

    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a histogram metric value"""
        self.record_metric(name, value, MetricType.HISTOGRAM, labels)

    def get_latest_value(self, name: str) -> Optional[Union[int, float]]:
        """Get the latest value for a metric"""
        with self._lock:
            if name in self.metrics and self.metrics[name]:
                return self.metrics[name][-1].value
            return None

    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get metrics summary for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        summary = {}

        with self._lock:
            for name, metric_list in self.metrics.items():
                recent_metrics = [m for m in metric_list if m.timestamp >= cutoff_time]
                if recent_metrics:
                    values = [m.value for m in recent_metrics]
                    summary[name] = {
                        "count": len(values),
                        "latest": values[-1],
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "type": recent_metrics[-1].metric_type.value,
                    }

        return summary

    def _cleanup_old_metrics(self, name: str):
        """Remove metrics older than retention period"""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        self.metrics[name] = [m for m in self.metrics[name] if m.timestamp >= cutoff_time]