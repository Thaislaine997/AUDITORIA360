from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uuid
import time

app = FastAPI()

# Simular armazenamento de jobs em memória
jobs = {}

@app.post("/processar-pdf")
async def processar_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF.")

    # Gerar um ID único para o job
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "PROCESSING"}

    # Simular processamento assíncrono
    time.sleep(2)  # Simular atraso inicial
    jobs[job_id]["status"] = "COMPLETED"  # Atualizar status para concluído

    return JSONResponse(content={"job_id": job_id})

@app.get("/status-job/{job_id}")
async def status_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado.")

    return JSONResponse(content={"status": job["status"]})
