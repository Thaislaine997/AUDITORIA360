def load_data_from_bq(project_id: str, dataset_id: str, table_name: str):
    from google.cloud import bigquery
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}`"
    return client.query(query).to_dataframe()

def preprocess_data(df, target_column):
    df = df.dropna(subset=[target_column])
    y = df[target_column]
    numeric_features = df.select_dtypes(include=['number']).columns.tolist()
    features_to_drop_from_numeric = [target_column, 'id_registro_treinamento', 'id_folha_processada_referencia']
    X_numeric = df[numeric_features].drop(columns=[col for col in features_to_drop_from_numeric if col in numeric_features], errors='ignore')
    X_numeric = X_numeric.fillna(X_numeric.mean())
    lista_de_features_usadas = list(X_numeric.columns)
    return X_numeric, y, lista_de_features_usadas

def save_model_artifacts(model, features_list, local_path="."):
    import joblib
    import os
    model_filename = os.path.join(local_path, "model.joblib")
    features_filename = os.path.join(local_path, "features.json")
    joblib.dump(model, model_filename)
    with open(features_filename, 'w') as f:
        json.dump(features_list, f)
    return model_filename, features_filename

def register_model_vertex_ai(model_display_name, model_artifact_uri, serving_container_image_uri):
    from google.cloud import aiplatform
    aiplatform.init(project=os.getenv("VERTEX_PROJECT_ID"), location=os.getenv("VERTEX_LOCATION"))
    # Logic to register the model in Vertex AI Model Registry
    pass