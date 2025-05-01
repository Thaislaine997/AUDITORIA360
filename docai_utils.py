import json
import pandas as pd
from google.cloud import documentai_v1 as documentai

with open("config.json") as f:
    CONFIG = json.load(f)

def processar_extrato_pdf(file):
    client = documentai.DocumentUnderstandingServiceClient()
    name = f"projects/{CONFIG['project_id']}/locations/{CONFIG['location']}/processors/{CONFIG['docai_extrato_id']}"
    raw_document = documentai.RawDocument(content=file.read(), mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    return pd.DataFrame([{ "type": ent.type_, "value": ent.mention_text } for ent in document.entities])

def processar_cct_pdf(file):
    client = documentai.DocumentUnderstandingServiceClient()
    name = f"projects/{CONFIG['project_id']}/locations/{CONFIG['location']}/processors/{CONFIG['docai_cct_id']}"
    raw_document = documentai.RawDocument(content=file.read(), mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    return pd.DataFrame([
        { "regra": "piso_efetivo", "valor": "1600.00" },
        { "regra": "he_100", "valor": "2.0" },
        { "regra": "adicional_noturno", "valor": "0.20" }
    ])

def cruzar_folha_cct(df_folha, df_cct):
    resultado = []
    regras = { row["regra"]: float(row["valor"]) for _, row in df_cct.iterrows() }
    for _, row in df_folha.iterrows():
        tipo = row["type"]
        valor = float(row["value"]) if row["value"].replace('.', '', 1).isdigit() else 0.0
        if tipo in regras:
            esperado = regras[tipo]
            status = "OK" if abs(valor - esperado) <= 0.05 else "NOK"
            resultado.append({ "item": tipo, "pago": valor, "esperado": esperado, "resultado": status })
    return pd.DataFrame(resultado)
