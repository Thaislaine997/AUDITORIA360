from pydantic import BaseModel, validator
from typing import Optional
from services.core.validators import is_valid_cpf, is_iso_date

class Entity(BaseModel):
    type: str
    text: str
    confidence: float
    cpf: Optional[str] = None
    data: Optional[str] = None
    salario: Optional[float] = None
    descontos: Optional[float] = None

    @validator('cpf')
    def cpf_valido(cls, v):
        if v is None:
            return v
        if not is_valid_cpf(v):
            raise ValueError('CPF inválido')
        return v

    @validator('data')
    def data_iso(cls, v):
        if v is None:
            return v
        if not is_iso_date(v):
            raise ValueError('Data deve estar no formato ISO (YYYY-MM-DD)')
        return v
