# main_minimal.py (na raiz do projeto)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app_minimal = FastAPI()

class ContabilidadeOption(BaseModel):
    id: str
    nome: str

@app_minimal.get("/options/contabilidades", response_model=List[ContabilidadeOption])
async def get_contabilidades_options_minimal():
    return [ContabilidadeOption(id="1", nome="Minimal Mock 1")]

# Para rodar: uvicorn main_minimal:app_minimal --reload