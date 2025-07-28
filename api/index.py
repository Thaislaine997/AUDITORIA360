# Arquivo principal da API FastAPI para deploy na Vercel
from fastapi import FastAPI

app = FastAPI()

# Importe e inclua suas rotas aqui
# from portal_demandas.api import router as demandas_router
# app.include_router(demandas_router)

@app.get("/")
def root():
    return {"message": "AUDITORIA360 API rodando na Vercel!"}
