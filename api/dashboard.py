"""
FastAPI wrapper for Streamlit Dashboard integration
This allows Streamlit-like dashboards to run on Vercel
"""

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
from typing import Dict, Any, Optional
from src.auth.unified_auth import get_current_user_dependency

# Create FastAPI app for dashboard
dashboard_app = FastAPI(
    title="AUDITORIA360 Dashboard",
    description="Interactive Dashboard for AUDITORIA360 System",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="dashboards/templates")

# Mock dashboard data (replace with real data from your services)
def get_dashboard_data(user: Dict[str, Any]) -> Dict[str, Any]:
    """Get dashboard data for the current user"""
    return {
        "user": user,
        "stats": {
            "total_employees": 1250,
            "active_audits": 15,
            "pending_documents": 8,
            "compliance_score": 94.5
        },
        "recent_activities": [
            {"action": "Payroll processed", "timestamp": "2024-01-28 14:30", "status": "success"},
            {"action": "Audit completed", "timestamp": "2024-01-28 13:15", "status": "success"},
            {"action": "Document uploaded", "timestamp": "2024-01-28 12:45", "status": "pending"},
        ],
        "charts": {
            "compliance_trend": [85, 88, 91, 93, 94.5],
            "monthly_audits": [12, 15, 18, 20, 15],
            "document_status": {
                "approved": 45,
                "pending": 8,
                "rejected": 2
            }
        }
    }

@dashboard_app.get("/", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Main dashboard page"""
    dashboard_data = get_dashboard_data(current_user)
    
    # Simple HTML template (in production, use proper Jinja2 templates)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AUDITORIA360 Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .stat-card {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }}
            .chart-container {{ 
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body style="background-color: #f8f9fa;">
        <nav class="navbar navbar-dark bg-primary">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">AUDITORIA360 Dashboard</span>
                <span class="navbar-text">Bem-vindo, {current_user.get('name', 'Usuário')}</span>
            </div>
        </nav>
        
        <div class="container-fluid mt-4">
            <div class="row">
                <div class="col-md-3">
                    <div class="stat-card text-center">
                        <h3>{dashboard_data['stats']['total_employees']}</h3>
                        <p>Total de Funcionários</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card text-center">
                        <h3>{dashboard_data['stats']['active_audits']}</h3>
                        <p>Auditorias Ativas</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card text-center">
                        <h3>{dashboard_data['stats']['pending_documents']}</h3>
                        <p>Documentos Pendentes</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card text-center">
                        <h3>{dashboard_data['stats']['compliance_score']}%</h3>
                        <p>Score de Compliance</p>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-8">
                    <div class="chart-container">
                        <h5>Tendência de Compliance</h5>
                        <div id="compliance-chart"></div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="chart-container">
                        <h5>Atividades Recentes</h5>
                        <div class="list-group">
                            {''.join([f'<div class="list-group-item"><strong>{activity["action"]}</strong><br><small>{activity["timestamp"]} - {activity["status"]}</small></div>' for activity in dashboard_data['recent_activities']])}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="chart-container">
                        <h5>Auditorias Mensais</h5>
                        <div id="audits-chart"></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="chart-container">
                        <h5>Status dos Documentos</h5>
                        <div id="documents-chart"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Compliance trend chart
            Plotly.newPlot('compliance-chart', [{{
                x: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
                y: {dashboard_data['charts']['compliance_trend']},
                type: 'scatter',
                mode: 'lines+markers',
                marker: {{color: '#667eea'}},
                line: {{width: 3}}
            }}], {{
                title: '',
                xaxis: {{title: 'Mês'}},
                yaxis: {{title: 'Score (%)'}},
                showlegend: false
            }});
            
            // Monthly audits chart
            Plotly.newPlot('audits-chart', [{{
                x: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
                y: {dashboard_data['charts']['monthly_audits']},
                type: 'bar',
                marker: {{color: '#764ba2'}}
            }}], {{
                title: '',
                xaxis: {{title: 'Mês'}},
                yaxis: {{title: 'Quantidade'}},
                showlegend: false
            }});
            
            // Document status pie chart
            Plotly.newPlot('documents-chart', [{{
                values: [45, 8, 2],
                labels: ['Aprovados', 'Pendentes', 'Rejeitados'],
                type: 'pie',
                marker: {{
                    colors: ['#28a745', '#ffc107', '#dc3545']
                }}
            }}], {{
                title: '',
                showlegend: true
            }});
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@dashboard_app.get("/api/data")
async def get_dashboard_api_data(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """API endpoint for dashboard data"""
    return get_dashboard_data(current_user)

@dashboard_app.get("/api/stats")
async def get_stats(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get just the stats data"""
    data = get_dashboard_data(current_user)
    return data["stats"]

@dashboard_app.get("/api/activities")
async def get_recent_activities(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get recent activities"""
    data = get_dashboard_data(current_user)
    return data["recent_activities"]

@dashboard_app.get("/health")
async def dashboard_health():
    """Dashboard health check"""
    return {
        "status": "healthy",
        "service": "AUDITORIA360 Dashboard",
        "version": "1.0.0",
        "features": [
            "Real-time statistics",
            "Interactive charts",
            "Activity monitoring",
            "Compliance tracking"
        ]
    }

# Integration endpoint for main API
@dashboard_app.get("/embed")
async def embed_dashboard():
    """Embeddable dashboard widget"""
    html_content = """
    <div id="auditoria360-dashboard-widget" style="width: 100%; height: 400px;">
        <iframe src="/dashboard/" width="100%" height="100%" frameborder="0"></iframe>
    </div>
    """
    return HTMLResponse(content=html_content)

# Dashboard configuration for different user roles
@dashboard_app.get("/config")
async def get_dashboard_config(
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """Get dashboard configuration based on user role"""
    user_roles = current_user.get('roles', ['user'])
    
    config = {
        "widgets": ["stats", "activities"],
        "charts": ["compliance_trend"],
        "permissions": {
            "export_data": False,
            "manage_users": False,
            "view_reports": True
        }
    }
    
    if 'admin' in user_roles:
        config["widgets"].extend(["user_management", "system_logs"])
        config["charts"].extend(["monthly_audits", "document_status"])
        config["permissions"].update({
            "export_data": True,
            "manage_users": True,
            "view_reports": True
        })
    
    return config