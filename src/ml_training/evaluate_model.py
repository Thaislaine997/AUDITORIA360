from sklearn.metrics import classification_report, roc_auc_score

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    proba_preds = model.predict_proba(X_test)[:, 1]
    
    print("Classification Report:\n", classification_report(y_test, preds))
    print("AUC-ROC:", roc_auc_score(y_test, proba_preds))