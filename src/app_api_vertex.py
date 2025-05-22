from fastapi import FastAPI, Request
from pydantic import BaseModel
from .vertex_utils import prever_rubrica_com_vertex

app = FastAPI(title="API Vertex AI - Classificação de CCTs")

class ClausulaRequest(BaseModel):
    texto: str

@app.post("/prever-rubrica/")
async def prever_rubrica(req: ClausulaRequest):
    rubrica = prever_rubrica_com_vertex(req.texto)
    return {"rubrica_prevista": rubrica or "Não identificado"}
