"""
System monitoring for AUDITORIA360 - tracks system resources and performance
"""

import logging
from typing import Any, Dict

import psutil

from .metrics import MetricsCollector

logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitors system resources and performance metrics"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.enabled = True

    def collect_system_metrics(self):
        """Collect and record system metrics"""
        if not self.enabled:
            return

        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.metrics_collector.set_gauge("system_cpu_percent", cpu_percent)

            # Memory metrics
            memory = psutil.virtual_memory()
            self.metrics_collector.set_gauge("system_memory_percent", memory.percent)
            self.metrics_collector.set_gauge("system_memory_used_bytes", memory.used)
            self.metrics_collector.set_gauge(
                "system_memory_available_bytes", memory.available
            )

            # Disk metrics
            disk = psutil.disk_usage("/")
            self.metrics_collector.set_gauge("system_disk_percent", disk.percent)
            self.metrics_collector.set_gauge("system_disk_used_bytes", disk.used)
            self.metrics_collector.set_gauge("system_disk_free_bytes", disk.free)

            # Network metrics (if available)
            try:
                network = psutil.net_io_counters()
                self.metrics_collector.set_gauge(
                    "system_network_bytes_sent", network.bytes_sent
                )
                self.metrics_collector.set_gauge(
                    "system_network_bytes_recv", network.bytes_recv
                )
                self.metrics_collector.set_gauge(
                    "system_network_packets_sent", network.packets_sent
                )
                self.metrics_collector.set_gauge(
                    "system_network_packets_recv", network.packets_recv
                )
            except Exception as e:
                logger.debug(f"Network metrics not available: {e}")

            # Load average (Unix-like systems)
            try:
                load_avg = psutil.getloadavg()
                self.metrics_collector.set_gauge("system_load_1m", load_avg[0])
                self.metrics_collector.set_gauge("system_load_5m", load_avg[1])
                self.metrics_collector.set_gauge("system_load_15m", load_avg[2])
            except (AttributeError, OSError):
                logger.debug("Load average metrics not available on this platform")

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

    def get_system_info(self) -> Dict[str, Any]:
        """Get detailed system information"""
        try:
            return {
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_total": psutil.disk_usage("/").total,
                "disk_free": psutil.disk_usage("/").free,
                "boot_time": psutil.boot_time(),
                "process_count": len(psutil.pids()),
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}

    def enable(self):
        """Enable system monitoring"""
        self.enabled = True
        logger.info("System monitoring enabled")

    def disable(self):
        """Disable system monitoring"""
        self.enabled = False
        logger.info("System monitoring disabled")
