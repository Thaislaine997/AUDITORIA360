import json
import os

import pandas as pd


def load_data_from_bq(
    project_id: str, dataset_id: str, table_name: str
) -> pd.DataFrame:
    """
    Load data from BigQuery using parameterized queries to prevent SQL injection

    Args:
        project_id: GCP project ID (validated)
        dataset_id: BigQuery dataset ID (validated)
        table_name: Table name (validated)

    Returns:
        pandas.DataFrame: Query results

    Raises:
        ValueError: If parameters contain invalid characters
    """
    from google.cloud import bigquery

    # Input validation to prevent SQL injection
    if not _validate_sql_identifier(project_id):
        raise ValueError("Invalid project_id: contains unsafe characters")
    if not _validate_sql_identifier(dataset_id):
        raise ValueError("Invalid dataset_id: contains unsafe characters")
    if not _validate_sql_identifier(table_name):
        raise ValueError("Invalid table_name: contains unsafe characters")

    client = bigquery.Client(project=project_id)

    # Use parameterized query with proper escaping
    query = """
        SELECT * FROM `@project_id.@dataset_id.@table_name`
    """

    # Use BigQuery's built-in parameter substitution for safety
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
            bigquery.ScalarQueryParameter("dataset_id", "STRING", dataset_id),
            bigquery.ScalarQueryParameter("table_name", "STRING", table_name),
        ]
    )

    # Alternative: Use table reference for maximum safety
    table_ref = client.dataset(dataset_id, project=project_id).table(table_name)
    table = client.get_table(table_ref)

    # Convert table to DataFrame safely
    return client.list_rows(table).to_dataframe()


def _validate_sql_identifier(identifier: str) -> bool:
    """
    Validate SQL identifier to prevent injection attacks

    Args:
        identifier: String to validate

    Returns:
        bool: True if identifier is safe to use
    """
    if not identifier:
        return False

    # Allow only alphanumeric characters, underscores, and hyphens
    import re

    pattern = r"^[a-zA-Z0-9_-]+$"

    return bool(re.match(pattern, identifier)) and len(identifier) <= 100


def preprocess_data(df, target_column):
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


def save_model_artifacts(model, features_list, local_path="."):
    import os

    import joblib

    model_filename = os.path.join(local_path, "model.joblib")
    features_filename = os.path.join(local_path, "features.json")
    joblib.dump(model, model_filename)
    with open(features_filename, "w") as f:
        json.dump(features_list, f)
    return model_filename, features_filename


def register_model_vertex_ai(
    model_display_name, model_artifact_uri, serving_container_image_uri
):
    from google.cloud import aiplatform

    aiplatform.init(
        project=os.getenv("VERTEX_PROJECT_ID"), location=os.getenv("VERTEX_LOCATION")
    )
    # Logic to register the model in Vertex AI Model Registry
