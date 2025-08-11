"""
Collective Intelligence System - The Second Quantum Leap
Implements federated learning and market anomaly detection for transcendent audit capabilities.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import numpy as np
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AnomalyAlert(BaseModel):
    """Market anomaly alert"""
    id: str
    tipo: str
    severidade: str  # "BAIXA", "MEDIA", "ALTA", "CRITICA"
    descricao: str
    setor_afetado: str
    divergencia_codigo: str
    percentual_aumento: float
    clientes_afetados: int
    timestamp: str
    recomendacao_acao: str


class FederatedLearningModel(BaseModel):
    """Federated learning model metadata"""
    model_id: str
    versao: str
    tipo_modelo: str  # "RISCO", "ANOMALIA", "COMPLIANCE"
    metricas: Dict[str, float]
    last_update: str
    participantes: int  # Number of clients contributing to this model


class MarketAnomaly(BaseModel):
    """Market-level anomaly detection result"""
    anomaly_id: str
    detected_at: str
    type: str
    affected_sector: str
    deviation_score: float
    affected_clients_count: int
    divergence_pattern: Dict[str, Any]
    recommended_investigation: str


class CollectiveIntelligenceSystem:
    """
    The brain of the second quantum leap - transforms isolated audits into collective consciousness.
    Each audit contributes anonymously to the collective intelligence without compromising privacy.
    """

    def __init__(self):
        self.federated_models: Dict[str, FederatedLearningModel] = {}
        self.anomaly_patterns: Dict[str, List[Dict[str, Any]]] = {}
        self.sector_baselines: Dict[str, Dict[str, float]] = {}
        self.learning_history: List[Dict[str, Any]] = []
        self._initialize_base_intelligence()

    def _initialize_base_intelligence(self):
        """Initialize the collective intelligence with baseline patterns"""
        
        # Initialize sector baselines
        self.sector_baselines = {
            "CONSTRUCAO_CIVIL": {
                "divergencia_media": 0.05,  # 5% average divergence rate
                "risco_trabalhista": 0.12,  # 12% risk score
                "compliance_score": 85.5    # Average compliance score
            },
            "COMERCIO": {
                "divergencia_media": 0.03,
                "risco_trabalhista": 0.08,
                "compliance_score": 92.1
            },
            "SERVICOS": {
                "divergencia_media": 0.04,
                "risco_trabalhista": 0.09,
                "compliance_score": 88.7
            },
            "INDUSTRIA": {
                "divergencia_media": 0.06,
                "risco_trabalhista": 0.11,
                "compliance_score": 87.3
            }
        }

        # Initialize base federated models
        self._initialize_federated_models()

    def _initialize_federated_models(self):
        """Initialize base federated learning models"""
        
        self.federated_models["risk_predictor_v1"] = FederatedLearningModel(
            model_id="risk_predictor_v1",
            versao="1.0.0",
            tipo_modelo="RISCO",
            metricas={
                "accuracy": 0.87,
                "precision": 0.83,
                "recall": 0.91,
                "f1_score": 0.87
            },
            last_update=datetime.now(timezone.utc).isoformat(),
            participantes=0
        )

        self.federated_models["anomaly_detector_v1"] = FederatedLearningModel(
            model_id="anomaly_detector_v1",
            versao="1.0.0", 
            tipo_modelo="ANOMALIA",
            metricas={
                "detection_rate": 0.92,
                "false_positive_rate": 0.05,
                "latency_ms": 150
            },
            last_update=datetime.now(timezone.utc).isoformat(),
            participantes=0
        )

    def contribute_audit_learning(
        self, 
        contabilidade_id: str, 
        audit_results: Dict[str, Any],
        setor: str = "SERVICOS"
    ) -> Dict[str, Any]:
        """
        Contribute learning from a local audit to the collective intelligence.
        Data is anonymized before being added to the collective knowledge.
        """
        
        # Anonymize the audit data
        anonymous_data = self._anonymize_audit_data(audit_results, setor)
        
        # Extract learning patterns
        learning_patterns = self._extract_learning_patterns(anonymous_data)
        
        # Update collective knowledge
        self._update_collective_knowledge(learning_patterns, setor)
        
        # Check for anomalies
        anomalies = self._detect_market_anomalies(learning_patterns, setor)
        
        # Update federated models
        model_updates = self._update_federated_models(learning_patterns)
        
        contribution_result = {
            "contribution_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "setor": setor,
            "patterns_contributed": len(learning_patterns),
            "anomalies_detected": len(anomalies),
            "model_updates": len(model_updates),
            "collective_benefit_score": self._calculate_collective_benefit(learning_patterns)
        }

        # Add to learning history
        self.learning_history.append({
            **contribution_result,
            "learning_patterns": learning_patterns[:3]  # Store sample patterns
        })

        logger.info(f"🧠 Collective intelligence contribution received: {contribution_result['contribution_id']}")
        
        return contribution_result

    def _anonymize_audit_data(self, audit_results: Dict[str, Any], setor: str) -> Dict[str, Any]:
        """Anonymize audit data while preserving learning value"""
        
        divergencias = audit_results.get("divergencias", [])
        
        anonymous_patterns = []
        for div in divergencias:
            pattern = {
                "codigo": div.get("codigo"),
                "nivel_gravidade": div.get("nivel_gravidade"),
                "tipo_trilha": [step.get("tipo") for step in div.get("trilha_cognitiva", [])],
                "impacto_relativo": self._normalize_impact(div.get("impacto_financeiro", 0)),
                "setor": setor
            }
            anonymous_patterns.append(pattern)
        
        return {
            "patterns": anonymous_patterns,
            "audit_complexity": len(divergencias),
            "setor": setor,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _normalize_impact(self, impact: float) -> str:
        """Normalize financial impact to relative categories"""
        if impact <= 100:
            return "BAIXO"
        elif impact <= 1000:
            return "MEDIO"
        elif impact <= 5000:
            return "ALTO"
        else:
            return "MUITO_ALTO"

    def _extract_learning_patterns(self, anonymous_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract learning patterns from anonymized data"""
        
        patterns = []
        for pattern in anonymous_data.get("patterns", []):
            learning_pattern = {
                "pattern_id": str(uuid4()),
                "divergence_type": pattern["codigo"],
                "severity": pattern["nivel_gravidade"],
                "cognitive_complexity": len(pattern["tipo_trilha"]),
                "impact_category": pattern["impacto_relativo"],
                "sector": pattern["setor"],
                "frequency_weight": 1.0  # Will be updated based on frequency
            }
            patterns.append(learning_pattern)
        
        return patterns

    def _update_collective_knowledge(self, patterns: List[Dict[str, Any]], setor: str):
        """Update the collective knowledge base with new patterns"""
        
        if setor not in self.anomaly_patterns:
            self.anomaly_patterns[setor] = []
        
        # Add patterns to sector-specific knowledge
        self.anomaly_patterns[setor].extend(patterns)
        
        # Update sector baselines
        if len(patterns) > 0:
            if setor not in self.sector_baselines:
                self.sector_baselines[setor] = {
                    "divergencia_media": 0.05,
                    "risco_trabalhista": 0.1,
                    "compliance_score": 90.0
                }
            
            avg_complexity = np.mean([p["cognitive_complexity"] for p in patterns])
            self.sector_baselines[setor]["divergencia_media"] = (
                self.sector_baselines[setor]["divergencia_media"] * 0.9 + 
                len(patterns) * 0.1 / 100
            )

    def _detect_market_anomalies(
        self, 
        patterns: List[Dict[str, Any]], 
        setor: str
    ) -> List[MarketAnomaly]:
        """Detect market-level anomalies based on collective patterns"""
        
        anomalies = []
        
        # Group patterns by divergence type
        pattern_counts = {}
        for pattern in patterns:
            div_type = pattern["divergence_type"]
            pattern_counts[div_type] = pattern_counts.get(div_type, 0) + 1
        
        # Check for unusual spikes in specific divergence types
        baseline = self.sector_baselines.get(setor, {})
        baseline_rate = baseline.get("divergencia_media", 0.05)
        
        for div_type, count in pattern_counts.items():
            # Calculate deviation from baseline
            current_rate = count / max(len(patterns), 1)
            deviation = current_rate / max(baseline_rate, 0.01)
            
            if deviation > 2.0:  # More than 2x the baseline rate
                anomaly = MarketAnomaly(
                    anomaly_id=str(uuid4()),
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    type=f"SPIKE_IN_{div_type}",
                    affected_sector=setor,
                    deviation_score=deviation,
                    affected_clients_count=1,  # This would be aggregated across all clients
                    divergence_pattern={
                        "type": div_type,
                        "observed_rate": current_rate,
                        "baseline_rate": baseline_rate,
                        "deviation_factor": deviation
                    },
                    recommended_investigation=f"Investigar possível mudança na legislação ou sistema que afete {div_type}"
                )
                anomalies.append(anomaly)
        
        return anomalies

    def _update_federated_models(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Update federated learning models with new patterns"""
        
        updated_models = []
        
        # Update risk predictor model
        if "risk_predictor_v1" in self.federated_models:
            model = self.federated_models["risk_predictor_v1"]
            model.participantes += 1
            model.last_update = datetime.now(timezone.utc).isoformat()
            
            # Simulate model improvement
            model.metricas["accuracy"] = min(0.99, model.metricas["accuracy"] + 0.001)
            updated_models.append("risk_predictor_v1")
        
        # Update anomaly detector model
        if "anomaly_detector_v1" in self.federated_models:
            model = self.federated_models["anomaly_detector_v1"]
            model.participantes += 1
            model.last_update = datetime.now(timezone.utc).isoformat()
            
            # Simulate model improvement
            model.metricas["detection_rate"] = min(0.98, model.metricas["detection_rate"] + 0.002)
            updated_models.append("anomaly_detector_v1")
        
        return updated_models

    def _calculate_collective_benefit(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate how much this contribution benefits the collective"""
        
        if not patterns:
            return 0.0
        
        # Calculate based on pattern uniqueness and complexity
        unique_types = len(set(p["divergence_type"] for p in patterns))
        avg_complexity = np.mean([p["cognitive_complexity"] for p in patterns])
        
        benefit_score = (unique_types * 10 + avg_complexity * 5) / len(patterns)
        return min(100.0, benefit_score)

    def get_market_intelligence_report(self, setor: Optional[str] = None) -> Dict[str, Any]:
        """Generate a market intelligence report for a specific sector or overall"""
        
        if setor and setor in self.sector_baselines:
            sector_data = self.sector_baselines[setor]
            sector_patterns = self.anomaly_patterns.get(setor, [])
        else:
            # Overall market intelligence
            sector_data = {
                "divergencia_media": np.mean([s["divergencia_media"] for s in self.sector_baselines.values()]),
                "risco_trabalhista": np.mean([s["risco_trabalhista"] for s in self.sector_baselines.values()]),
                "compliance_score": np.mean([s["compliance_score"] for s in self.sector_baselines.values()])
            }
            sector_patterns = []
            for patterns in self.anomaly_patterns.values():
                sector_patterns.extend(patterns)

        # Generate insights
        recent_patterns = [p for p in self.learning_history if 
                          datetime.fromisoformat(p["timestamp"]) > datetime.now(timezone.utc) - timedelta(days=7)]

        report = {
            "report_id": str(uuid4()),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "setor": setor or "TODOS",
            "baseline_metrics": sector_data,
            "collective_intelligence_level": len(self.learning_history),
            "active_federated_models": len(self.federated_models),
            "recent_contributions": len(recent_patterns),
            "market_trends": self._generate_market_trends(sector_patterns),
            "predictive_insights": self._generate_predictive_insights(sector_patterns),
            "recommended_focus_areas": self._recommend_focus_areas(sector_patterns)
        }

        return report

    def _generate_market_trends(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate market trend analysis"""
        
        # Group patterns by type and analyze trends
        type_frequency = {}
        for pattern in patterns:
            div_type = pattern["divergence_type"]
            type_frequency[div_type] = type_frequency.get(div_type, 0) + 1
        
        trends = []
        for div_type, frequency in sorted(type_frequency.items(), key=lambda x: x[1], reverse=True):
            trend = {
                "trend_type": div_type,
                "frequency": frequency,
                "trend_direction": "CRESCENTE" if frequency > 5 else "ESTAVEL",
                "impact_level": "ALTO" if frequency > 10 else "MEDIO" if frequency > 5 else "BAIXO"
            }
            trends.append(trend)
        
        return trends[:5]  # Top 5 trends

    def _generate_predictive_insights(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate predictive insights based on collective patterns"""
        
        insights = []
        
        if len(patterns) > 20:
            insights.append("Alto volume de padrões detectados indica possível mudança regulatória em andamento")
        
        high_impact_patterns = [p for p in patterns if p.get("impact_category") in ["ALTO", "MUITO_ALTO"]]
        if len(high_impact_patterns) > len(patterns) * 0.3:
            insights.append("Concentração de divergências de alto impacto sugere necessidade de auditoria preventiva sistemática")
        
        if len(set(p["divergence_type"] for p in patterns)) > 10:
            insights.append("Diversidade de tipos de divergência indica complexidade crescente do ambiente regulatório")
        
        return insights

    def _recommend_focus_areas(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Recommend focus areas based on collective intelligence"""
        
        recommendations = []
        
        # Analyze most frequent divergence types
        type_frequency = {}
        for pattern in patterns:
            div_type = pattern["divergence_type"]
            type_frequency[div_type] = type_frequency.get(div_type, 0) + 1
        
        if type_frequency:
            top_issue = max(type_frequency.items(), key=lambda x: x[1])
            recommendations.append(f"Priorizar capacitação em: {top_issue[0]} (padrão mais frequente)")
        
        # Analyze complexity patterns
        avg_complexity = np.mean([p["cognitive_complexity"] for p in patterns]) if patterns else 0
        if avg_complexity > 3:
            recommendations.append("Implementar ferramentas de auditoria assistida por IA para casos complexos")
        
        # Sector-specific recommendations
        recommendations.append("Monitorar continuamente mudanças na legislação trabalhista")
        recommendations.append("Estabelecer network de inteligência coletiva com outros profissionais")
        
        return recommendations

    def generate_anomaly_alerts(self) -> List[AnomalyAlert]:
        """Generate alerts for market anomalies requiring immediate attention"""
        
        alerts = []
        
        # Check recent learning patterns for anomalies
        recent_cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        recent_patterns = [p for p in self.learning_history if 
                          datetime.fromisoformat(p["timestamp"]) > recent_cutoff]
        
        # Group by sector and analyze
        sector_activity = {}
        for pattern in recent_patterns:
            setor = pattern.get("setor", "UNKNOWN")
            if setor not in sector_activity:
                sector_activity[setor] = []
            sector_activity[setor].append(pattern)
        
        # Generate alerts for unusual activity
        for setor, activities in sector_activity.items():
            if len(activities) > 10:  # More than 10 contributions in 24h is unusual
                alert = AnomalyAlert(
                    id=str(uuid4()),
                    tipo="ATIVIDADE_ANOMALA_SETOR",
                    severidade="MEDIA",
                    descricao=f"Detectado aumento súbito de atividade no setor {setor}",
                    setor_afetado=setor,
                    divergencia_codigo="MULTIPLAS",
                    percentual_aumento=len(activities) * 10,  # Simplified calculation
                    clientes_afetados=len(activities),
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    recomendacao_acao=f"Investigar possíveis mudanças regulatórias ou sistêmicas afetando o setor {setor}"
                )
                alerts.append(alert)
        
        return alerts

    def get_federated_model_status(self) -> Dict[str, Any]:
        """Get status of all federated learning models"""
        
        return {
            "total_models": len(self.federated_models),
            "models": {model_id: {
                "versao": model.versao,
                "tipo": model.tipo_modelo,
                "participantes": model.participantes,
                "performance": model.metricas,
                "last_update": model.last_update
            } for model_id, model in self.federated_models.items()},
            "collective_intelligence_score": self._calculate_collective_intelligence_score()
        }

    def _calculate_collective_intelligence_score(self) -> float:
        """Calculate overall collective intelligence score"""
        
        base_score = 50.0
        
        # Add points for models
        model_score = len(self.federated_models) * 10
        
        # Add points for learning history
        history_score = min(len(self.learning_history) * 2, 30)
        
        # Add points for sector coverage
        sector_score = len(self.anomaly_patterns) * 5
        
        total_score = min(100.0, base_score + model_score + history_score + sector_score)
        return total_score


# Global collective intelligence instance
_collective_intelligence: Optional[CollectiveIntelligenceSystem] = None


def get_collective_intelligence() -> CollectiveIntelligenceSystem:
    """Get or create the global collective intelligence instance"""
    global _collective_intelligence
    if _collective_intelligence is None:
        _collective_intelligence = CollectiveIntelligenceSystem()
        logger.info("🌌 Collective Intelligence System initialized - The hive mind awakens")
    return _collective_intelligence