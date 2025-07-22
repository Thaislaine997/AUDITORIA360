from fastapi import APIRouter, HTTPException, Body, Depends, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from src.schemas import TabelaINSS, TabelaIRRF, TabelaSalarioFamilia, TabelaSalarioMinimo, TabelaFGTS
from src.controllers import param_legais_controller

router = APIRouter()

# Endpoints para Tabela INSS
@router.post("/inss/", response_model=TabelaINSS, status_code=201,
              summary="Cria uma nova versão da tabela de INSS",
              description="Cria um novo registro de tabela de INSS com suas faixas, alíquotas e vigência.",
              tags=["Parâmetros Legais - INSS"])
async def criar_tabela_inss_endpoint(tabela_inss: TabelaINSS = Body(...)):
    return await param_legais_controller.criar_nova_tabela_inss(tabela_inss)

@router.get("/inss/", response_model=List[TabelaINSS],
            summary="Lista todas as versões das tabelas de INSS",
            tags=["Parâmetros Legais - INSS"])
async def listar_tabelas_inss_endpoint(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return await param_legais_controller.listar_tabelas_inss(skip=skip, limit=limit)

@router.get("/inss/{id_versao}", response_model=TabelaINSS,
            summary="Obtém uma versão específica da tabela de INSS",
            tags=["Parâmetros Legais - INSS"])
async def obter_tabela_inss_endpoint(id_versao: str):
    try:
        return await param_legais_controller.obter_tabela_inss_por_id(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/inss/{id_versao}", response_model=TabelaINSS,
            summary="Atualiza uma versão específica da tabela de INSS",
            description="Atualiza os dados de uma versão existente da tabela de INSS. Pode envolver a criação de uma nova versão ou ajuste de vigências.",
            tags=["Parâmetros Legais - INSS"])
async def atualizar_tabela_inss_endpoint(id_versao: str, tabela_inss: TabelaINSS = Body(...)):
    try:
        return await param_legais_controller.atualizar_tabela_inss(id_versao, tabela_inss)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/inss/{id_versao}", status_code=200, # Pode ser 204 se não retornar conteúdo
               summary="Deleta uma versão específica da tabela de INSS",
               tags=["Parâmetros Legais - INSS"])
async def deletar_tabela_inss_endpoint(id_versao: str):
    try:
        return await param_legais_controller.deletar_tabela_inss(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Tabela IRRF
@router.post("/irrf/", response_model=TabelaIRRF, status_code=201,
              summary="Cria uma nova versão da tabela de IRRF",
              description="Cria um novo registro de tabela de IRRF com suas faixas, alíquotas, deduções e vigência.",
              tags=["Parâmetros Legais - IRRF"])
async def criar_tabela_irrf_endpoint(tabela_irrf: TabelaIRRF = Body(...)):
    return await param_legais_controller.criar_nova_tabela_irrf(tabela_irrf)

@router.get("/irrf/", response_model=List[TabelaIRRF],
            summary="Lista todas as versões das tabelas de IRRF",
            tags=["Parâmetros Legais - IRRF"])
async def listar_tabelas_irrf_endpoint(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return await param_legais_controller.listar_tabelas_irrf(skip=skip, limit=limit)

@router.get("/irrf/{id_versao}", response_model=TabelaIRRF,
            summary="Obtém uma versão específica da tabela de IRRF",
            tags=["Parâmetros Legais - IRRF"])
async def obter_tabela_irrf_endpoint(id_versao: str):
    try:
        return await param_legais_controller.obter_tabela_irrf_por_id(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/irrf/{id_versao}", response_model=TabelaIRRF,
            summary="Atualiza uma versão específica da tabela de IRRF",
            tags=["Parâmetros Legais - IRRF"])
async def atualizar_tabela_irrf_endpoint(id_versao: str, tabela_irrf: TabelaIRRF = Body(...)):
    try:
        return await param_legais_controller.atualizar_tabela_irrf(id_versao, tabela_irrf)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/irrf/{id_versao}", status_code=200,
               summary="Deleta uma versão específica da tabela de IRRF",
               tags=["Parâmetros Legais - IRRF"])
async def deletar_tabela_irrf_endpoint(id_versao: str):
    try:
        return await param_legais_controller.deletar_tabela_irrf(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Tabela Salário Família
@router.post("/salario-familia/", response_model=TabelaSalarioFamilia, status_code=201,
              summary="Cria uma nova versão da tabela de Salário Família",
              description="Cria um novo registro de tabela de Salário Família com suas faixas, valores e vigência.",
              tags=["Parâmetros Legais - Salário Família"])
async def criar_tabela_salario_familia_endpoint(tabela_sf: TabelaSalarioFamilia = Body(...)):
    return await param_legais_controller.criar_nova_tabela_salario_familia(tabela_sf)

@router.get("/salario-familia/", response_model=List[TabelaSalarioFamilia],
            summary="Lista todas as versões das tabelas de Salário Família",
            tags=["Parâmetros Legais - Salário Família"])
async def listar_tabelas_salario_familia_endpoint(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return await param_legais_controller.listar_tabelas_salario_familia(skip=skip, limit=limit)

@router.get("/salario-familia/{id_versao}", response_model=TabelaSalarioFamilia,
            summary="Obtém uma versão específica da tabela de Salário Família",
            tags=["Parâmetros Legais - Salário Família"])
async def obter_tabela_salario_familia_endpoint(id_versao: str):
    try:
        return await param_legais_controller.obter_tabela_salario_familia_por_id(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/salario-familia/{id_versao}", response_model=TabelaSalarioFamilia,
            summary="Atualiza uma versão específica da tabela de Salário Família",
            tags=["Parâmetros Legais - Salário Família"])
async def atualizar_tabela_salario_familia_endpoint(id_versao: str, tabela_sf: TabelaSalarioFamilia = Body(...)):
    try:
        return await param_legais_controller.atualizar_tabela_salario_familia(id_versao, tabela_sf)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/salario-familia/{id_versao}", status_code=200,
               summary="Deleta uma versão específica da tabela de Salário Família",
               tags=["Parâmetros Legais - Salário Família"])
async def deletar_tabela_salario_familia_endpoint(id_versao: str):
    try:
        return await param_legais_controller.deletar_tabela_salario_familia(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Tabela Salário Mínimo
@router.post("/salario-minimo/", response_model=TabelaSalarioMinimo, status_code=201,
              summary="Cria uma nova versão da tabela de Salário Mínimo",
              description="Cria um novo registro de tabela de Salário Mínimo com seus valores e vigência.",
              tags=["Parâmetros Legais - Salário Mínimo"])
async def criar_tabela_salario_minimo_endpoint(tabela_sm: TabelaSalarioMinimo = Body(...)):
    return await param_legais_controller.criar_nova_tabela_salario_minimo(tabela_sm)

@router.get("/salario-minimo/", response_model=List[TabelaSalarioMinimo],
            summary="Lista todas as versões das tabelas de Salário Mínimo",
            tags=["Parâmetros Legais - Salário Mínimo"])
async def listar_tabelas_salario_minimo_endpoint(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return await param_legais_controller.listar_tabelas_salario_minimo(skip=skip, limit=limit)

@router.get("/salario-minimo/{id_versao}", response_model=TabelaSalarioMinimo,
            summary="Obtém uma versão específica da tabela de Salário Mínimo",
            tags=["Parâmetros Legais - Salário Mínimo"])
async def obter_tabela_salario_minimo_endpoint(id_versao: str):
    try:
        return await param_legais_controller.obter_tabela_salario_minimo_por_id(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/salario-minimo/{id_versao}", response_model=TabelaSalarioMinimo,
            summary="Atualiza uma versão específica da tabela de Salário Mínimo",
            tags=["Parâmetros Legais - Salário Mínimo"])
async def atualizar_tabela_salario_minimo_endpoint(id_versao: str, tabela_sm: TabelaSalarioMinimo = Body(...)):
    try:
        return await param_legais_controller.atualizar_tabela_salario_minimo(id_versao, tabela_sm)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/salario-minimo/{id_versao}", status_code=200,
               summary="Deleta uma versão específica da tabela de Salário Mínimo",
               tags=["Parâmetros Legais - Salário Mínimo"])
async def deletar_tabela_salario_minimo_endpoint(id_versao: str):
    try:
        return await param_legais_controller.deletar_tabela_salario_minimo(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Tabela FGTS
@router.post("/fgts/", response_model=TabelaFGTS, status_code=201,
              summary="Cria uma nova versão da tabela de FGTS",
              description="Cria um novo registro de tabela de FGTS com seus parâmetros e vigência.",
              tags=["Parâmetros Legais - FGTS"])
async def criar_tabela_fgts_endpoint(tabela_fgts: TabelaFGTS = Body(...)):
    return await param_legais_controller.criar_nova_tabela_fgts(tabela_fgts)

@router.get("/fgts/", response_model=List[TabelaFGTS],
            summary="Lista todas as versões das tabelas de FGTS",
            tags=["Parâmetros Legais - FGTS"])
async def listar_tabelas_fgts_endpoint(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return await param_legais_controller.listar_tabelas_fgts(skip=skip, limit=limit)

@router.get("/fgts/{id_versao}", response_model=TabelaFGTS,
            summary="Obtém uma versão específica da tabela de FGTS",
            tags=["Parâmetros Legais - FGTS"])
async def obter_tabela_fgts_endpoint(id_versao: str):
    try:
        return await param_legais_controller.obter_tabela_fgts_por_id(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/fgts/{id_versao}", response_model=TabelaFGTS,
            summary="Atualiza uma versão específica da tabela de FGTS",
            tags=["Parâmetros Legais - FGTS"])
async def atualizar_tabela_fgts_endpoint(id_versao: str, tabela_fgts: TabelaFGTS = Body(...)):
    try:
        return await param_legais_controller.atualizar_tabela_fgts(id_versao, tabela_fgts)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/fgts/{id_versao}", status_code=200,
               summary="Deleta uma versão específica da tabela de FGTS",
               tags=["Parâmetros Legais - FGTS"])
async def deletar_tabela_fgts_endpoint(id_versao: str):
    try:
        return await param_legais_controller.deletar_tabela_fgts(id_versao)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para Verificação Manual de Parâmetros Legais
class LogVerificacaoPayload(BaseModel):
    tipo_parametro: str
    link_verificado: str
    houve_alteracao: bool
    observacao_verificacao: Optional[str] = None
    # usuario_verificacao será obtido do sistema de autenticação no futuro
    # data_verificacao será gerada no backend

class LogVerificacaoResponse(BaseModel):
    id_log_verificacao: str
    tipo_parametro: str
    data_verificacao: datetime
    usuario_verificacao: str
    link_verificado: str
    houve_alteracao: bool
    observacao_verificacao: Optional[str]
    data_criacao: datetime

class FonteOficial(BaseModel):
    nome: str
    url: str

@router.post("/param-legais/log-verificacao", response_model=LogVerificacaoResponse, status_code=201,
              summary="Registra uma nova verificação manual de parâmetro legal",
              tags=["Parâmetros Legais - Verificação Manual"])
async def registrar_log_verificacao_endpoint(payload: LogVerificacaoPayload):
    # No futuro, o usuario_verificacao virá de um sistema de autenticação
    # Aqui, estamos usando um placeholder ou esperando que o controller lide com isso.
    # Se o controller precisar do usuário, precisaremos de um Depends(...) com autenticação.
    try:
        # Assumindo que o controller pode precisar do nome do usuário, mas por agora não passamos
        log_criado = await param_legais_controller.registrar_log_verificacao_manual(
            tipo_parametro=payload.tipo_parametro,
            link_verificado=payload.link_verificado,
            houve_alteracao=payload.houve_alteracao,
            observacao_verificacao=payload.observacao_verificacao,
            usuario_verificacao="admin_placeholder" # Placeholder
        )
        return log_criado
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log a exceção para depuração
        print(f"Erro ao registrar log de verificação: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao registrar log de verificação: {str(e)}")

@router.get("/param-legais/log-verificacao/ultimo/{tipo_parametro}", response_model=Optional[LogVerificacaoResponse],
             summary="Obtém o último log de verificação para um tipo de parâmetro",
             tags=["Parâmetros Legais - Verificação Manual"])
async def obter_ultimo_log_verificacao_endpoint(tipo_parametro: str):
    try:
        return await param_legais_controller.obter_ultimo_log_verificacao(tipo_parametro)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/param-legais/config/fontes-oficiais", response_model=dict[str, FonteOficial],
             summary="Obtém a configuração das fontes oficiais para os parâmetros legais",
             tags=["Parâmetros Legais - Verificação Manual"])
async def obter_config_fontes_oficiais_endpoint():
    try:
        return await param_legais_controller.obter_config_fontes_oficiais()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

