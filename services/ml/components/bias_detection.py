

import logging
import pandas as pd
from sklearn.metrics import accuracy_score

def detect_bias(model, data: pd.DataFrame, target_col: str = 'target', group_col: str = None):
    """
    Detecta viés de performance entre grupos (exemplo: accuracy por grupo).
    """
    if group_col is None:
        logging.warning("group_col não informado para bias detection.")
        return {"error": "group_col não informado"}
    X = data.drop(columns=[target_col])
    y = data[target_col]
    groups = data[group_col].unique()
    bias_report = {}
    for g in groups:
        idx = data[group_col] == g
        acc = accuracy_score(y[idx], model.predict(X[idx]))
        bias_report[str(g)] = acc
        logging.info(f"Accuracy para grupo {g}: {acc:.3f}")
    return bias_report
