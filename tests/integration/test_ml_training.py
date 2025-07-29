import pandas as pd
import pytest


# Mock das funções de treinamento
def load_data_from_bq(*args, **kwargs):
    return []


def preprocess_data(*args, **kwargs):
    return []


def train_model(*args, **kwargs):
    return None


def evaluate_model(*args, **kwargs):
    return {}


@pytest.fixture
def sample_data():
    data = {
        "feature_num_total_rubricas": [150, 200, 250],
        "feature_perc_rubricas_nao_mapeadas": [0.05, 0.10, 0.15],
        "feature_num_func_div_alta": [1, 2, 0],
        "feature_var_total_bruto_3m": [0.1, 0.2, 0.3],
        "feature_flag_decimo_terceiro": [False, True, False],
        "feature_dias_desde_ult_param_inss": [30, 60, 90],
        "target_risco_alta_severidade_ocorreu": [True, False, True],
    }
    return pd.DataFrame(data)


def test_load_data_from_bq(mocker):
    mocker.patch("google.cloud.bigquery.Client.query", return_value=pd.DataFrame())
    df = load_data_from_bq("project_id", "dataset_id", "table_name")
    assert isinstance(df, pd.DataFrame)


def test_preprocess_data(sample_data):
    X, y, features_used = preprocess_data(
        sample_data, "target_risco_alta_severidade_ocorreu"
    )
    assert X.shape[0] == 3
    assert len(features_used) == 6


def test_train_model(sample_data):
    X, y, _ = preprocess_data(sample_data, "target_risco_alta_severidade_ocorreu")
    model = train_model(X, y)
    assert model is not None


def test_evaluate_model(sample_data):
    X, y, _ = preprocess_data(sample_data, "target_risco_alta_severidade_ocorreu")
    model = train_model(X, y)
    metrics = evaluate_model(model, X, y)
    assert "AUC-ROC" in metrics
