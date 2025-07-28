from fastapi import FastAPI
from portal_demandas.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AUDITORIA360 API")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AUDITORIA360 API is running!"}

# Inclua suas rotas aqui

# --- Endpoints de upload/download para Cloudflare R2 ---
from fastapi import UploadFile, File, HTTPException
from services.storage_utils import upload_file_to_r2
import shutil
import os

@app.post("/upload-r2/")
async def upload_r2(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        upload_file_to_r2(temp_path, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_path)
    return {"status": "ok", "filename": file.filename}
# Arquivo principal da API FastAPI para deploy na Vercel
from fastapi import FastAPI

app = FastAPI()

# Importe e inclua suas rotas aqui
# from portal_demandas.api import router as demandas_router
# app.include_router(demandas_router)

@app.get("/")
def root():
    return {"message": "AUDITORIA360 API rodando na Vercel!"}
