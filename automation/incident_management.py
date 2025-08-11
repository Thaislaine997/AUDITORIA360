#!/usr/bin/env python3
"""
AUDITORIA360 - Incident Management System
Sistema automatizado de gestão de incidentes
"""

import logging
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import os
import uuid

logger = logging.getLogger(__name__)

class IncidentManager:
    def __init__(self):
        self.incidents_file = "incidents_log.json"
        self.raci_matrix = {
            "Dashboard Estratégico": {"responsible": "Frontend", "approver": "PO", "consulted": "Suporte", "informed": "Admin"},
            "Disparo de Auditoria": {"responsible": "DevOps", "approver": "CTO", "consulted": "Suporte", "informed": "Clientes"},
            "Integração com IA": {"responsible": "Data Eng", "approver": "CTO", "consulted": "DevOps", "informed": "Clientes"},
            "Análise Forense": {"responsible": "Backend", "approver": "CTO", "consulted": "Frontend", "informed": "Suporte"},
            "Gestão de Regras": {"responsible": "Backend", "approver": "Jurídico", "consulted": "DevOps", "informed": "Clientes"},
            "Simulador de Impactos": {"responsible": "Data Eng", "approver": "CTO", "consulted": "Backend", "informed": "Clientes"},
            "LOGOPERACOES": {"responsible": "DevOps", "approver": "CISO", "consulted": "Backend", "informed": "Admin"},
            "Personificação": {"responsible": "DevOps", "approver": "CISO", "consulted": "Suporte", "informed": "Admin"},
            "Gerenciamento de Usuários": {"responsible": "Backend", "approver": "CISO", "consulted": "Frontend", "informed": "Admin"}
        }
    
    def get_module_responsible(self, module_name: str) -> Dict[str, str]:
        """Obter responsáveis pelo módulo baseado na matriz RACI"""
        return self.raci_matrix.get(module_name, {
            "responsible": "DevOps", 
            "approver": "CTO", 
            "consulted": "Suporte", 
            "informed": "Admin"
        })
    
    def determine_severity(self, module_name: str, error_details: str, status: str) -> str:
        """Determinar severidade do incidente"""
        critical_modules = ["Disparo de Auditoria", "Integração com IA", "LOGOPERACOES"]
        critical_keywords = ["database", "connection", "timeout", "authentication", "security"]
        
        if module_name in critical_modules:
            return "critical"
        
        if status in ["error", "critical", "down"]:
            return "high"
        
        if any(keyword in error_details.lower() for keyword in critical_keywords):
            return "high"
        
        if status in ["degraded", "warning"]:
            return "medium"
        
        return "low"
    
    def create_incident_from_failure(self, module_name: str, error_details: str, status: str = "error") -> Dict[str, Any]:
        """Criar incidente a partir de falha do sistema"""
        incident_id = str(uuid.uuid4())[:8]
        severity = self.determine_severity(module_name, error_details, status)
        responsible_team = self.get_module_responsible(module_name)
        
        incident = {
            "id": incident_id,
            "title": f"Falha em {module_name}",
            "description": error_details,
            "module": module_name,
            "severity": severity,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "responsible_team": responsible_team,
            "assigned_to": responsible_team.get("responsible", "DevOps"),
            "approver": responsible_team.get("approver", "CTO"),
            "stakeholders": [
                responsible_team.get("consulted", ""),
                responsible_team.get("informed", "")
            ],
            "priority": self._calculate_priority(severity, module_name),
            "estimated_resolution": self._estimate_resolution_time(severity),
            "actions_taken": [],
            "resolution": None,
            "resolved_at": None,
            "tags": ["automated", "system-failure", module_name.lower().replace(" ", "-")]
        }
        
        # Save incident
        self._save_incident(incident)
        
        # Create notifications
        self._send_incident_notifications(incident)
        
        # Create GitHub issue if configured
        self._create_github_issue(incident)
        
        logger.info(f"Created incident {incident_id} for {module_name} with severity {severity}")
        
        return incident
    
    def _calculate_priority(self, severity: str, module_name: str) -> str:
        """Calcular prioridade baseado na severidade e importância do módulo"""
        critical_modules = ["Disparo de Auditoria", "Integração com IA", "LOGOPERACOES"]
        
        if severity == "critical":
            return "P0" if module_name in critical_modules else "P1"
        elif severity == "high":
            return "P1" if module_name in critical_modules else "P2"
        elif severity == "medium":
            return "P2"
        else:
            return "P3"
    
    def _estimate_resolution_time(self, severity: str) -> str:
        """Estimar tempo de resolução baseado na severidade"""
        resolution_times = {
            "critical": "2 horas",
            "high": "4 horas",
            "medium": "24 horas",
            "low": "72 horas"
        }
        return resolution_times.get(severity, "72 horas")
    
    def _save_incident(self, incident: Dict[str, Any]):
        """Salvar incidente no arquivo de log"""
        try:
            # Load existing incidents
            incidents = []
            if os.path.exists(self.incidents_file):
                with open(self.incidents_file, "r", encoding="utf-8") as f:
                    incidents = json.load(f)
            
            # Add new incident
            incidents.append(incident)
            
            # Save back
            with open(self.incidents_file, "w", encoding="utf-8") as f:
                json.dump(incidents, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving incident: {e}")
    
    def _send_incident_notifications(self, incident: Dict[str, Any]):
        """Enviar notificações do incidente"""
        try:
            # Load alert template
            template_path = "templates/alert_template.md"
            if not os.path.exists(template_path):
                logger.warning("Alert template not found")
                return
            
            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()
            
            # Replace template variables
            alert_content = template.replace("{{alert_type}}", f"Incidente #{incident['id']}")
            alert_content = alert_content.replace("{{module_name}}", incident['module'])
            alert_content = alert_content.replace("{{status}}", incident['status'])
            alert_content = alert_content.replace("{{severity}}", incident['severity'])
            alert_content = alert_content.replace("{{timestamp}}", incident['created_at'])
            alert_content = alert_content.replace("{{details}}", incident['description'])
            alert_content = alert_content.replace("{{action_required}}", f"Resolver incidente de prioridade {incident['priority']}")
            alert_content = alert_content.replace("{{dashboard_url}}", "https://auditoria360.com/dashboard")
            alert_content = alert_content.replace("{{generation_time}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Save alert
            alert_filename = f"incident_alert_{incident['id']}.md"
            with open(alert_filename, "w", encoding="utf-8") as f:
                f.write(alert_content)
            
            logger.info(f"Created incident alert: {alert_filename}")
            
            # Here you would send actual notifications (Slack, Teams, Email)
            # Example webhook call:
            # self._send_slack_notification(incident, alert_content)
            # self._send_email_notification(incident, alert_content)
            
        except Exception as e:
            logger.error(f"Error sending notifications: {e}")
    
    def _create_github_issue(self, incident: Dict[str, Any]):
        """Criar issue automática no GitHub"""
        try:
            # GitHub API configuration (would come from environment variables)
            github_token = os.getenv("GITHUB_TOKEN")
            github_repo = os.getenv("GITHUB_REPO", "Thaislaine997/AUDITORIA360")
            
            if not github_token:
                logger.info("GitHub token not configured, skipping issue creation")
                return
            
            # Issue content
            issue_title = f"🚨 Incidente #{incident['id']}: {incident['title']}"
            issue_body = f"""## 📋 Detalhes do Incidente

- **ID:** {incident['id']}
- **Módulo:** {incident['module']}
- **Severidade:** {incident['severity']}
- **Prioridade:** {incident['priority']}
- **Criado em:** {incident['created_at']}
- **Responsável:** {incident['assigned_to']}
- **Aprovador:** {incident['approver']}

## 🔍 Descrição

{incident['description']}

## ⏱️ SLA de Resolução

**Tempo Estimado:** {incident['estimated_resolution']}

## 👥 Equipe Responsável (RACI)

- **Responsible:** {incident['responsible_team'].get('responsible', 'N/A')}
- **Approver:** {incident['responsible_team'].get('approver', 'N/A')}
- **Consulted:** {incident['responsible_team'].get('consulted', 'N/A')}
- **Informed:** {incident['responsible_team'].get('informed', 'N/A')}

## 🏷️ Labels

- incident
- {incident['severity']}-severity
- {incident['priority'].lower()}
- {incident['module'].lower().replace(' ', '-')}

---

*Issue criada automaticamente pelo Sistema de Gestão de Incidentes AUDITORIA360*
"""
            
            # API call to create GitHub issue
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            issue_data = {
                "title": issue_title,
                "body": issue_body,
                "labels": [
                    "incident",
                    f"{incident['severity']}-severity",
                    incident['priority'].lower(),
                    incident['module'].lower().replace(' ', '-').replace('/', '-')
                ]
            }
            
            # Simulate GitHub API call (commented out for demo)
            # response = requests.post(
            #     f"https://api.github.com/repos/{github_repo}/issues",
            #     headers=headers,
            #     json=issue_data
            # )
            
            logger.info(f"GitHub issue would be created for incident {incident['id']}")
            
        except Exception as e:
            logger.error(f"Error creating GitHub issue: {e}")
    
    def resolve_incident(self, incident_id: str, resolution: str) -> bool:
        """Marcar incidente como resolvido"""
        try:
            if not os.path.exists(self.incidents_file):
                return False
            
            with open(self.incidents_file, "r", encoding="utf-8") as f:
                incidents = json.load(f)
            
            # Find and update incident
            for incident in incidents:
                if incident['id'] == incident_id:
                    incident['status'] = 'resolved'
                    incident['resolved_at'] = datetime.now().isoformat()
                    incident['resolution'] = resolution
                    incident['updated_at'] = datetime.now().isoformat()
                    
                    # Save back
                    with open(self.incidents_file, "w", encoding="utf-8") as f:
                        json.dump(incidents, f, indent=2, ensure_ascii=False)
                    
                    logger.info(f"Resolved incident {incident_id}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error resolving incident: {e}")
            return False
    
    def get_open_incidents(self) -> List[Dict[str, Any]]:
        """Obter lista de incidentes em aberto"""
        try:
            if not os.path.exists(self.incidents_file):
                return []
            
            with open(self.incidents_file, "r", encoding="utf-8") as f:
                incidents = json.load(f)
            
            return [i for i in incidents if i.get('status') == 'open']
            
        except Exception as e:
            logger.error(f"Error getting open incidents: {e}")
            return []
    
    def generate_incident_report(self) -> str:
        """Gerar relatório de incidentes"""
        try:
            if not os.path.exists(self.incidents_file):
                return "Nenhum incidente registrado."
            
            with open(self.incidents_file, "r", encoding="utf-8") as f:
                incidents = json.load(f)
            
            open_incidents = [i for i in incidents if i.get('status') == 'open']
            resolved_incidents = [i for i in incidents if i.get('status') == 'resolved']
            
            # Count by severity
            severity_counts = {}
            for incident in open_incidents:
                severity = incident.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            report = f"""# 📊 AUDITORIA360 - Relatório de Incidentes

**Gerado em:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📈 Resumo Executivo

- **Total de Incidentes:** {len(incidents)}
- **Incidentes Abertos:** {len(open_incidents)}
- **Incidentes Resolvidos:** {len(resolved_incidents)}

### Distribuição por Severidade (Abertos)

"""
            
            for severity, count in severity_counts.items():
                emoji = {"critical": "🚨", "high": "⚠️", "medium": "🔶", "low": "🔵"}.get(severity, "❓")
                report += f"- {emoji} **{severity.title()}:** {count}\n"
            
            report += "\n## 🔥 Incidentes Críticos Abertos\n\n"
            
            critical_open = [i for i in open_incidents if i.get('severity') == 'critical']
            if critical_open:
                for incident in critical_open:
                    report += f"### 🚨 #{incident['id']} - {incident['title']}\n"
                    report += f"- **Módulo:** {incident['module']}\n"
                    report += f"- **Prioridade:** {incident['priority']}\n"
                    report += f"- **Responsável:** {incident['assigned_to']}\n"
                    report += f"- **Criado:** {incident['created_at']}\n\n"
            else:
                report += "✅ Nenhum incidente crítico aberto\n\n"
            
            report += """
## 📋 Todos os Incidentes Abertos

| ID | Módulo | Severidade | Prioridade | Responsável | Criado |
|----|--------|------------|------------|-------------|--------|
"""
            
            for incident in open_incidents:
                report += f"| {incident['id']} | {incident['module']} | {incident['severity']} | {incident['priority']} | {incident['assigned_to']} | {incident['created_at'][:10]} |\n"
            
            if not open_incidents:
                report += "| - | - | - | - | - | - |\n*Nenhum incidente aberto*\n"
            
            report += """

---

*Relatório gerado automaticamente pelo Sistema de Gestão de Incidentes AUDITORIA360*
"""
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating incident report: {e}")
            return "Erro ao gerar relatório de incidentes."

def main():
    """Função principal para demonstrar o sistema de incidentes"""
    logging.basicConfig(level=logging.INFO)
    
    incident_manager = IncidentManager()
    
    # Example: Create a test incident
    incident = incident_manager.create_incident_from_failure(
        "Integração com IA", 
        "Timeout ao conectar com OpenAI API - possível problema de rede",
        "error"
    )
    
    print(f"Created test incident: {incident['id']}")
    
    # Generate report
    report = incident_manager.generate_incident_report()
    
    # Save report
    with open("incident_management_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("Incident management report generated: incident_management_report.md")

if __name__ == "__main__":
    main()