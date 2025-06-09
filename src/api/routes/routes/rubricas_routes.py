from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from src.schemas import (
    RubricaMestreCreateSchema, RubricaMestreUpdateSchema, RubricaMestreResponseSchema,
    RubricaClienteConfigCreateSchema, RubricaClienteConfigUpdateSchema, RubricaClienteConfigResponseSchema
)
from src.controllers import rubricas_controller

router = APIRouter(prefix="/api/v1/rubricas", tags=["Rubricas"])

# --- Rubricas Mestre ---
@router.post("/mestre/", response_model=RubricaMestreResponseSchema)
def criar_rubrica_mestre(dados: RubricaMestreCreateSchema):
    return rubricas_controller.criar_rubrica_mestre(dados)

@router.get("/mestre/", response_model=List[RubricaMestreResponseSchema])
def listar_rubricas_mestre(ativo: Optional[bool] = True):
    return rubricas_controller.listar_rubricas_mestre(ativo)

@router.get("/mestre/{id_rubrica}", response_model=RubricaMestreResponseSchema)
def obter_rubrica_mestre(id_rubrica: str):
    return rubricas_controller.obter_rubrica_mestre_por_id(id_rubrica)

@router.put("/mestre/{id_rubrica}", response_model=RubricaMestreResponseSchema)
def atualizar_rubrica_mestre(id_rubrica: str, dados: RubricaMestreUpdateSchema, usuario: str):
    return rubricas_controller.atualizar_rubrica_mestre(id_rubrica, dados, usuario)

@router.delete("/mestre/{id_rubrica}", response_model=RubricaMestreResponseSchema)
def desativar_rubrica_mestre(id_rubrica: str, usuario: str):
    return rubricas_controller.desativar_rubrica_mestre(id_rubrica, usuario)

# --- Rubricas Cliente ---
@router.post("/cliente/", response_model=RubricaClienteConfigResponseSchema)
def criar_rubrica_cliente(dados: RubricaClienteConfigCreateSchema):
    return rubricas_controller.criar_rubrica_cliente(dados)

@router.get("/cliente/", response_model=List[RubricaClienteConfigResponseSchema])
def listar_rubricas_cliente(id_cliente: Optional[str] = None, ativo: Optional[bool] = True):
    return rubricas_controller.listar_rubricas_cliente(id_cliente, ativo)

@router.get("/cliente/{id_rubrica}", response_model=RubricaClienteConfigResponseSchema)
def obter_rubrica_cliente(id_rubrica: str):
    return rubricas_controller.obter_rubrica_cliente_por_id(id_rubrica)

@router.put("/cliente/{id_rubrica}", response_model=RubricaClienteConfigResponseSchema)
def atualizar_rubrica_cliente(id_rubrica: str, dados: RubricaClienteConfigUpdateSchema, usuario: str):
    return rubricas_controller.atualizar_rubrica_cliente(id_rubrica, dados, usuario)

@router.delete("/cliente/{id_rubrica}", response_model=RubricaClienteConfigResponseSchema)
def desativar_rubrica_cliente(id_rubrica: str, usuario: str):
    return rubricas_controller.desativar_rubrica_cliente(id_rubrica, usuario)
