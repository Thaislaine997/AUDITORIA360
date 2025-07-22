from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Optional
from datetime import date
from src.schemas.cct_schemas import (
    CCTDocumentoCreateRequest,
    CCTDocumentoResponse,
    AlertaCCTResponse,
    UpdateAlertaStatusRequest
)
from src_legacy_backup.controllers.cct_controller import (
    salvar_documento_cct_e_metadados,
    listar_ccts,
    atualizar_metadata_cct,
    desativar_cct,
    listar_alertas,
    atualizar_status_alerta
)

router = APIRouter(prefix="/api/v1/ccts", tags=["CCTs"])

@router.post("/upload", response_model=CCTDocumentoResponse)
async def upload_cct_documento(
    nome_documento_original: str = Form(...),
    data_inicio_vigencia_cct: date = Form(...),
    data_fim_vigencia_cct: Optional[date] = Form(None),
    sindicatos_laborais_json_str: Optional[str] = Form(None),
    sindicatos_patronais_json_str: Optional[str] = Form(None),
    numero_registro_mte: Optional[str] = Form(None),
    link_fonte_oficial: Optional[str] = Form(None),
    id_cct_base_fk: Optional[str] = Form(None),
    id_cliente_principal_associado: Optional[str] = Form(None),
    ids_clientes_afetados_lista_str: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    # Validação de tipo de arquivo
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=422, detail="Tipo de arquivo não suportado. Envie PDF ou DOCX.")
    try:
        result = await salvar_documento_cct_e_metadados(
            file=file,
            nome_documento_original=nome_documento_original,
            data_inicio_vigencia=data_inicio_vigencia_cct,
            data_fim_vigencia=data_fim_vigencia_cct,
            sindicatos_laborais_json_str=sindicatos_laborais_json_str,
            sindicatos_patronais_json_str=sindicatos_patronais_json_str,
            numero_registro_mte=numero_registro_mte,
            link_fonte_oficial=link_fonte_oficial,
            id_cct_base_fk=id_cct_base_fk,
            id_cliente_principal=id_cliente_principal_associado,
            ids_clientes_afetados=ids_clientes_afetados_lista_str
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[CCTDocumentoResponse])
async def get_ccts(
    id_cliente_afetado: Optional[str] = None,
    sindicato_nome_contem: Optional[str] = None,
    data_vigencia_em: Optional[date] = None
):
    return await listar_ccts(
        id_cliente_afetado=id_cliente_afetado,
        sindicato_nome_contem=sindicato_nome_contem,
        data_vigencia_em=data_vigencia_em
    )

@router.put("/{id_cct}", response_model=CCTDocumentoResponse)
async def update_cct_metadata(id_cct: str, payload: CCTDocumentoCreateRequest):
    return await atualizar_metadata_cct(id_cct, payload)

@router.delete("/{id_cct}")
async def delete_cct(id_cct: str):
    await desativar_cct(id_cct)
    return {"status": "ok", "id_cct": id_cct}

@router.get("/alerts", response_model=List[AlertaCCTResponse])
async def get_alertas(
    status: Optional[str] = None
):
    """Listar alertas de novas CCTs, opcionalmente filtrando por status."""
    return await listar_alertas(status=status)

@router.put("/alerts/{id_alerta}", response_model=AlertaCCTResponse)
async def update_alerta_status(
    id_alerta: str,
    payload: UpdateAlertaStatusRequest
):
    """Atualizar status e notas de um alerta de CCT."""
    return await atualizar_status_alerta(id_alerta, payload)