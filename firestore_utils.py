import firebase_admin
from firebase_admin import credentials, firestore
import os

def iniciar_firestore():
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    return firestore.client()

def salvar_auditoria_firestore(empresa, competencia, dados_auditoria):
    db = iniciar_firestore()
    doc_ref = db.collection("auditorias").document(f"{empresa}_{competencia}")
    doc_ref.set(dados_auditoria, merge=True)
    return f"Salvo com sucesso em Firestore para {empresa} - {competencia}"
