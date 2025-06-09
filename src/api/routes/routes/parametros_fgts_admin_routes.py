from src.controllers.parametros_fgts_admin_controller import *
from fastapi import APIRouter
router = APIRouter()
@router.get("/parametros/fgts")
def listar_parametros_fgts():
    return listar_fgts()
@router.post("/parametros/fgts")
def criar_parametro_fgts(parametro):
    return criar_fgts(parametro)
@router.put("/parametros/fgts/{id_parametro}")
def atualizar_parametro_fgts(id_parametro, parametro):
    return atualizar_fgts(id_parametro, parametro)
@router.delete("/parametros/fgts/{id_parametro}")
def deletar_parametro_fgts(id_parametro):
    return deletar_fgts(id_parametro)
