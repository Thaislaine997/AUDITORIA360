from typing import List, Dict
import pandas as pd

def transformar_features(df: pd.DataFrame) -> pd.DataFrame:
    # Exemplo de transformação de features
    df['feature_num_total_rubricas'] = df['linhas'].apply(lambda x: len(x))
    df['feature_perc_rubricas_nao_mapeadas'] = df['rubricas_nao_mapeadas'] / df['feature_num_total_rubricas']
    df['feature_num_func_div_alta'] = df['divergencias'].apply(lambda x: sum(1 for d in x if d['severidade'] == 'ALTA'))
    df['feature_var_total_bruto_3m'] = df['total_bruto'].rolling(window=3).var()
    df['feature_flag_decimo_terceiro'] = df['mes'].apply(lambda x: 1 if x in [11, 12] else 0)
    df['feature_dias_desde_ult_param_inss'] = (pd.to_datetime(df['data_referencia']) - pd.to_datetime(df['data_ultimo_param'])).dt.days

    return df

def preparar_dados_para_modelo(df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
    return df[features]