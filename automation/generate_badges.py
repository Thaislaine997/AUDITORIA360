#!/usr/bin/env python3
"""
AUDITORIA360 - Badge Generator
Generates status badges for README and dashboards
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
import requests

def generate_badges(status_file: str = "status_report_auditoria360.json") -> Dict[str, str]:
    """Generate various status badges based on system health"""
    
    badges = {}
    
    try:
        with open(status_file, 'r') as f:
            status_data = json.load(f)
    except FileNotFoundError:
        # Default badges when no status available
        return {
            "system_status": "![System Status](https://img.shields.io/badge/system-unknown-lightgrey)",
            "health_percentage": "![Health](https://img.shields.io/badge/health-unknown-lightgrey)",
            "modules_count": "![Modules](https://img.shields.io/badge/modules-unknown-lightgrey)",
            "last_check": "![Last Check](https://img.shields.io/badge/last%20check-unknown-lightgrey)"
        }
    
    # System status badge
    system_health = status_data.get("system_health", {})
    health_status = system_health.get("status", "unknown")
    
    if health_status == "healthy":
        status_color = "brightgreen"
        status_text = "healthy"
    elif health_status == "degraded":
        status_color = "yellow"
        status_text = "degraded"
    elif health_status == "critical":
        status_color = "red"
        status_text = "critical"
    else:
        status_color = "lightgrey"
        status_text = "unknown"
    
    badges["system_status"] = f"![System Status](https://img.shields.io/badge/system-{status_text}-{status_color})"
    
    # Health percentage badge
    health_score = system_health.get("score", 0)
    health_color = "brightgreen" if health_score >= 90 else "yellow" if health_score >= 70 else "red"
    badges["health_percentage"] = f"![Health](https://img.shields.io/badge/health-{health_score:.0f}%25-{health_color})"
    
    # Modules count badge
    summary = status_data.get("summary", {})
    total_modules = summary.get("total_modules", 0)
    healthy_total = summary.get("healthy_total", 0)
    badges["modules_count"] = f"![Modules](https://img.shields.io/badge/modules-{healthy_total}%2F{total_modules}-blue)"
    
    # Last check badge
    timestamp = status_data.get("timestamp", "")
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            time_str = dt.strftime("%Y--%m--%d")
            badges["last_check"] = f"![Last Check](https://img.shields.io/badge/last%20check-{time_str}-lightblue)"
        except:
            badges["last_check"] = "![Last Check](https://img.shields.io/badge/last%20check-unknown-lightgrey)"
    else:
        badges["last_check"] = "![Last Check](https://img.shields.io/badge/last%20check-unknown-lightgrey)"
    
    # Response time badge
    avg_response_time = summary.get("average_response_time")
    if avg_response_time is not None:
        if avg_response_time < 0.1:
            time_color = "brightgreen"
        elif avg_response_time < 0.5:
            time_color = "yellow"
        else:
            time_color = "red"
        
        time_ms = int(avg_response_time * 1000)
        badges["response_time"] = f"![Response Time](https://img.shields.io/badge/response%20time-{time_ms}ms-{time_color})"
    else:
        badges["response_time"] = "![Response Time](https://img.shields.io/badge/response%20time-unknown-lightgrey)"
    
    return badges

def generate_status_page_html(status_file: str = "status_report_auditoria360.json") -> str:
    """Generate a simple HTML status page"""
    
    try:
        with open(status_file, 'r') as f:
            status_data = json.load(f)
    except FileNotFoundError:
        status_data = {}
    
    badges = generate_badges(status_file)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AUDITORIA360 - Status do Sistema</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        .badges {{
            padding: 30px;
            text-align: center;
            background: #f8f9fa;
            border-bottom: 1px solid #eee;
        }}
        .badge {{
            margin: 5px;
            display: inline-block;
        }}
        .content {{
            padding: 40px;
        }}
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .status-card {{
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 20px;
            border-radius: 8px;
        }}
        .status-card.healthy {{ border-left-color: #28a745; }}
        .status-card.degraded {{ border-left-color: #ffc107; }}
        .status-card.critical {{ border-left-color: #dc3545; }}
        .status-card h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .status-card .value {{
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
        }}
        .status-card.healthy .value {{ color: #28a745; }}
        .status-card.degraded .value {{ color: #ffc107; }}
        .status-card.critical .value {{ color: #dc3545; }}
        .modules-list {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }}
        .module-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .module-item:last-child {{ border-bottom: none; }}
        .module-status {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .status-funcionando {{ background: #d4edda; color: #155724; }}
        .status-em-teste {{ background: #cce7ff; color: #004085; }}
        .status-em-desenvolvimento {{ background: #fff3cd; color: #856404; }}
        .status-erro {{ background: #f8d7da; color: #721c24; }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #6c757d;
            border-top: 1px solid #eee;
            font-size: 0.9rem;
        }}
        .refresh-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            margin: 20px 0;
        }}
        .refresh-btn:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AUDITORIA360</h1>
            <p>Status Operacional do Sistema</p>
        </div>
        
        <div class="badges">
            <div class="badge">{badges.get('system_status', '')}</div>
            <div class="badge">{badges.get('health_percentage', '')}</div>
            <div class="badge">{badges.get('modules_count', '')}</div>
            <div class="badge">{badges.get('response_time', '')}</div>
            <div class="badge">{badges.get('last_check', '')}</div>
        </div>
        
        <div class="content">
            <button class="refresh-btn" onclick="location.reload()">🔄 Atualizar Status</button>
            
            <div class="status-grid">"""
    
    # Add status cards
    summary = status_data.get("summary", {})
    system_health = status_data.get("system_health", {})
    
    health_class = system_health.get("status", "unknown").replace("healthy", "healthy").replace("degraded", "degraded").replace("critical", "critical")
    
    html += f"""
                <div class="status-card {health_class}">
                    <h3>Status Geral</h3>
                    <div class="value">{system_health.get("status", "unknown").upper()}</div>
                </div>
                
                <div class="status-card">
                    <h3>Saúde do Sistema</h3>
                    <div class="value">{system_health.get("score", 0):.1f}%</div>
                </div>
                
                <div class="status-card">
                    <h3>Módulos Funcionando</h3>
                    <div class="value">{summary.get("healthy_total", 0)}/{summary.get("total_modules", 0)}</div>
                </div>
                
                <div class="status-card">
                    <h3>Tempo Resposta Médio</h3>
                    <div class="value">{int(summary.get("average_response_time", 0) * 1000)}ms</div>
                </div>
            </div>
            
            <div class="modules-list">
                <h3>Status dos Módulos</h3>"""
    
    # Add modules
    for module in status_data.get("modules", []):
        status = module.get("status", "unknown").lower().replace(" ", "-")
        status_class = f"status-{status}" if status in ["funcionando", "em-teste", "em-desenvolvimento"] else "status-erro"
        
        html += f"""
                <div class="module-item">
                    <div>
                        <strong>{module.get("name", "Unknown")}</strong><br>
                        <small>{module.get("details", "")}</small>
                    </div>
                    <span class="module-status {status_class}">{module.get("status", "UNKNOWN")}</span>
                </div>"""
    
    html += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>Última atualização: {status_data.get("timestamp", "Desconhecido")}</p>
            <p>Sistema de Monitoramento AUDITORIA360 | Gerado automaticamente</p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => location.reload(), 300000);
    </script>
</body>
</html>"""
    
    return html

def update_readme_badges(readme_path: str = "README.md"):
    """Update README.md with current status badges"""
    
    badges = generate_badges()
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"README file not found: {readme_path}")
        return
    
    # Badge section markers
    start_marker = "<!-- STATUS BADGES START -->"
    end_marker = "<!-- STATUS BADGES END -->"
    
    badge_section = f"""<!-- STATUS BADGES START -->
## 📊 Status do Sistema

{badges['system_status']} {badges['health_percentage']} {badges['modules_count']} {badges['response_time']} {badges['last_check']}

- **Sistema:** Status geral da plataforma
- **Saúde:** Percentual de módulos operacionais
- **Módulos:** Quantidade de módulos funcionando
- **Resposta:** Tempo médio de resposta das APIs
- **Verificação:** Última verificação de saúde

> 📈 [Dashboard de Status em Tempo Real](./status-dashboard.html) | 📋 [Relatório Detalhado](./processos_status_auditoria360.md)

<!-- STATUS BADGES END -->"""
    
    if start_marker in content and end_marker in content:
        # Replace existing badge section
        start_index = content.find(start_marker)
        end_index = content.find(end_marker) + len(end_marker)
        new_content = content[:start_index] + badge_section + content[end_index:]
    else:
        # Add badge section after title if markers don't exist
        lines = content.split('\n')
        insert_index = 1  # After first line (title)
        lines.insert(insert_index, badge_section)
        new_content = '\n'.join(lines)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated README.md with status badges")

def main():
    """Main function"""
    print("🎯 AUDITORIA360 Badge Generator")
    print("=" * 40)
    
    # Generate badges
    badges = generate_badges()
    print("✅ Generated status badges")
    
    # Generate status page HTML
    html_content = generate_status_page_html()
    with open("status-dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ Generated status-dashboard.html")
    
    # Update README
    if os.path.exists("README.md"):
        update_readme_badges()
    else:
        print("⚠️  README.md not found, skipping badge update")
    
    # Output badges for CI/CD use
    print("\n📋 Generated Badges:")
    for name, badge in badges.items():
        print(f"  {name}: {badge}")
    
    # Save badges to file for CI/CD
    with open("status_badges.json", "w") as f:
        json.dump(badges, f, indent=2)
    print("✅ Saved badges to status_badges.json")

if __name__ == "__main__":
    main()