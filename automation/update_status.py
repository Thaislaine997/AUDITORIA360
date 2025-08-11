#!/usr/bin/env python3
"""
AUDITORIA360 - Automated System Status Monitoring
Health-Check Script for Module Status Tracking
"""

import requests
import time
from datetime import datetime
from typing import Dict, Any, List
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base configuration
BASE_URL = os.getenv("AUDITORIA360_BASE_URL", "http://localhost:8001")

# Module health check endpoints mapping
MODULES = {
    "Dashboard Estratégico": f"{BASE_URL}/dashboard",
    "Controle Mensal": f"{BASE_URL}/controle_mensal",
    "Disparo de Auditoria": f"{BASE_URL}/disparo_auditoria",
    "Análise Forense": f"{BASE_URL}/forense", 
    "Gestão de Regras": f"{BASE_URL}/regras",
    "Simulador de Impactos": f"{BASE_URL}/simulador",
    "Geração de Relatórios": f"{BASE_URL}/relatorios",
    "Integração com IA": f"{BASE_URL}/ia",
    "Login/Admin": f"{BASE_URL}/login_admin",
    "LOGOPERACOES/Auditoria de Sistema": f"{BASE_URL}/logoperacoes", 
    "Personificação/Suporte Supremo": f"{BASE_URL}/personificacao",
    "Login/Onboarding": f"{BASE_URL}/login_onboarding",
    "Logs e Auditoria": f"{BASE_URL}/logs_auditoria",
    "Onboarding Escritório": f"{BASE_URL}/onboarding_escritorio",
    "Gerenciamento de Usuários": f"{BASE_URL}/gerenciamento_usuarios",
}

# Status mapping
STATUS_MESSAGES = {
    200: "FUNCIONANDO",
    500: "ERRO",
    503: "EM MANUTENÇÃO", 
    404: "NÃO ENCONTRADO",
    "timeout": "TIMEOUT",
    "connection_error": "ERRO DE CONEXÃO"
}

def check_module_health(name: str, url: str) -> Dict[str, Any]:
    """Check health of a single module"""
    try:
        logger.info(f"Checking health for {name}...")
        response = requests.get(url, timeout=5)
        
        status_code = response.status_code
        response_data = {}
        
        try:
            response_data = response.json()
        except:
            pass
            
        if status_code == 200 and response_data.get("status") in ["ok", "healthy", "funcionando"]:
            status = "FUNCIONANDO"
        elif status_code == 200 and response_data.get("status") == "em_desenvolvimento":
            status = "EM DESENVOLVIMENTO"
        elif status_code == 200 and response_data.get("status") == "em_teste":
            status = "EM TESTE"
        else:
            status = STATUS_MESSAGES.get(status_code, "ERRO")
            
        return {
            "name": name,
            "status": status,
            "status_code": status_code,
            "response_time": response.elapsed.total_seconds(),
            "details": response_data.get("details", ""),
            "last_check": datetime.now().isoformat(),
            "url": url
        }
        
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout checking {name}")
        return {
            "name": name,
            "status": "TIMEOUT",
            "status_code": None,
            "response_time": None,
            "details": "Health check timeout after 5 seconds",
            "last_check": datetime.now().isoformat(),
            "url": url
        }
    except requests.exceptions.ConnectionError:
        logger.warning(f"Connection error checking {name}")
        return {
            "name": name,
            "status": "ERRO DE CONEXÃO",
            "status_code": None,
            "response_time": None,
            "details": "Unable to connect to service",
            "last_check": datetime.now().isoformat(),
            "url": url
        }
    except Exception as e:
        logger.error(f"Error checking {name}: {str(e)}")
        return {
            "name": name,
            "status": "ERRO",
            "status_code": None,
            "response_time": None,
            "details": f"Unexpected error: {str(e)}",
            "last_check": datetime.now().isoformat(),
            "url": url
        }

def generate_status_markdown(results: List[Dict[str, Any]]) -> str:
    """Generate markdown status report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    markdown = f"""# Status Operacional Automatizado – AUDITORIA360

**Última atualização**: {timestamp}

## Resumo Executivo

"""
    
    # Count statuses
    status_counts = {}
    for result in results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    total_modules = len(results)
    functioning = status_counts.get("FUNCIONANDO", 0)
    
    markdown += f"""- **Total de Módulos**: {total_modules}
- **Funcionando**: {functioning} ({functioning/total_modules*100:.1f}%)
- **Com Problemas**: {total_modules - functioning} ({(total_modules-functioning)/total_modules*100:.1f}%)

"""
    
    # Add status indicators
    for status, count in status_counts.items():
        if status == "FUNCIONANDO":
            emoji = "✅"
        elif status == "EM DESENVOLVIMENTO":
            emoji = "🚧"
        elif status == "EM TESTE":
            emoji = "🧪"
        else:
            emoji = "❌"
        markdown += f"- {emoji} **{status}**: {count} módulos\n"
    
    markdown += "\n## Status Detalhado por Módulo\n\n"
    markdown += "| Módulo | Status | Tempo Resposta | Detalhes | Última Verificação |\n"
    markdown += "|--------|--------|----------------|----------|--------------------|\n"
    
    for result in results:
        status = result["status"]
        if status == "FUNCIONANDO":
            status_emoji = "✅"
        elif status == "EM DESENVOLVIMENTO":
            status_emoji = "🚧"
        elif status == "EM TESTE":
            status_emoji = "🧪"
        else:
            status_emoji = "❌"
            
        response_time = f"{result['response_time']:.3f}s" if result['response_time'] else "N/A"
        details = result['details'] if result['details'] else "-"
        last_check = datetime.fromisoformat(result['last_check']).strftime("%H:%M:%S")
        
        markdown += f"| {result['name']} | {status_emoji} {status} | {response_time} | {details} | {last_check} |\n"
    
    # Add performance metrics
    markdown += "\n## Métricas de Performance\n\n"
    
    response_times = [r['response_time'] for r in results if r['response_time'] is not None]
    if response_times:
        avg_response = sum(response_times) / len(response_times)
        max_response = max(response_times)
        min_response = min(response_times)
        
        markdown += f"""- **Tempo de Resposta Médio**: {avg_response:.3f}s
- **Tempo de Resposta Máximo**: {max_response:.3f}s  
- **Tempo de Resposta Mínimo**: {min_response:.3f}s
"""
    else:
        markdown += "- **Métricas de Performance**: Não disponíveis\n"
    
    # Add system health summary
    markdown += "\n## Indicadores de Saúde do Sistema\n\n"
    
    if functioning/total_modules >= 0.9:
        health_status = "🟢 SISTEMA SAUDÁVEL"
    elif functioning/total_modules >= 0.7:
        health_status = "🟡 SISTEMA COM ATENÇÕES"
    else:
        health_status = "🔴 SISTEMA CRÍTICO"
        
    markdown += f"**Status Geral**: {health_status}\n\n"
    
    # Add recommendations
    problematic_modules = [r for r in results if r['status'] not in ['FUNCIONANDO', 'EM DESENVOLVIMENTO', 'EM TESTE']]
    
    if problematic_modules:
        markdown += "## ⚠️ Módulos que Requerem Atenção\n\n"
        for module in problematic_modules:
            markdown += f"- **{module['name']}**: {module['status']} - {module['details']}\n"
    
    markdown += f"""
---

## Automação e Monitoramento

- **Script de Monitoramento**: `automation/update_status.py`
- **Frequência de Atualização**: A cada 5 minutos (configurável)
- **Alertas Automáticos**: Habilitados para falhas críticas
- **Dashboard em Tempo Real**: Disponível em `/status-dashboard`

## Próximas Verificações

- **Próxima Verificação Automática**: {(datetime.now()).strftime("%Y-%m-%d %H:%M:%S UTC")}
- **Histórico Completo**: Disponível em `/api/health/history`

---

*Relatório gerado automaticamente pelo Sistema de Monitoramento AUDITORIA360*
"""

    return markdown

def generate_json_status(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate JSON status report"""
    
    status_counts = {}
    for result in results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    total_modules = len(results)
    functioning = status_counts.get("FUNCIONANDO", 0)
    
    response_times = [r['response_time'] for r in results if r['response_time'] is not None]
    avg_response_time = sum(response_times) / len(response_times) if response_times else None
    
    return {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_modules": total_modules,
            "functioning": functioning,
            "functioning_percentage": functioning/total_modules*100,
            "with_issues": total_modules - functioning,
            "status_distribution": status_counts,
            "average_response_time": avg_response_time
        },
        "modules": results,
        "system_health": {
            "status": "healthy" if functioning/total_modules >= 0.9 else "degraded" if functioning/total_modules >= 0.7 else "critical",
            "score": functioning/total_modules*100
        }
    }

def save_status_files(markdown: str, json_data: Dict[str, Any]):
    """Save status reports to files"""
    
    # Save markdown report
    markdown_path = "processos_status_auditoria360.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    logger.info(f"Status markdown saved to {markdown_path}")
    
    # Save JSON report  
    json_path = "status_report_auditoria360.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    logger.info(f"Status JSON saved to {json_path}")

def main():
    """Main function to run health checks and generate reports"""
    logger.info("Starting AUDITORIA360 health monitoring...")
    
    results = []
    
    for name, url in MODULES.items():
        result = check_module_health(name, url)
        results.append(result)
        time.sleep(0.1)  # Small delay between requests
    
    # Generate reports
    markdown_report = generate_status_markdown(results)
    json_report = generate_json_status(results)
    
    # Save to files
    save_status_files(markdown_report, json_report)
    
    # Print summary to console
    functioning = sum(1 for r in results if r['status'] == 'FUNCIONANDO')
    total = len(results)
    
    logger.info(f"Health check completed: {functioning}/{total} modules functioning ({functioning/total*100:.1f}%)")
    
    # Return status for potential CI/CD usage
    return 0 if functioning/total >= 0.8 else 1

if __name__ == "__main__":
    exit(main())