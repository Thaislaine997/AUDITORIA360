from src.controllers.parametros_salario_minimo_admin_controller import *
from fastapi import APIRouter
router = APIRouter()
@router.get("/parametros/salario-minimo")
def listar_parametros_salario_minimo():
    return listar_salario_minimo()
@router.post("/parametros/salario-minimo")
def criar_parametro_salario_minimo(parametro):
    return criar_salario_minimo(parametro)
@router.put("/parametros/salario-minimo/{id_parametro}")
def atualizar_parametro_salario_minimo(id_parametro, parametro):
    return atualizar_salario_minimo(id_parametro, parametro)
@router.delete("/parametros/salario-minimo/{id_parametro}")
def deletar_parametro_salario_minimo(id_parametro):
    return deletar_salario_minimo(id_parametro)
