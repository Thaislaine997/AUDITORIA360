#!/usr/bin/env python3
"""
AUDITORIA360 - Metrics Collector and SLA Monitor
Coleta métricas do sistema e monitora SLAs definidos
"""

import logging
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import statistics
import os

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
        self.sla_targets = {
            "uptime_percentage": 99.5,
            "response_time_95th": 2000,  # ms
            "ai_availability": 98.0,
            "error_rate": 1.0  # percentage
        }
    
    def calculate_uptime(self) -> float:
        """Calcular uptime percentage baseado nos health checks"""
        try:
            # Simulated uptime calculation - in production would query monitoring system
            # Based on successful health checks vs total checks in time period
            total_checks = 288  # 24 hours * 12 checks per hour (every 5 minutes)
            successful_checks = 285  # Simulated successful checks
            
            uptime = (successful_checks / total_checks) * 100
            return round(uptime, 2)
        except Exception as e:
            logger.error(f"Error calculating uptime: {e}")
            return 0.0
    
    def get_response_metrics(self) -> Dict[str, float]:
        """Obter métricas de tempo de resposta"""
        try:
            # Simulated response time collection - in production would query actual metrics
            response_times = [150, 200, 180, 220, 190, 250, 300, 175, 160, 210]  # ms
            
            return {
                "avg_response_time": round(statistics.mean(response_times), 2),
                "p50_response_time": round(statistics.median(response_times), 2),
                "p95_response_time": round(statistics.quantiles(response_times, n=20)[18], 2),  # 95th percentile
                "p99_response_time": round(max(response_times), 2),
                "min_response_time": round(min(response_times), 2),
                "max_response_time": round(max(response_times), 2)
            }
        except Exception as e:
            logger.error(f"Error getting response metrics: {e}")
            return {}
    
    def get_error_rates(self) -> Dict[str, float]:
        """Obter taxas de erro do sistema"""
        try:
            # Simulated error rate calculation
            total_requests = 10000
            error_requests = 45
            
            return {
                "total_requests": total_requests,
                "error_requests": error_requests,
                "error_rate_percentage": round((error_requests / total_requests) * 100, 3),
                "success_rate_percentage": round(((total_requests - error_requests) / total_requests) * 100, 3)
            }
        except Exception as e:
            logger.error(f"Error calculating error rates: {e}")
            return {}
    
    def check_ai_services(self) -> Dict[str, Any]:
        """Verificar disponibilidade dos serviços de IA"""
        try:
            # Simulated AI service availability check
            ai_services = {
                "openai_api": {"status": "healthy", "response_time": 450},
                "document_processing": {"status": "healthy", "response_time": 1200},
                "risk_analysis": {"status": "healthy", "response_time": 800},
                "report_generation": {"status": "degraded", "response_time": 3500}
            }
            
            healthy_services = len([s for s in ai_services.values() if s["status"] == "healthy"])
            total_services = len(ai_services)
            availability = (healthy_services / total_services) * 100
            
            return {
                "services": ai_services,
                "availability_percentage": round(availability, 2),
                "healthy_services": healthy_services,
                "total_services": total_services
            }
        except Exception as e:
            logger.error(f"Error checking AI services: {e}")
            return {}
    
    def get_user_metrics(self) -> Dict[str, int]:
        """Obter métricas de usuário e atividade"""
        try:
            # Simulated user activity metrics
            return {
                "active_users_24h": 156,
                "new_registrations_24h": 8,
                "audit_executions_24h": 45,
                "report_generations_24h": 23,
                "login_sessions_24h": 189,
                "concurrent_users": 23
            }
        except Exception as e:
            logger.error(f"Error getting user metrics: {e}")
            return {}
    
    def get_audit_volume(self) -> Dict[str, int]:
        """Obter volume de logs de auditoria"""
        try:
            # Simulated audit log volume
            return {
                "total_audit_logs_24h": 2847,
                "security_events_24h": 12,
                "admin_actions_24h": 34,
                "failed_logins_24h": 8,
                "data_access_logs_24h": 1423
            }
        except Exception as e:
            logger.error(f"Error getting audit volume: {e}")
            return {}
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Coletar todas as métricas do sistema"""
        logger.info("Collecting comprehensive system metrics...")
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "collection_duration": 0,
            "uptime": {},
            "performance": {},
            "errors": {},
            "ai_services": {},
            "user_activity": {},
            "audit_logs": {},
            "sla_compliance": {}
        }
        
        start_time = time.time()
        
        try:
            # Collect all metrics
            metrics["uptime"]["percentage"] = self.calculate_uptime()
            metrics["performance"] = self.get_response_metrics()
            metrics["errors"] = self.get_error_rates()
            metrics["ai_services"] = self.check_ai_services()
            metrics["user_activity"] = self.get_user_metrics()
            metrics["audit_logs"] = self.get_audit_volume()
            
            # Calculate SLA compliance
            metrics["sla_compliance"] = self.check_sla_compliance(metrics)
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
        finally:
            metrics["collection_duration"] = round(time.time() - start_time, 2)
        
        return metrics
    
    def check_sla_compliance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Verificar compliance com SLAs definidos"""
        compliance = {}
        
        try:
            # Uptime SLA
            uptime = metrics.get("uptime", {}).get("percentage", 0)
            compliance["uptime"] = {
                "target": self.sla_targets["uptime_percentage"],
                "actual": uptime,
                "compliant": uptime >= self.sla_targets["uptime_percentage"],
                "deviation": round(uptime - self.sla_targets["uptime_percentage"], 2)
            }
            
            # Response time SLA (95th percentile)
            p95_response = metrics.get("performance", {}).get("p95_response_time", 0)
            compliance["response_time"] = {
                "target": self.sla_targets["response_time_95th"],
                "actual": p95_response,
                "compliant": p95_response <= self.sla_targets["response_time_95th"],
                "deviation": round(p95_response - self.sla_targets["response_time_95th"], 2)
            }
            
            # AI availability SLA
            ai_availability = metrics.get("ai_services", {}).get("availability_percentage", 0)
            compliance["ai_availability"] = {
                "target": self.sla_targets["ai_availability"],
                "actual": ai_availability,
                "compliant": ai_availability >= self.sla_targets["ai_availability"],
                "deviation": round(ai_availability - self.sla_targets["ai_availability"], 2)
            }
            
            # Error rate SLA
            error_rate = metrics.get("errors", {}).get("error_rate_percentage", 0)
            compliance["error_rate"] = {
                "target": self.sla_targets["error_rate"],
                "actual": error_rate,
                "compliant": error_rate <= self.sla_targets["error_rate"],
                "deviation": round(error_rate - self.sla_targets["error_rate"], 2)
            }
            
            # Overall SLA compliance
            compliant_slas = len([sla for sla in compliance.values() if sla.get("compliant", False)])
            total_slas = len(compliance)
            compliance["overall"] = {
                "compliant_slas": compliant_slas,
                "total_slas": total_slas,
                "compliance_percentage": round((compliant_slas / total_slas) * 100, 1),
                "status": "compliant" if compliant_slas == total_slas else "breach"
            }
            
        except Exception as e:
            logger.error(f"Error checking SLA compliance: {e}")
        
        return compliance
    
    def generate_metrics_report(self, metrics: Dict[str, Any]) -> str:
        """Gerar relatório de métricas em markdown"""
        
        compliance = metrics.get("sla_compliance", {})
        overall_compliance = compliance.get("overall", {})
        
        # Status icons
        status_icon = "✅" if overall_compliance.get("status") == "compliant" else "⚠️"
        
        report = f"""# 📊 AUDITORIA360 - Relatório de Métricas e SLA

**Data/Hora:** {metrics['timestamp']}
**Status SLA:** {status_icon} {overall_compliance.get('status', 'unknown').upper()}
**Compliance Geral:** {overall_compliance.get('compliance_percentage', 0)}%

## 📈 Métricas de Performance

### Uptime e Disponibilidade
- **Uptime Atual:** {metrics.get('uptime', {}).get('percentage', 0)}%
- **Meta SLA:** {self.sla_targets['uptime_percentage']}%
- **Status:** {'✅ Compliant' if compliance.get('uptime', {}).get('compliant') else '❌ SLA Breach'}

### Tempo de Resposta
- **Tempo Médio:** {metrics.get('performance', {}).get('avg_response_time', 0)}ms
- **95th Percentil:** {metrics.get('performance', {}).get('p95_response_time', 0)}ms
- **Meta SLA:** {self.sla_targets['response_time_95th']}ms
- **Status:** {'✅ Compliant' if compliance.get('response_time', {}).get('compliant') else '❌ SLA Breach'}

### Taxa de Erro
- **Taxa de Erro:** {metrics.get('errors', {}).get('error_rate_percentage', 0)}%
- **Taxa de Sucesso:** {metrics.get('errors', {}).get('success_rate_percentage', 0)}%
- **Meta SLA:** ≤{self.sla_targets['error_rate']}%
- **Status:** {'✅ Compliant' if compliance.get('error_rate', {}).get('compliant') else '❌ SLA Breach'}

## 🤖 Serviços de IA

### Disponibilidade
- **Disponibilidade IA:** {metrics.get('ai_services', {}).get('availability_percentage', 0)}%
- **Serviços Ativos:** {metrics.get('ai_services', {}).get('healthy_services', 0)}/{metrics.get('ai_services', {}).get('total_services', 0)}
- **Meta SLA:** {self.sla_targets['ai_availability']}%
- **Status:** {'✅ Compliant' if compliance.get('ai_availability', {}).get('compliant') else '❌ SLA Breach'}

### Status dos Serviços
"""
        
        ai_services = metrics.get('ai_services', {}).get('services', {})
        for service_name, service_data in ai_services.items():
            status_emoji = "✅" if service_data.get('status') == 'healthy' else "⚠️" if service_data.get('status') == 'degraded' else "❌"
            report += f"- **{service_name}:** {status_emoji} {service_data.get('status', 'unknown')} ({service_data.get('response_time', 0)}ms)\n"
        
        report += f"""

## 👥 Atividade de Usuários (24h)

- **Usuários Ativos:** {metrics.get('user_activity', {}).get('active_users_24h', 0)}
- **Usuários Simultâneos:** {metrics.get('user_activity', {}).get('concurrent_users', 0)}
- **Novos Registros:** {metrics.get('user_activity', {}).get('new_registrations_24h', 0)}
- **Auditorias Executadas:** {metrics.get('user_activity', {}).get('audit_executions_24h', 0)}
- **Relatórios Gerados:** {metrics.get('user_activity', {}).get('report_generations_24h', 0)}
- **Sessões de Login:** {metrics.get('user_activity', {}).get('login_sessions_24h', 0)}

## 📋 Logs de Auditoria (24h)

- **Total de Logs:** {metrics.get('audit_logs', {}).get('total_audit_logs_24h', 0)}
- **Eventos de Segurança:** {metrics.get('audit_logs', {}).get('security_events_24h', 0)}
- **Ações Admin:** {metrics.get('audit_logs', {}).get('admin_actions_24h', 0)}
- **Logins Falhados:** {metrics.get('audit_logs', {}).get('failed_logins_24h', 0)}
- **Acessos a Dados:** {metrics.get('audit_logs', {}).get('data_access_logs_24h', 0)}

## 🎯 SLA Compliance Detalhado

| Métrica | Meta | Atual | Status | Desvio |
|---------|------|-------|--------|--------|
"""
        
        sla_metrics = ['uptime', 'response_time', 'ai_availability', 'error_rate']
        for metric in sla_metrics:
            if metric in compliance:
                sla = compliance[metric]
                status_emoji = "✅" if sla.get('compliant') else "❌"
                target = sla.get('target', 0)
                actual = sla.get('actual', 0)
                deviation = sla.get('deviation', 0)
                
                # Format based on metric type
                if metric == 'uptime' or metric == 'ai_availability':
                    target_str = f"{target}%"
                    actual_str = f"{actual}%"
                elif metric == 'response_time':
                    target_str = f"{target}ms"
                    actual_str = f"{actual}ms"
                else:  # error_rate
                    target_str = f"≤{target}%"
                    actual_str = f"{actual}%"
                
                report += f"| {metric.replace('_', ' ').title()} | {target_str} | {actual_str} | {status_emoji} | {deviation:+.2f} |\n"
        
        report += f"""

## 📊 Resumo Executivo

- **Status Geral:** {'🟢 Sistema Saudável' if overall_compliance.get('status') == 'compliant' else '🟡 Atenção Requerida'}
- **SLAs Atendidos:** {overall_compliance.get('compliant_slas', 0)}/{overall_compliance.get('total_slas', 0)}
- **Compliance Score:** {overall_compliance.get('compliance_percentage', 0)}%
- **Próxima Coleta:** {(datetime.now() + timedelta(minutes=5)).strftime('%H:%M:%S')}

## 🔍 Recomendações

"""
        
        # Generate recommendations based on SLA breaches
        recommendations = []
        for metric, sla in compliance.items():
            if metric != 'overall' and not sla.get('compliant', True):
                if metric == 'uptime':
                    recommendations.append("🚨 Investigar causas de downtime e implementar melhorias de infraestrutura")
                elif metric == 'response_time':
                    recommendations.append("⚡ Otimizar performance da aplicação e considerar scaling")
                elif metric == 'ai_availability':
                    recommendations.append("🤖 Verificar conectividade com serviços de IA e implementar fallbacks")
                elif metric == 'error_rate':
                    recommendations.append("🐛 Investigar causas de erros e implementar correções")
        
        if not recommendations:
            recommendations.append("✅ Todos os SLAs estão sendo atendidos - continuar monitoramento")
        
        for rec in recommendations:
            report += f"- {rec}\n"
        
        report += f"""

---

*Relatório gerado automaticamente pelo Sistema de Monitoramento AUDITORIA360*
*Tempo de coleta: {metrics.get('collection_duration', 0)}s*
"""
        
        return report

def main():
    """Função principal para coletar métricas"""
    logging.basicConfig(level=logging.INFO)
    
    collector = MetricsCollector()
    
    # Collect metrics
    metrics = collector.collect_system_metrics()
    
    # Generate reports
    report_markdown = collector.generate_metrics_report(metrics)
    
    # Save JSON report
    with open("system_metrics_report.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    # Save markdown report
    with open("system_metrics_report.md", "w", encoding="utf-8") as f:
        f.write(report_markdown)
    
    # Log summary
    overall_compliance = metrics.get('sla_compliance', {}).get('overall', {})
    logger.info(f"Metrics collection completed. SLA compliance: {overall_compliance.get('compliance_percentage', 0)}%")
    
    # Exit code based on SLA compliance
    return 0 if overall_compliance.get('status') == 'compliant' else 1

if __name__ == "__main__":
    exit(main())