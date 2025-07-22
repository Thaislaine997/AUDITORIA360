import shap
import numpy as np

def explain_with_shap(model, X: np.ndarray, nsamples=100):
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X[:nsamples])
    return shap_values
