"""
Rotas administrativas para CRUD de parâmetros legais (INSS, IRRF, Salário Família, Salário Mínimo, FGTS).
"""
from fastapi import APIRouter, HTTPException
from src.controllers import parametros_legais_admin_controller

router = APIRouter(prefix="/api/v1/parametros-legais-admin", tags=["Parâmetros Legais Admin"])

@router.get("/inss")
def listar_inss():
    return parametros_legais_admin_controller.listar_inss()

@router.post("/inss")
def criar_inss(parametro: dict):
    return parametros_legais_admin_controller.criar_inss(parametro)

@router.put("/inss/{id_parametro_inss}")
def atualizar_inss(id_parametro_inss: str, parametro: dict):
    return parametros_legais_admin_controller.atualizar_inss(id_parametro_inss, parametro)

@router.delete("/inss/{id_parametro_inss}")
def deletar_inss(id_parametro_inss: str):
    return parametros_legais_admin_controller.deletar_inss(id_parametro_inss)

# (Repetir para IRRF, Salário Família, Salário Mínimo, FGTS)
