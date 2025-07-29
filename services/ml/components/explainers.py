import logging

import pandas as pd
import shap


def explain_model(model, data: pd.DataFrame, nsamples: int = 100):
    """
    Gera explicações SHAP para o modelo treinado.
    """
    logging.info(f"Gerando explicações SHAP para {nsamples} amostras...")
    explainer = shap.Explainer(model, data)
    shap_values = explainer(data.iloc[:nsamples])
    logging.info("Explicações SHAP geradas.")
    return shap_values
