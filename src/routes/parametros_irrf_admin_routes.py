from src.controllers.parametros_irrf_admin_controller import *
from fastapi import APIRouter
router = APIRouter()
@router.get("/parametros/irrf")
def listar_parametros_irrf():
    return listar_irrf()
@router.post("/parametros/irrf")
def criar_parametro_irrf(parametro):
    return criar_irrf(parametro)
@router.put("/parametros/irrf/{id_parametro}")
def atualizar_parametro_irrf(id_parametro, parametro):
    return atualizar_irrf(id_parametro, parametro)
@router.delete("/parametros/irrf/{id_parametro}")
def deletar_parametro_irrf(id_parametro):
    return deletar_irrf(id_parametro)
