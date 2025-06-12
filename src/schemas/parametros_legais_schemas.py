from pydantic import BaseModel
from typing import List, Optional

class TabelaSalarioMinimo(BaseModel):
    ano: int
    valor: float

class TabelaSalarioFamilia(BaseModel):
    ano: int
    faixa: str
    valor: float

class TabelaFGTS(BaseModel):
    ano: int
    aliquota: float

class TabelaIRRF(BaseModel):
    ano: int
    faixas: list

class FaixaIRRF(BaseModel):
    faixa: str
    valor: float

class TabelaINSS(BaseModel):
    ano: int
    faixas: list

class FaixaINSS(BaseModel):
    faixa: str
    valor: float
