from services.ml.components.isolation_forest import train_isolation_forest, predict_anomalies
import numpy as np

def test_isolation_forest():
    X = np.random.normal(0, 1, (100, 2))
    model = train_isolation_forest(X, contamination=0.1)
    preds = predict_anomalies(model, X)
    assert set(preds).issubset({-1, 1})
