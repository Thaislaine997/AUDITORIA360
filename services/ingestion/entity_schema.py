from typing import Optional

from pydantic import BaseModel, field_validator

from services.core.validators import is_iso_date, is_valid_cpf


class Entity(BaseModel):
    type: str
    text: str
    confidence: float
    cpf: Optional[str] = None
    data: Optional[str] = None
    salario: Optional[float] = None
    descontos: Optional[float] = None

    @field_validator("cpf")
    @classmethod
    def cpf_valido(cls, v):
        if v is None:
            return v
        if not is_valid_cpf(v):
            raise ValueError("CPF inválido")
        # Return cleaned CPF (numbers only)
        import re

        return re.sub(r"\D", "", v)

    @field_validator("data")
    @classmethod
    def data_iso(cls, v):
        if v is None:
            return v
        if not is_iso_date(v):
            raise ValueError("Data deve estar no formato ISO (YYYY-MM-DD)")
        return v
