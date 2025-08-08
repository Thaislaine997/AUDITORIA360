"""
Enhanced ML Training for Agent Specialization
Extends the existing ML training to create specialized agents for the collective
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from ..mcp.swarm import AgentCapability, SpecialistAgent

logger = logging.getLogger(__name__)


class AgentSpecializationTrainer:
    """Trains specialized agents for the collective mind"""

    def __init__(self, collective_mind=None):
        self.collective_mind = collective_mind
        self.training_history = []
        self.specialist_models = {}

    async def train_specialist_for_domain(
        self,
        domain: str,
        training_data: pd.DataFrame = None,
        specialization_type: str = "risk_analysis",
    ) -> str:
        """Train a new specialist agent for a specific domain"""

        logger.info(f"Training specialist for domain: {domain}")

        # Generate agent ID
        agent_id = (
            f"specialist_{domain.replace(' ', '_').lower()}_{str(uuid.uuid4())[:8]}"
        )

        # Create specialist agent
        specialist = SpecialistAgent(agent_id, specialization_type, domain)

        # Train domain-specific model if training data available
        if training_data is not None:
            model_info = await self._train_domain_model(domain, training_data)
            specialist.performance_metrics["model_accuracy"] = model_info.get(
                "accuracy", 0.0
            )
            specialist.performance_metrics["training_samples"] = len(training_data)
        else:
            # Use simulated training for demo purposes
            model_info = await self._simulate_training(domain, specialization_type)

        # Add domain-specific capabilities based on training
        capabilities = self._generate_capabilities_from_training(
            domain, specialization_type, model_info
        )
        for capability in capabilities:
            specialist.add_capability(capability)

        # Set initial performance based on training
        specialist.trust_score = model_info.get("trust_score", 0.7)
        specialist.performance_metrics["learning_rate"] = model_info.get(
            "learning_rate", 0.8
        )

        # Register with collective if available
        if self.collective_mind:
            await self.collective_mind.register_agent(specialist)

        # Store training info
        training_record = {
            "agent_id": agent_id,
            "domain": domain,
            "specialization_type": specialization_type,
            "trained_at": datetime.now().isoformat(),
            "model_info": model_info,
            "capabilities": [cap.name for cap in capabilities],
        }
        self.training_history.append(training_record)

        logger.info(f"Successfully trained specialist {agent_id} for {domain}")
        return agent_id

    async def _train_domain_model(
        self, domain: str, training_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """Train a machine learning model for the domain"""

        try:
            # Determine target column based on domain
            target_column = self._determine_target_column(domain, training_data.columns)

            if target_column not in training_data.columns:
                logger.warning(
                    f"Target column {target_column} not found, using simulated training"
                )
                return await self._simulate_training(domain, "general")

            # Prepare features and target
            y = training_data[target_column]
            numeric_features = training_data.select_dtypes(
                include=["number"]
            ).columns.tolist()

            # Remove target and ID columns from features
            features_to_remove = [target_column, "id", "index"]
            X_features = [
                col for col in numeric_features if col not in features_to_remove
            ]

            if not X_features:
                logger.warning("No suitable features found, using simulated training")
                return await self._simulate_training(domain, "general")

            X = training_data[X_features].fillna(training_data[X_features].mean())

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y if len(y.unique()) > 1 else None,
            )

            # Train model
            model = RandomForestClassifier(
                n_estimators=100, random_state=42, class_weight="balanced"
            )
            model.fit(X_train, y_train)

            # Evaluate
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)

            # Store model
            model_path = (
                f"/tmp/specialist_model_{domain.replace(' ', '_').lower()}.joblib"
            )
            joblib.dump(model, model_path)

            self.specialist_models[domain] = {
                "model": model,
                "features": X_features,
                "model_path": model_path,
            }

            return {
                "accuracy": test_score,
                "train_accuracy": train_score,
                "features_used": X_features,
                "samples_trained": len(X_train),
                "trust_score": min(0.9, test_score + 0.1),  # Trust based on performance
                "learning_rate": test_score,
                "model_path": model_path,
            }

        except Exception as e:
            logger.error(f"Error training model for domain {domain}: {e}")
            return await self._simulate_training(domain, "general")

    async def _simulate_training(
        self, domain: str, specialization_type: str
    ) -> Dict[str, Any]:
        """Simulate training when real data is not available"""

        # Simulate different performance based on domain complexity
        domain_complexity = {
            "hr": 0.8,
            "legal": 0.7,
            "financial": 0.85,
            "logistics": 0.75,
            "audit": 0.9,
            "risk": 0.8,
            "compliance": 0.7,
        }

        # Find best match for domain
        complexity_score = 0.75  # default
        for key, score in domain_complexity.items():
            if key in domain.lower():
                complexity_score = score
                break

        # Simulate training results
        simulated_accuracy = (
            complexity_score + (hash(domain) % 20) / 100
        )  # Add some variation
        simulated_accuracy = min(
            0.95, max(0.6, simulated_accuracy)
        )  # Clamp to reasonable range

        return {
            "accuracy": simulated_accuracy,
            "train_accuracy": simulated_accuracy + 0.05,
            "features_used": [f"{domain}_feature_{i}" for i in range(5)],
            "samples_trained": 1000 + (hash(domain) % 500),  # Simulated sample count
            "trust_score": min(0.9, simulated_accuracy + 0.1),
            "learning_rate": simulated_accuracy,
            "simulated": True,
        }

    def _determine_target_column(self, domain: str, columns: List[str]) -> str:
        """Determine appropriate target column based on domain"""

        domain_targets = {
            "hr": ["satisfaction", "turnover", "performance"],
            "legal": ["compliance", "risk", "violation"],
            "financial": ["profit", "cost", "revenue", "risk"],
            "logistics": ["efficiency", "delivery_time", "cost"],
            "audit": ["anomaly", "risk", "compliance"],
            "risk": ["risk_level", "severity", "probability"],
        }

        # Find best match
        for domain_key, targets in domain_targets.items():
            if domain_key in domain.lower():
                for target in targets:
                    for col in columns:
                        if target in col.lower():
                            return col

        # Default fallback targets
        default_targets = ["target", "label", "class", "outcome", "result"]
        for target in default_targets:
            for col in columns:
                if target in col.lower():
                    return col

        # If nothing found, return first column as fallback
        return columns[0] if columns else "target"

    def _generate_capabilities_from_training(
        self, domain: str, specialization_type: str, model_info: Dict[str, Any]
    ) -> List[AgentCapability]:
        """Generate agent capabilities based on training results"""

        capabilities = []
        base_proficiency = model_info.get("accuracy", 0.7)

        # Domain-specific capabilities
        if "hr" in domain.lower() or "employee" in domain.lower():
            capabilities.extend(
                [
                    AgentCapability(
                        "employee_analysis",
                        base_proficiency,
                        ["hr", "employee_satisfaction"],
                        2.0,
                    ),
                    AgentCapability(
                        "survey_design",
                        base_proficiency * 0.9,
                        ["surveys", "questionnaires"],
                        1.5,
                    ),
                    AgentCapability(
                        "satisfaction_prediction",
                        base_proficiency,
                        ["prediction", "hr"],
                        2.5,
                    ),
                ]
            )

        if "legal" in domain.lower() or "compliance" in domain.lower():
            capabilities.extend(
                [
                    AgentCapability(
                        "legal_analysis", base_proficiency, ["legal", "compliance"], 3.0
                    ),
                    AgentCapability(
                        "regulation_checking",
                        base_proficiency * 0.95,
                        ["regulations", "rules"],
                        2.0,
                    ),
                    AgentCapability(
                        "risk_assessment",
                        base_proficiency * 0.85,
                        ["risk", "legal"],
                        2.5,
                    ),
                ]
            )

        if "financial" in domain.lower() or "cost" in domain.lower():
            capabilities.extend(
                [
                    AgentCapability(
                        "financial_analysis", base_proficiency, ["finance", "cost"], 2.0
                    ),
                    AgentCapability(
                        "budget_optimization",
                        base_proficiency * 0.9,
                        ["budget", "optimization"],
                        3.0,
                    ),
                    AgentCapability(
                        "cost_prediction",
                        base_proficiency,
                        ["prediction", "finance"],
                        2.5,
                    ),
                ]
            )

        if "logistics" in domain.lower() or "delivery" in domain.lower():
            capabilities.extend(
                [
                    AgentCapability(
                        "route_optimization",
                        base_proficiency,
                        ["logistics", "routing"],
                        2.5,
                    ),
                    AgentCapability(
                        "delivery_planning",
                        base_proficiency * 0.9,
                        ["delivery", "planning"],
                        2.0,
                    ),
                    AgentCapability(
                        "supply_chain_analysis",
                        base_proficiency * 0.8,
                        ["supply_chain"],
                        3.0,
                    ),
                ]
            )

        # General capabilities based on specialization type
        if specialization_type == "risk_analysis":
            capabilities.append(
                AgentCapability(
                    "risk_modeling", base_proficiency, ["risk", "modeling"], 2.5
                )
            )
        elif specialization_type == "data_analysis":
            capabilities.append(
                AgentCapability(
                    "data_processing", base_proficiency, ["data", "analysis"], 1.5
                )
            )

        # Always add basic ML capability
        capabilities.append(
            AgentCapability(
                "machine_learning", base_proficiency * 0.7, ["ml", "prediction"], 2.0
            )
        )

        return capabilities

    async def create_emergency_specialist(
        self, required_capability: str, urgency_level: int = 3
    ) -> str:
        """Create an emergency specialist when the collective lacks required capability"""

        logger.info(
            f"Creating emergency specialist for capability: {required_capability}"
        )

        # Determine domain from capability
        domain = self._infer_domain_from_capability(required_capability)
        specialization = required_capability.replace(" ", "_").lower()

        # Create specialist with emergency training
        agent_id = await self.train_specialist_for_domain(
            domain=domain, specialization_type=specialization
        )

        # Mark as emergency specialist
        if self.collective_mind and agent_id in self.collective_mind.agents:
            specialist = self.collective_mind.agents[agent_id]
            specialist.performance_metrics["emergency_created"] = True
            specialist.performance_metrics["urgency_level"] = urgency_level
            specialist.trust_score = (
                0.6  # Lower initial trust for emergency specialists
            )

        return agent_id

    def _infer_domain_from_capability(self, capability: str) -> str:
        """Infer domain from required capability"""

        capability_domains = {
            "hr": ["employee", "satisfaction", "survey", "human"],
            "legal": ["compliance", "regulation", "legal", "law"],
            "financial": ["cost", "budget", "financial", "money"],
            "logistics": ["delivery", "route", "logistics", "transport"],
            "audit": ["audit", "review", "check", "verify"],
            "data": ["analysis", "processing", "mining", "statistics"],
        }

        capability_lower = capability.lower()

        for domain, keywords in capability_domains.items():
            if any(keyword in capability_lower for keyword in keywords):
                return domain

        return "general"

    def get_training_summary(self) -> Dict[str, Any]:
        """Get summary of all training activities"""

        return {
            "total_specialists_trained": len(self.training_history),
            "domains_covered": list(
                set(record["domain"] for record in self.training_history)
            ),
            "specialization_types": list(
                set(record["specialization_type"] for record in self.training_history)
            ),
            "average_accuracy": sum(
                record["model_info"].get("accuracy", 0)
                for record in self.training_history
            )
            / max(len(self.training_history), 1),
            "training_history": self.training_history,
            "models_stored": len(self.specialist_models),
        }

    async def fine_tune_existing_specialist(
        self,
        agent_id: str,
        new_data: pd.DataFrame = None,
        feedback: Dict[str, Any] = None,
    ) -> bool:
        """Fine-tune an existing specialist based on performance feedback"""

        if not self.collective_mind or agent_id not in self.collective_mind.agents:
            logger.warning(f"Agent {agent_id} not found for fine-tuning")
            return False

        agent = self.collective_mind.agents[agent_id]

        # Update performance based on feedback
        if feedback:
            success_rate = feedback.get(
                "success_rate", agent.performance_metrics.get("success_rate", 1.0)
            )
            agent.performance_metrics["success_rate"] = success_rate

            # Adjust trust score based on performance
            if success_rate < 0.5:
                agent.trust_score *= 0.9  # Reduce trust for poor performance
            elif success_rate > 0.8:
                agent.trust_score = min(
                    1.0, agent.trust_score * 1.1
                )  # Increase trust for good performance

        # Retrain with new data if available
        if new_data is not None:
            domain = agent.specializations[0] if agent.specializations else "general"
            model_info = await self._train_domain_model(domain, new_data)

            # Update agent capabilities based on new training
            agent.performance_metrics["model_accuracy"] = model_info.get(
                "accuracy", 0.0
            )
            agent.performance_metrics["last_retrained"] = datetime.now().isoformat()

            logger.info(
                f"Fine-tuned specialist {agent_id} with new accuracy: {model_info.get('accuracy', 0.0)}"
            )

        return True
