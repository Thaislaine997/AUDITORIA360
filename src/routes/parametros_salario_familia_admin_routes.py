from src.controllers.parametros_salario_familia_admin_controller import *
from fastapi import APIRouter
router = APIRouter()
@router.get("/parametros/salario-familia")
def listar_parametros_salario_familia():
    return listar_salario_familia()
@router.post("/parametros/salario-familia")
def criar_parametro_salario_familia(parametro):
    return criar_salario_familia(parametro)
@router.put("/parametros/salario-familia/{id_parametro}")
def atualizar_parametro_salario_familia(id_parametro, parametro):
    return atualizar_salario_familia(id_parametro, parametro)
@router.delete("/parametros/salario-familia/{id_parametro}")
def deletar_parametro_salario_familia(id_parametro):
    return deletar_salario_familia(id_parametro)
