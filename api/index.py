from fastapi import FastAPI
from portal_demandas.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AUDITORIA360 API")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AUDITORIA360 API is running!"}

# Inclua suas rotas aqui
# app.include_router(seu_router.router, prefix="/demandas", tags=["Demandas"])
# Arquivo principal da API FastAPI para deploy na Vercel
from fastapi import FastAPI

app = FastAPI()

# Importe e inclua suas rotas aqui
# from portal_demandas.api import router as demandas_router
# app.include_router(demandas_router)

@app.get("/")
def root():
    return {"message": "AUDITORIA360 API rodando na Vercel!"}
