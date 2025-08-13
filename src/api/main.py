from fastapi import FastAPI, Query
from src.main import process_document_ocr, process_control_sheet

app = FastAPI(title="AUDITORIA360 API", description="API para processamento de documentos e planilhas.")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ocr")
def ocr_endpoint(file_name: str = Query(...), bucket_name: str = Query(...)):
    """
    Endpoint para processar documento PDF via OCR.
    """
    return process_document_ocr(file_name, bucket_name)

@app.post("/planilha")
def planilha_endpoint(file_name: str = Query(...), bucket_name: str = Query(...)):
    """
    Endpoint para processar planilha de controle.
    """
    return process_control_sheet(file_name, bucket_name)
