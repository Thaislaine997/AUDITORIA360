import json
import os

import joblib
import pandas as pd
from google.cloud import aiplatform, bigquery
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split


def load_data_from_bq(
    project_id: str, dataset_id: str, table_name: str
) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}`"
    return client.query(query).to_dataframe()


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
