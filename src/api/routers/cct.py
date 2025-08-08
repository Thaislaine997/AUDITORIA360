"""
CCT (Collective Labor Agreements) API Router
Módulo 3: Base de Convenções Coletivas (CCTs)
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.services.cct_service import CCTService

router = APIRouter()


# Modelos Pydantic para validação de dados
class SindicatoCreate(BaseModel):
    nome_sindicato: str
    cnpj: Optional[str] = None
    base_territorial: Optional[str] = None
    categoria_representada: Optional[str] = None


class SindicatoUpdate(BaseModel):
    nome_sindicato: Optional[str] = None
    cnpj: Optional[str] = None
    base_territorial: Optional[str] = None
    categoria_representada: Optional[str] = None


class ConvencaoColetivaCreate(BaseModel):
    sindicato_id: int
    numero_registro_mte: Optional[str] = None
    vigencia_inicio: str  # ISO date format
    vigencia_fim: str     # ISO date format
    link_documento_oficial: Optional[str] = None
    dados_cct: Optional[Dict] = None


class ConvencaoColetivaUpdate(BaseModel):
    numero_registro_mte: Optional[str] = None
    vigencia_inicio: Optional[str] = None
    vigencia_fim: Optional[str] = None
    link_documento_oficial: Optional[str] = None
    dados_cct: Optional[Dict] = None


# Dependency para obter instância do serviço
def get_cct_service():
    return CCTService()


# Endpoints para Sindicatos
@router.post("/sindicatos", summary="Criar novo sindicato")
async def criar_sindicato(
    sindicato: SindicatoCreate,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Cria um novo sindicato"""
    try:
        resultado = cct_service.criar_sindicato(sindicato.dict())
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar sindicato: {str(e)}"
        )


@router.get("/sindicatos", summary="Listar sindicatos")
async def listar_sindicatos(
    limit: int = 100,
    offset: int = 0,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Lista todos os sindicatos disponíveis"""
    try:
        sindicatos = cct_service.listar_sindicatos(limit=limit, offset=offset)
        return {"status": "success", "data": sindicatos}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar sindicatos: {str(e)}"
        )


@router.get("/sindicatos/{sindicato_id}", summary="Obter sindicato")
async def obter_sindicato(
    sindicato_id: int,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Obtém os dados de um sindicato específico"""
    try:
        sindicato = cct_service.obter_sindicato(sindicato_id)
        if not sindicato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sindicato não encontrado"
            )
        return {"status": "success", "data": sindicato}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter sindicato: {str(e)}"
        )


@router.put("/sindicatos/{sindicato_id}", summary="Atualizar sindicato")
async def atualizar_sindicato(
    sindicato_id: int,
    dados: SindicatoUpdate,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Atualiza os dados de um sindicato"""
    try:
        # Remove campos None
        dados_atualizacao = {k: v for k, v in dados.dict().items() if v is not None}
        
        if not dados_atualizacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado fornecido para atualização"
            )
        
        resultado = cct_service.atualizar_sindicato(sindicato_id, dados_atualizacao)
        return {"status": "success", "data": resultado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar sindicato: {str(e)}"
        )


# Endpoints para Convenções Coletivas
@router.post("/", summary="Criar nova CCT")
async def criar_cct(
    cct: ConvencaoColetivaCreate,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Cria uma nova Convenção Coletiva de Trabalho (CCT)"""
    try:
        resultado = cct_service.criar_convencao_coletiva(cct.dict())
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar CCT: {str(e)}"
        )


@router.get("/", summary="Listar CCTs")
async def listar_ccts(
    skip: int = 0,
    limit: int = 100,
    union_id: Optional[int] = None,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Lista CCTs com filtros opcionais"""
    try:
        ccts = cct_service.listar_convencoes_coletivas(
            sindicato_id=union_id,
            limit=limit,
            offset=skip
        )
        return {"status": "success", "data": ccts}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar CCTs: {str(e)}"
        )


@router.get("/{cct_id}", summary="Obter CCT")
async def obter_cct(
    cct_id: int,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Obtém CCT específica com detalhes completos"""
    try:
        cct = cct_service.obter_convencao_coletiva(cct_id)
        if not cct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CCT não encontrada"
            )
        return {"status": "success", "data": cct}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter CCT: {str(e)}"
        )


@router.put("/{cct_id}", summary="Atualizar CCT")
async def atualizar_cct(
    cct_id: int,
    dados: ConvencaoColetivaUpdate,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Atualiza uma CCT existente"""
    try:
        # Remove campos None
        dados_atualizacao = {k: v for k, v in dados.dict().items() if v is not None}
        
        if not dados_atualizacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado fornecido para atualização"
            )
        
        resultado = cct_service.atualizar_convencao_coletiva(cct_id, dados_atualizacao)
        return {"status": "success", "data": resultado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar CCT: {str(e)}"
        )


# Endpoints auxiliares
@router.post("/empresas/{empresa_id}/sindicato/{sindicato_id}", summary="Associar empresa ao sindicato")
async def associar_empresa_sindicato(
    empresa_id: int,
    sindicato_id: int,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Associa uma empresa a um sindicato"""
    try:
        resultado = cct_service.associar_empresa_sindicato(empresa_id, sindicato_id)
        return {"status": "success", "data": resultado}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao associar empresa ao sindicato: {str(e)}"
        )


@router.get("/sindicatos/{sindicato_id}/empresas", summary="Listar empresas do sindicato")
async def listar_empresas_sindicato(
    sindicato_id: int,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Lista empresas associadas a um sindicato específico"""
    try:
        empresas = cct_service.listar_empresas_por_sindicato(sindicato_id)
        return {"status": "success", "data": empresas}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar empresas do sindicato: {str(e)}"
        )


# Manter compatibilidade com endpoints antigos (deprecated)
@router.get("/unions", summary="[DEPRECATED] Listar sindicatos", deprecated=True)
async def list_unions(cct_service: CCTService = Depends(get_cct_service)):
    """[DEPRECATED] Use /sindicatos instead"""
    try:
        sindicatos = cct_service.listar_sindicatos()
        return {"status": "success", "data": sindicatos}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar sindicatos: {str(e)}"
        )


@router.post("/{cct_id}/compare/{other_cct_id}", summary="Comparar CCTs")
async def compare_ccts(
    cct_id: int,
    other_cct_id: int,
    cct_service: CCTService = Depends(get_cct_service)
):
    """Compara duas CCTs (funcionalidade futura)"""
    # Esta funcionalidade será implementada numa versão futura
    return {
        "status": "not_implemented",
        "message": "Funcionalidade de comparação será implementada numa versão futura",
        "cct_id": cct_id,
        "other_cct_id": other_cct_id
    }
