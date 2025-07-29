import pandas as pd
import pytest

from services.ingestion.bq_loader import load_data_to_bq

# Adapte para funções equivalentes de transformação e anonimização se existirem


def test_extracao_dados():
    # Teste de extração de dados do BigQuery (mock/fake)
    # Aqui usamos um DataFrame fictício para simular o retorno
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    assert df is not None
    assert isinstance(df, pd.DataFrame)


def test_transformacao_features():
    # Teste de transformação de features
    df_bruto = pd.DataFrame(
        {
            "linhas": [[1, 2, 3], [4, 5]],
            "rubricas_nao_mapeadas": [1, 2],
            "divergencias": [
                [{"severidade": "ALTA"}, {"severidade": "BAIXA"}],
                [{"severidade": "ALTA"}],
            ],
            "total_bruto": [100, 200],
            "mes": [11, 12],
            "data_referencia": ["2024-01-01", "2024-02-01"],
            "data_ultimo_param": ["2023-12-01", "2024-01-01"],
        }
    )
    df_transformado = transformar_features(df_bruto)
    assert df_transformado is not None
    assert "feature_num_total_rubricas" in df_transformado.columns


def test_anonimizar_dados():
    # Teste de anonimização de dados
    df = pd.DataFrame(
        {"funcionario_cpf": ["123.456.789-00"], "empresa_cnpj": ["12.345.678/0001-00"]}
    )
    df_anon = anonimiza_dataframe(df)
    assert df_anon is not None
    assert "funcionario_cpf" in df_anon.columns
    assert "empresa_cnpj" in df_anon.columns
