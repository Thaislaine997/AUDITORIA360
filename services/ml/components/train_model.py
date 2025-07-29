import logging

import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_model(data: pd.DataFrame, target_col: str = "target"):
    """
    Treina um modelo RandomForest simples.
    """
    logging.info(f"Iniciando treinamento com {len(data)} amostras...")
    X = data.drop(columns=[target_col])
    y = data[target_col]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    logging.info("Treinamento concluído.")
    return model
