from google.cloud import aiplatform
import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
import os

def preparar_features_para_predicao(dados_folha_df: pd.DataFrame, features_treinamento: List[str]) -> List[Dict[str, Any]]:
    instancias_para_predicao = []
    if not dados_folha_df.empty:
        linha_features = dados_folha_df.iloc[0]
        instancia = {}
        for feature_name in features_treinamento:
            if feature_name in linha_features:
                valor = linha_features[feature_name]
                instancia[feature_name] = float(valor) if pd.notna(valor) else 0.0
            else:
                instancia[feature_name] = 0.0
        instancias_para_predicao.append(instancia)
    return instancias_para_predicao

async def gerar_predicoes_risco_folha(
    id_folha_processada: str,
    id_cliente: str,
) -> Optional[Dict[str, Any]]:
    dados_folha_df = pd.DataFrame([{
        "feature_num_total_rubricas": 150, "feature_perc_rubricas_nao_mapeadas": 0.05,
        "feature_num_func_div_alta": 1, "feature_var_total_bruto_3m": 0.1,
        "feature_flag_decimo_terceiro": False, "feature_dias_desde_ult_param_inss": 30
    }])

    try:
        features_treinamento = [
            "feature_num_total_rubricas", "feature_perc_rubricas_nao_mapeadas",
            "feature_num_func_div_alta", "feature_var_total_bruto_3m",
            "feature_flag_decimo_terceiro", "feature_dias_desde_ult_param_inss"
        ]
    except FileNotFoundError:
        print("ERRO: Arquivo features.json não encontrado. Não é possível preparar instâncias para predição.")
        return None

    instancias_para_predicao = preparar_features_para_predicao(dados_folha_df, features_treinamento)

    if not instancias_para_predicao:
        print(f"Não foi possível preparar instâncias para predição para a folha {id_folha_processada}.")
        return None

    endpoint_id = os.getenv("VERTEX_RISK_ENDPOINT_ID", "seu-endpoint-id")
    project = os.getenv("VERTEX_PROJECT_ID_PRED", "seu-projeto-gcp")
    location = os.getenv("VERTEX_LOCATION_PRED", "us-central1")

    try:
        aiplatform.init(project=project, location=location)
        endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)
        
        prediction_response = endpoint.predict(instances=instancias_para_predicao)
        
        probabilidade_risco_alto = 0.65
        classe_predita = "ALTO" if probabilidade_risco_alto > 0.5 else "BAIXO"
        id_modelo_usado = "projects/seu-projeto/locations/us-central1/models/seu_modelo_id@version"

    except Exception as e:
        print(f"Erro ao chamar Vertex AI Endpoint para folha {id_folha_processada}: {e}")
        return None

    score_saude = round((1 - probabilidade_risco_alto) * 100)

    predicao_a_salvar = {
        "id_predicao_risco": str(uuid.uuid4()),
        "id_folha_processada_fk": id_folha_processada,
        "id_cliente": id_cliente,
        "id_modelo_vertex_usado": id_modelo_usado,
        "timestamp_predicao": datetime.now(),
        "probabilidade_risco_alto_predita": float(probabilidade_risco_alto),
        "classe_risco_predita": classe_predita,
        "score_saude_folha_calculado": score_saude,
        "features_utilizadas_json": json.dumps(instancias_para_predicao[0])
    }

    print(f"MOCK - Predição a salvar: {predicao_a_salvar}")
    print(f"MOCK - Atualizar FolhasProcessadasHeader ({id_folha_processada}) com score: {score_saude}")
    
    return predicao_a_salvar