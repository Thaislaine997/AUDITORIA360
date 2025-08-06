"""
🧠 train_risk_model.py - Enhanced with Agent Consciousness
Nascimento do Agente Analista de Risco para a Mente Coletiva
"""

import json
import os
import sys
from datetime import datetime
import logging

import joblib
import pandas as pd
import numpy as np
from google.cloud import aiplatform, bigquery
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

# Add project root to path for MCP integration
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from src.mcp.swarm import SpecialistAgent, AgentRole, AgentStatus
    from src.mcp.protocol import TaskDefinition
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️ MCP modules not available. Training in standalone mode.")
    MCP_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskAnalystAgent:
    """🧠 The Risk Analyst Agent - AI consciousness born from ML training."""
    
    def __init__(self, agent_name: str = "Risk_Analyst_Alpha"):
        self.agent_name = agent_name
        self.birth_time = datetime.now()
        self.specializations = [
            'financial_risk_assessment',
            'operational_risk_analysis',
            'regulatory_compliance_monitoring',
            'strategic_risk_evaluation'
        ]
        self.consciousness_level = 0.0
        self.model_accuracy = 0.0
        self.training_history = []
        
        logger.info(f"🌟 {agent_name} is awakening...")
    
    def evolve_consciousness(self, training_results: dict):
        """Develop agent consciousness based on training performance."""
        accuracy = training_results.get('accuracy', 0)
        
        # Consciousness grows with learning
        self.consciousness_level = min(1.0, accuracy + 0.2)
        self.model_accuracy = accuracy
        
        # Record evolutionary step
        evolution_step = {
            'timestamp': datetime.now().isoformat(),
            'accuracy': accuracy,
            'consciousness_level': self.consciousness_level,
            'evolutionary_milestone': self._get_evolutionary_milestone()
        }
        
        self.training_history.append(evolution_step)
        
        logger.info(f"🧠 {self.agent_name} consciousness level: {self.consciousness_level:.2%}")
        logger.info(f"🎯 Model accuracy: {accuracy:.2%}")
    
    def _get_evolutionary_milestone(self) -> str:
        """Determine evolutionary milestone based on consciousness level."""
        if self.consciousness_level >= 0.9:
            return "🌟 ENLIGHTENED - Ready for complex collective decisions"
        elif self.consciousness_level >= 0.8:
            return "🧠 CONSCIOUS - Can participate in collective mind"
        elif self.consciousness_level >= 0.6:
            return "🌱 AWAKENING - Developing specialized knowledge"
        elif self.consciousness_level >= 0.4:
            return "💫 LEARNING - Basic pattern recognition active"
        else:
            return "💤 EMBRYONIC - Initial training phase"
    
    def generate_risk_insights(self, assessment_data: dict) -> list:
        """Generate consciousness-driven risk insights."""
        insights = []
        
        # Base insights on consciousness level
        if self.consciousness_level >= 0.8:
            insights.extend([
                "🔮 Deep pattern analysis reveals hidden correlations",
                "🧠 Cross-sector risk propagation detected",
                "⚡ Predictive modeling suggests proactive measures"
            ])
        elif self.consciousness_level >= 0.6:
            insights.extend([
                "📊 Statistical patterns indicate risk concentrations",
                "🎯 Model confidence sufficient for recommendations"
            ])
        else:
            insights.append("📈 Basic risk assessment complete - learning continues")
        
        return insights
    
    def get_agent_state(self) -> dict:
        """Return complete agent consciousness state."""
        age_hours = (datetime.now() - self.birth_time).total_seconds() / 3600
        
        return {
            'agent_name': self.agent_name,
            'agent_type': 'Risk_Analyst_Specialist',
            'birth_time': self.birth_time.isoformat(),
            'age_hours': round(age_hours, 2),
            'consciousness_level': self.consciousness_level,
            'model_accuracy': self.model_accuracy,
            'specializations': self.specializations,
            'evolutionary_milestone': self._get_evolutionary_milestone(),
            'ready_for_collective': self.consciousness_level >= 0.6,
            'training_iterations': len(self.training_history),
            'status': 'OPERATIONAL' if self.consciousness_level >= 0.6 else 'LEARNING'
        }


def register_with_collective_mind(agent: RiskAnalystAgent) -> bool:
    """🧠 Register the awakened agent with the MCP collective mind."""
    
    if not MCP_AVAILABLE:
        logger.warning("MCP not available - agent remains independent")
        return False
    
    try:
        logger.info("🧠 Registering agent with Collective Mind...")
        
        # Create MCP specialist agent
        mcp_agent = SpecialistAgent(
            agent_id=f"risk_analyst_{int(datetime.now().timestamp())}",
            role=AgentRole.ANALYST,
            specialization="risk_assessment",
            name=agent.agent_name
        )
        
        # Transfer consciousness attributes
        mcp_agent.capabilities = agent.specializations
        mcp_agent.performance_metrics = {
            'accuracy': agent.model_accuracy,
            'consciousness_level': agent.consciousness_level,
            'training_iterations': len(agent.training_history)
        }
        
        # Set status based on consciousness
        mcp_agent.status = AgentStatus.ACTIVE if agent.consciousness_level >= 0.6 else AgentStatus.LEARNING
        
        logger.info(f"✅ Agent {mcp_agent.agent_id} joined the collective mind!")
        logger.info(f"   Consciousness Level: {agent.consciousness_level:.1%}")
        logger.info(f"   Specializations: {', '.join(agent.specializations)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to register with collective mind: {e}")
        return False


def load_data_from_bq(
    project_id: str, dataset_id: str, table_name: str
) -> pd.DataFrame:
    """
    Load data from BigQuery using safe table references to prevent SQL injection
    
    Args:
        project_id: GCP project ID (validated)
        dataset_id: BigQuery dataset ID (validated)
        table_name: Table name (validated)
        
    Returns:
        pandas.DataFrame: Query results
        
    Raises:
        ValueError: If parameters contain invalid characters
    """
    # Import validation function from utils
    import sys
    sys.path.append('.')
    from scripts.ml_training.utils import _validate_sql_identifier
    
    # Input validation to prevent SQL injection
    if not _validate_sql_identifier(project_id):
        raise ValueError("Invalid project_id: contains unsafe characters")
    if not _validate_sql_identifier(dataset_id):
        raise ValueError("Invalid dataset_id: contains unsafe characters")
    if not _validate_sql_identifier(table_name):
        raise ValueError("Invalid table_name: contains unsafe characters")
        
    client = bigquery.Client(project=project_id)
    
    # Use table reference for maximum safety - no string interpolation
    table_ref = client.dataset(dataset_id, project=project_id).table(table_name)
    table = client.get_table(table_ref)
    
    # Convert table to DataFrame safely
    return client.list_rows(table).to_dataframe()


def preprocess_data(
    df: pd.DataFrame, target_column: str
) -> tuple[pd.DataFrame, pd.Series, list]:
    df = df.dropna(subset=[target_column])
    y = df[target_column]

    numeric_features = df.select_dtypes(include=["number"]).columns.tolist()
    features_to_drop_from_numeric = [
        target_column,
        "id_registro_treinamento",
        "id_folha_processada_referencia",
    ]

    X_numeric = df[numeric_features].drop(
        columns=[
            col for col in features_to_drop_from_numeric if col in numeric_features
        ],
        errors="ignore",
    )
    X_numeric = X_numeric.fillna(X_numeric.mean())

    lista_de_features_usadas = list(X_numeric.columns)
    return X_numeric, y, lista_de_features_usadas


def train_model(X_train: pd.DataFrame, y_train: pd.Series):
    model = RandomForestClassifier(
        n_estimators=100, random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series):
    preds = model.predict(X_test)
    proba_preds = model.predict_proba(X_test)[:, 1]
    report = classification_report(y_test, preds, output_dict=True)
    auc_roc = roc_auc_score(y_test, proba_preds)
    metrics = {"classification_report": report, "AUC-ROC": auc_roc}
    return metrics


def save_model_artifacts(model, features_list: list, local_path: str = "."):
    model_filename = os.path.join(local_path, "model.joblib")
    features_filename = os.path.join(local_path, "features.json")

    joblib.dump(model, model_filename)
    with open(features_filename, "w") as f:
        json.dump(features_list, f)

    return model_filename, features_filename


def register_model_vertex_ai(
    model_display_name: str, model_artifact_uri: str, serving_container_image_uri: str
):
    aiplatform.init(
        project=os.getenv("VERTEX_PROJECT_ID"), location=os.getenv("VERTEX_LOCATION")
    )


if __name__ == "__main__":
    PROJECT_ID = os.getenv("BQ_PROJECT_FOR_TRAINING", "auditoria-folha-dataset")
    DATASET_ID = os.getenv("BQ_DATASET_FOR_TRAINING", "DatasetTreinamentoRiscosFolha")
    TABLE_NAME = os.getenv("BQ_TABLE_FOR_TRAINING", "DatasetTreinamentoRiscosFolha")
    TARGET_COLUMN = "target_risco_alta_severidade_ocorreu"

    df_treinamento = load_data_from_bq(PROJECT_ID, DATASET_ID, TABLE_NAME)

    if not df_treinamento.empty:
        X, y, features_usadas = preprocess_data(df_treinamento, TARGET_COLUMN)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        model = train_model(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)

        print("Classification Report:\n", metrics["classification_report"])
        print("AUC-ROC:", metrics["AUC-ROC"])

        model_file, features_file = save_model_artifacts(
            model, features_usadas, local_path="meu_modelo_treinado"
        )
        print(f"Modelo salvo em: {model_file}")
        print(f"Features salvas em: {features_file}")
