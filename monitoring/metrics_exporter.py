#!/usr/bin/env python3
"""
AUDITORIA360 - Prometheus Metrics Exporter
Exports system health metrics for monitoring
"""

import json
import time
import os
from datetime import datetime
from prometheus_client import start_http_server, Gauge, Counter, Histogram
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
SYSTEM_HEALTH_SCORE = Gauge('auditoria360_system_health_score', 'Overall system health score percentage')
MODULE_STATUS = Gauge('auditoria360_module_status', 'Module status (1=ok, 0.5=development/test, 0=error)', ['module_name'])
MODULE_RESPONSE_TIME = Gauge('auditoria360_module_response_time_seconds', 'Module response time in seconds', ['module_name'])
TOTAL_MODULES = Gauge('auditoria360_total_modules', 'Total number of modules')
FUNCTIONING_MODULES = Gauge('auditoria360_functioning_modules', 'Number of functioning modules')
SYSTEM_UPTIME = Gauge('auditoria360_system_uptime_seconds', 'System uptime in seconds')
HEALTH_CHECK_DURATION = Histogram('auditoria360_health_check_duration_seconds', 'Time spent on health checks')
HEALTH_CHECK_ERRORS = Counter('auditoria360_health_check_errors_total', 'Total health check errors')

class AUDITORIA360MetricsExporter:
    """Prometheus metrics exporter for AUDITORIA360"""
    
    def __init__(self, status_file: str = 'status_report_auditoria360.json'):
        self.status_file = status_file
        self.start_time = time.time()
        
    def update_metrics(self):
        """Update Prometheus metrics from status file"""
        try:
            with HEALTH_CHECK_DURATION.time():
                # Load status data
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    status_data = json.load(f)
                
                # System-level metrics
                summary = status_data.get('summary', {})
                system_health = status_data.get('system_health', {})
                
                SYSTEM_HEALTH_SCORE.set(system_health.get('score', 0))
                TOTAL_MODULES.set(summary.get('total_modules', 0))
                FUNCTIONING_MODULES.set(summary.get('functioning', 0))
                SYSTEM_UPTIME.set(time.time() - self.start_time)
                
                # Module-level metrics
                modules = status_data.get('modules', [])
                for module in modules:
                    module_name = module.get('name', 'unknown')
                    status = module.get('status', '').upper()
                    response_time = module.get('response_time', 0)
                    
                    # Convert status to numeric value
                    if status == 'FUNCIONANDO':
                        status_value = 1.0
                    elif status in ['EM DESENVOLVIMENTO', 'EM TESTE']:
                        status_value = 0.5
                    else:
                        status_value = 0.0
                    
                    MODULE_STATUS.labels(module_name=module_name).set(status_value)
                    
                    if response_time:
                        MODULE_RESPONSE_TIME.labels(module_name=module_name).set(response_time)
                
                logger.info(f"Metrics updated successfully - {len(modules)} modules")
                
        except FileNotFoundError:
            logger.error(f"Status file {self.status_file} not found")
            HEALTH_CHECK_ERRORS.inc()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in status file: {str(e)}")
            HEALTH_CHECK_ERRORS.inc()
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            HEALTH_CHECK_ERRORS.inc()
    
    def run(self, port: int = 8000, interval: int = 30):
        """Run the metrics exporter"""
        logger.info(f"Starting AUDITORIA360 metrics exporter on port {port}")
        
        # Start HTTP server
        start_http_server(port)
        
        logger.info(f"Metrics server started, updating every {interval} seconds")
        
        while True:
            self.update_metrics()
            time.sleep(interval)

def main():
    """Main function"""
    status_file = os.getenv('AUDITORIA360_STATUS_FILE', 'status_report_auditoria360.json')
    port = int(os.getenv('EXPORTER_PORT', '8000'))
    interval = int(os.getenv('UPDATE_INTERVAL', '30'))
    
    exporter = AUDITORIA360MetricsExporter(status_file)
    
    try:
        exporter.run(port=port, interval=interval)
    except KeyboardInterrupt:
        logger.info("Metrics exporter stopped")
    except Exception as e:
        logger.error(f"Metrics exporter error: {str(e)}")

if __name__ == "__main__":
    main()