from sklearn.ensemble import IsolationForest
import numpy as np


def train_isolation_forest(X: np.ndarray, contamination: float = 0.05):
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)
    return model


def predict_anomalies(model, X: np.ndarray):
    preds = model.predict(X)
    # -1 = anomalia, 1 = normal
    return preds
