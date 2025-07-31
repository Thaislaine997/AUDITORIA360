"""
AI-Powered Client Management API Router for AUDITORIA360
Implements churn detection, compliance anomalies, and intelligent suggestions
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
import json

from ...models.database import get_db
from ...models.client_models import (
    Client,
    ClientConfiguration, 
    ConfigurationTemplate,
    ChurnRiskAnalysis,
    ComplianceAnomaly,
    SimulationSession,
    AIInsight
)
from ...models.auth_models import User
from ...auth.auth_utils import get_current_user
from ..common.responses import success_response, error_response

router = APIRouter(prefix="/ai-clients", tags=["ai-clients"])


@router.get("/")
async def get_clients_with_ai_insights(
    skip: int = 0,
    limit: int = 100,
    include_risk_analysis: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get clients with AI-powered insights"""
    try:
        clients_query = db.query(Client).filter(
            Client.created_by_user_id == current_user.id
        ).offset(skip).limit(limit)
        
        clients = []
        for client in clients_query.all():
            client_data = {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "document_number": client.document_number,
                "business_segment": client.business_segment,
                "tax_regime": client.tax_regime,
                "annual_revenue": client.annual_revenue,
                "status": client.status,
                "churn_risk_score": client.churn_risk_score,
                "churn_risk_level": client.churn_risk_level,
                "last_interaction": client.last_interaction,
                "total_configurations": client.total_configurations,
                "failed_sends_count": client.failed_sends_count,
                "successful_sends_count": client.successful_sends_count,
                "created_at": client.created_at,
            }
            
            if include_risk_analysis:
                # Get latest risk analysis
                latest_analysis = db.query(ChurnRiskAnalysis).filter(
                    ChurnRiskAnalysis.client_id == client.id
                ).order_by(desc(ChurnRiskAnalysis.analysis_date)).first()
                
                client_data["latest_risk_analysis"] = {
                    "risk_score": latest_analysis.risk_score,
                    "risk_level": latest_analysis.risk_level,
                    "confidence_score": latest_analysis.confidence_score,
                    "risk_factors": latest_analysis.risk_factors,
                    "recommendations": latest_analysis.recommendations,
                    "analysis_date": latest_analysis.analysis_date,
                } if latest_analysis else None
                
                # Get unresolved anomalies
                anomalies = db.query(ComplianceAnomaly).filter(
                    ComplianceAnomaly.client_id == client.id,
                    ComplianceAnomaly.is_resolved == False
                ).all()
                
                client_data["active_anomalies"] = [
                    {
                        "id": anomaly.id,
                        "anomaly_type": anomaly.anomaly_type,
                        "severity": anomaly.severity,
                        "description": anomaly.description,
                        "detected_at": anomaly.detected_at,
                    }
                    for anomaly in anomalies
                ]
            
            clients.append(client_data)
        
        return success_response(clients)
        
    except Exception as e:
        return error_response(f"Failed to get clients: {str(e)}", 500)


@router.get("/{client_id}/risk-analysis")
async def get_client_risk_analysis(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed churn risk analysis for a client"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Get risk analysis history
        analyses = db.query(ChurnRiskAnalysis).filter(
            ChurnRiskAnalysis.client_id == client_id
        ).order_by(desc(ChurnRiskAnalysis.analysis_date)).limit(10).all()
        
        return success_response({
            "client_id": client_id,
            "client_name": client.name,
            "current_risk_score": client.churn_risk_score,
            "current_risk_level": client.churn_risk_level,
            "analysis_history": [
                {
                    "id": analysis.id,
                    "risk_score": analysis.risk_score,
                    "risk_level": analysis.risk_level,
                    "confidence_score": analysis.confidence_score,
                    "risk_factors": analysis.risk_factors,
                    "recommendations": analysis.recommendations,
                    "model_version": analysis.model_version,
                    "analysis_date": analysis.analysis_date,
                }
                for analysis in analyses
            ]
        })
        
    except HTTPException:
        raise
    except Exception as e:
        return error_response(f"Failed to get risk analysis: {str(e)}", 500)


@router.post("/{client_id}/analyze-churn-risk")
async def analyze_churn_risk(
    client_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trigger AI-powered churn risk analysis for a client"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Schedule background analysis
        background_tasks.add_task(
            perform_churn_analysis, 
            client_id, 
            current_user.id, 
            db
        )
        
        return success_response({
            "message": "Churn risk analysis started",
            "client_id": client_id,
            "estimated_completion": "2-5 minutes"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        return error_response(f"Failed to start churn analysis: {str(e)}", 500)


async def perform_churn_analysis(client_id: int, user_id: int, db: Session):
    """Background task to perform churn risk analysis"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            return
        
        # Mock AI analysis - in reality, this would call an ML model
        risk_factors = {}
        risk_score = 0.0
        
        # Factor 1: Days since last interaction
        if client.last_interaction:
            days_since_interaction = (datetime.now() - client.last_interaction).days
            if days_since_interaction > 30:
                risk_factors["interaction_gap"] = {
                    "weight": 0.3,
                    "value": days_since_interaction,
                    "description": f"{days_since_interaction} days since last interaction"
                }
                risk_score += 0.3 * min(days_since_interaction / 90, 1.0)
        
        # Factor 2: Failed sends ratio
        total_sends = client.successful_sends_count + client.failed_sends_count
        if total_sends > 0:
            failure_rate = client.failed_sends_count / total_sends
            if failure_rate > 0.1:  # More than 10% failure rate
                risk_factors["failure_rate"] = {
                    "weight": 0.4,
                    "value": failure_rate,
                    "description": f"{failure_rate:.1%} failure rate in sends"
                }
                risk_score += 0.4 * failure_rate
        
        # Factor 3: Configuration activity
        recent_configs = db.query(ClientConfiguration).filter(
            ClientConfiguration.client_id == client_id,
            ClientConfiguration.created_at >= datetime.now() - timedelta(days=30)
        ).count()
        
        if recent_configs == 0:
            risk_factors["config_inactivity"] = {
                "weight": 0.2,
                "value": 0,
                "description": "No configuration changes in the last 30 days"
            }
            risk_score += 0.2
        
        # Factor 4: Payment issues (mock)
        # In reality, this would check payment history
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = "critical"
        elif risk_score >= 0.6:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Generate recommendations
        recommendations = []
        if "interaction_gap" in risk_factors:
            recommendations.append({
                "type": "contact",
                "priority": "high",
                "action": "Schedule a check-in call with the client",
                "expected_impact": "Restore communication and identify issues"
            })
        
        if "failure_rate" in risk_factors:
            recommendations.append({
                "type": "technical",
                "priority": "medium",
                "action": "Review and fix configuration issues causing send failures",
                "expected_impact": "Improve service reliability"
            })
        
        if "config_inactivity" in risk_factors:
            recommendations.append({
                "type": "engagement",
                "priority": "medium", 
                "action": "Offer configuration review or new features demonstration",
                "expected_impact": "Increase platform engagement"
            })
        
        # Save analysis
        analysis = ChurnRiskAnalysis(
            client_id=client_id,
            risk_score=risk_score,
            risk_level=risk_level,
            confidence_score=0.85,  # Mock confidence
            risk_factors=risk_factors,
            recommendations=recommendations,
            model_version="1.0.0"
        )
        db.add(analysis)
        
        # Update client risk info
        client.churn_risk_score = risk_score
        client.churn_risk_level = risk_level
        client.last_risk_analysis = datetime.now()
        
        # Update client status if critical risk
        if risk_level == "critical":
            client.status = "churn_risk"
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Error in churn analysis: {str(e)}")


@router.get("/{client_id}/compliance-anomalies")
async def get_compliance_anomalies(
    client_id: int,
    resolved: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance anomalies for a client"""
    try:
        query = db.query(ComplianceAnomaly).filter(
            ComplianceAnomaly.client_id == client_id
        )
        
        if resolved is not None:
            query = query.filter(ComplianceAnomaly.is_resolved == resolved)
        
        anomalies = query.order_by(desc(ComplianceAnomaly.detected_at)).all()
        
        return success_response([
            {
                "id": anomaly.id,
                "anomaly_type": anomaly.anomaly_type,
                "severity": anomaly.severity,
                "description": anomaly.description,
                "expected_pattern": anomaly.expected_pattern,
                "actual_pattern": anomaly.actual_pattern,
                "confidence_score": anomaly.confidence_score,
                "is_resolved": anomaly.is_resolved,
                "resolved_at": anomaly.resolved_at,
                "resolution_notes": anomaly.resolution_notes,
                "detected_at": anomaly.detected_at,
            }
            for anomaly in anomalies
        ])
        
    except Exception as e:
        return error_response(f"Failed to get compliance anomalies: {str(e)}", 500)


@router.post("/{client_id}/anomalies/{anomaly_id}/resolve")
async def resolve_compliance_anomaly(
    client_id: int,
    anomaly_id: int,
    resolution_notes: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resolve a compliance anomaly"""
    try:
        anomaly = db.query(ComplianceAnomaly).filter(
            ComplianceAnomaly.id == anomaly_id,
            ComplianceAnomaly.client_id == client_id
        ).first()
        
        if not anomaly:
            raise HTTPException(status_code=404, detail="Anomaly not found")
        
        anomaly.is_resolved = True
        anomaly.resolved_at = datetime.now()
        anomaly.resolution_notes = resolution_notes
        anomaly.resolved_by_user_id = current_user.id
        
        db.commit()
        
        return success_response({
            "message": "Anomaly resolved successfully",
            "anomaly_id": anomaly_id,
            "resolved_at": anomaly.resolved_at
        })
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return error_response(f"Failed to resolve anomaly: {str(e)}", 500)


@router.get("/configuration-suggestions/{client_id}")
async def get_configuration_suggestions(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered configuration suggestions for a client"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Find similar clients for suggestions
        similar_clients = db.query(Client).filter(
            Client.business_segment == client.business_segment,
            Client.tax_regime == client.tax_regime,
            Client.id != client_id
        ).all()
        
        # Get most common configurations from similar clients
        common_configs = {}
        for similar_client in similar_clients:
            configs = db.query(ClientConfiguration).filter(
                ClientConfiguration.client_id == similar_client.id,
                ClientConfiguration.status == "active"
            ).all()
            
            for config in configs:
                config_key = f"{config.name}_{similar_client.business_segment}"
                if config_key not in common_configs:
                    common_configs[config_key] = {
                        "count": 0,
                        "config": config,
                        "success_rate": 0
                    }
                common_configs[config_key]["count"] += 1
        
        # Generate suggestions
        suggestions = []
        for config_key, data in common_configs.items():
            if data["count"] >= 2:  # At least 2 similar clients use this
                usage_percentage = (data["count"] / len(similar_clients)) * 100
                suggestions.append({
                    "type": "configuration",
                    "title": f"Adicionar configuração: {data['config'].name}",
                    "description": f"{usage_percentage:.0f}% das empresas do {client.business_segment} também usam esta configuração",
                    "confidence": min(usage_percentage / 100, 0.95),
                    "expected_benefit": "Melhoria na conformidade e automação",
                    "implementation_effort": "Baixo",
                    "config_template": {
                        "name": data['config'].name,
                        "description": data['config'].description,
                        "configuration_data": data['config'].configuration_data
                    }
                })
        
        # Add document suggestions based on tax regime
        if client.tax_regime == "Simples Nacional" and client.annual_revenue and client.annual_revenue > 1000000:
            suggestions.append({
                "type": "document",
                "title": "Adicionar DEFIS à configuração",
                "description": "Empresas do Simples Nacional com faturamento > R$1M devem enviar DEFIS",
                "confidence": 0.9,
                "expected_benefit": "Compliance obrigatória",
                "implementation_effort": "Baixo",
                "document_type": "DEFIS"
            })
        
        return success_response({
            "client_id": client_id,
            "suggestions": suggestions,
            "analysis_basis": f"Baseado em {len(similar_clients)} empresas similares do segmento {client.business_segment}"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        return error_response(f"Failed to get suggestions: {str(e)}", 500)


@router.post("/simulate-configuration")
async def simulate_configuration(
    client_id: int,
    configuration_data: Dict[str, Any],
    session_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run a simulation of configuration changes"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Create simulation session
        simulation = SimulationSession(
            user_id=current_user.id,
            client_id=client_id,
            session_name=session_name or f"Simulação {client.name}",
            configuration_data=configuration_data
        )
        
        # Mock simulation logic
        validation_errors = []
        warnings = []
        
        # Validate required fields
        required_fields = ["documents", "recipients", "channels"]
        for field in required_fields:
            if field not in configuration_data:
                validation_errors.append(f"Campo obrigatório '{field}' não encontrado")
        
        # Validate document types for tax regime
        if "documents" in configuration_data and client.tax_regime:
            documents = configuration_data["documents"]
            if client.tax_regime == "Simples Nacional":
                required_docs = ["DAS", "Declaração do Simples"]
                for doc in required_docs:
                    if doc not in documents:
                        warnings.append(f"Documento '{doc}' recomendado para {client.tax_regime}")
        
        # Validate recipient formats
        if "recipients" in configuration_data:
            for recipient in configuration_data["recipients"]:
                if "@" not in recipient.get("email", ""):
                    validation_errors.append(f"Email inválido: {recipient.get('email')}")
        
        # Determine simulation success
        is_successful = len(validation_errors) == 0
        
        simulation.validation_errors = validation_errors
        simulation.is_successful = is_successful
        simulation.simulation_results = {
            "validation_errors": validation_errors,
            "warnings": warnings,
            "estimated_send_time": "2-5 minutos",
            "estimated_success_rate": 0.95 if is_successful else 0.3,
            "cost_estimate": "R$ 0,10 por documento enviado"
        }
        simulation.completed_at = datetime.now()
        
        db.add(simulation)
        db.commit()
        
        return success_response({
            "simulation_id": simulation.id,
            "is_successful": is_successful,
            "validation_errors": validation_errors,
            "warnings": warnings,
            "results": simulation.simulation_results,
            "recommendation": "Configuração aprovada para produção" if is_successful else "Corrija os erros antes de aplicar"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        return error_response(f"Failed to run simulation: {str(e)}", 500)


@router.get("/ai-insights")
async def get_ai_insights(
    insight_type: Optional[str] = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated insights for the user"""
    try:
        query = db.query(AIInsight).filter(
            AIInsight.generated_for_user_id == current_user.id
        )
        
        if insight_type:
            query = query.filter(AIInsight.insight_type == insight_type)
        
        insights = query.order_by(desc(AIInsight.generated_at)).limit(limit).all()
        
        return success_response([
            {
                "id": insight.id,
                "insight_type": insight.insight_type,
                "title": insight.title,
                "description": insight.description,
                "confidence_score": insight.confidence_score,
                "related_resource": insight.related_resource,
                "related_resource_id": insight.related_resource_id,
                "is_implemented": insight.is_implemented,
                "implementation_notes": insight.implementation_notes,
                "generated_at": insight.generated_at,
            }
            for insight in insights
        ])
        
    except Exception as e:
        return error_response(f"Failed to get AI insights: {str(e)}", 500)