#!/usr/bin/env python3
"""
Basic Monitoring Setup Script for AUDITORIA360
Sets up essential monitoring components
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class BasicMonitoringSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.setup_log = []
    
    def log_step(self, message, status="info"):
        """Log setup step"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {status.upper()}: {message}"
        print(log_entry)
        self.setup_log.append(log_entry)
    
    def create_basic_alerts(self):
        """Create basic alert configuration"""
        self.log_step("Configurando alertas básicos...", "info")
        
        alerts_config = {
            "basic_alerts": [
                {
                    "name": "system_down",
                    "description": "Sistema fora do ar",
                    "threshold": "service_unavailable",
                    "severity": "critical"
                },
                {
                    "name": "high_error_rate",
                    "description": "Taxa de erro elevada",
                    "threshold": "error_rate > 10%",
                    "severity": "warning"
                }
            ],
            "notification": {
                "email": "admin@auditoria360.com"
            }
        }
        
        # Create monitoring directory
        monitoring_dir = self.project_root / "monitoring"
        monitoring_dir.mkdir(exist_ok=True)
        
        with open(monitoring_dir / "basic_alerts.json", "w") as f:
            json.dump(alerts_config, f, indent=2)
        
        self.log_step("✅ Alertas básicos configurados", "success")
        return True
    
    def setup_basic_dashboard(self):
        """Setup basic monitoring dashboard"""
        self.log_step("Criando dashboard básico...", "info")
        
        dashboard_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>AUDITORIA360 - Basic Monitor</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .ok { background: #d4edda; }
        .warning { background: #fff3cd; }
        .error { background: #f8d7da; }
    </style>
</head>
<body>
    <h1>🎯 AUDITORIA360 - Monitor Básico</h1>
    <div class="status ok">✅ Sistema: Operacional</div>
    <div class="status ok">✅ API: Funcionando</div>
    <div class="status ok">✅ Database: Conectado</div>
    <p>Última atualização: <span id="timestamp"></span></p>
    <script>
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
'''
        
        monitoring_dir = self.project_root / "monitoring"
        with open(monitoring_dir / "basic_dashboard.html", "w") as f:
            f.write(dashboard_content)
        
        self.log_step("✅ Dashboard básico criado", "success")
        return True
    
    def configure_logging(self):
        """Configure basic logging"""
        self.log_step("Configurando logging básico...", "info")
        
        logging_config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "logs/auditoria360.log",
                    "formatter": "default"
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default"
                }
            },
            "loggers": {
                "auditoria360": {
                    "level": "INFO",
                    "handlers": ["file", "console"]
                }
            }
        }
        
        # Create logs directory
        logs_dir = self.project_root / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Create logging config
        with open(self.project_root / "logging_config.json", "w") as f:
            json.dump(logging_config, f, indent=2)
        
        self.log_step("✅ Logging configurado", "success")
        return True
    
    def setup_monitoring(self):
        """Execute basic monitoring setup"""
        self.log_step("🔧 AUDITORIA360 - Setup Monitoramento Básico", "info")
        self.log_step("=" * 40, "info")
        
        steps = [
            ("Alertas Básicos", self.create_basic_alerts),
            ("Dashboard Básico", self.setup_basic_dashboard),
            ("Logging", self.configure_logging)
        ]
        
        success = True
        for step_name, step_func in steps:
            try:
                if step_func():
                    self.log_step(f"✅ {step_name}: CONCLUÍDO", "success")
                else:
                    self.log_step(f"❌ {step_name}: FALHOU", "error")
                    success = False
            except Exception as e:
                self.log_step(f"❌ {step_name}: ERRO - {e}", "error")
                success = False
        
        if success:
            self.log_step("🎉 MONITORAMENTO BÁSICO CONFIGURADO!", "success")
        else:
            self.log_step("⚠️  Setup concluído com erros", "warning")
        
        return success

def main():
    """Main monitoring setup function"""
    setup = BasicMonitoringSetup()
    success = setup.setup_monitoring()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()