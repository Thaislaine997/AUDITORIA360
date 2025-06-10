from fastapi import APIRouter, HTTPException, Path, Depends, Request
from fastapi.responses import StreamingResponse
from google.cloud import bigquery
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from src.utils.config_manager import config_manager # Corrigido o caminho do import
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
import bq_loader

def get_current_config(request: Request):
    return config_manager.get_config(request)

class AuditoriaErroDetalhe(BaseModel):
    id_erro: Optional[str]
    nome_clausula_auditada: Optional[str]
    campo_auditado_folha: Optional[str]
    valor_encontrado_folha: Optional[str]
    valor_esperado_calculado: Optional[str]
    diferenca: Optional[str]
    detalhe_erro: Optional[str]
    severidade: Optional[str]

class AuditoriaDetalhe(BaseModel):
    id_folha: Optional[str]
    mes_ano_folha: Optional[str]
    status_folha: Optional[str]
    data_envio_cliente_folha: Optional[str]
    observacoes_folha: Optional[str]
    id_empresa: Optional[str]
    nome_empresa: Optional[str]
    cnpj_empresa_folha: Optional[str]
    id_contabilidade: Optional[str]
    nome_contabilidade: Optional[str]
    id_sindicato: Optional[str]
    nome_sindicato: Optional[str]
    erros_auditoria: Optional[List[AuditoriaErroDetalhe]]

router = APIRouter(
    prefix="/api/v1/auditorias",
    tags=["relatorios"],
)

def generate_pdf_content(auditoria_data: AuditoriaDetalhe) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    # Estilo do Título
    style_title = styles["h1"]
    style_title.alignment = TA_CENTER
    style_title.fontSize = 18
    story.append(Paragraph("Relatório de Auditoria", style_title))
    story.append(Spacer(1, 24))

    # Estilo do Subtítulo e Corpo
    style_h2 = styles["h2"]
    style_h2.fontSize = 14
    style_body = styles["Normal"]
    style_body.fontSize = 10
    style_body_bold = styles["Normal"]
    style_body_bold.fontName = 'Helvetica-Bold'
    style_body_bold.fontSize = 10

    # Informações da Auditoria
    story.append(Paragraph("Detalhes da Auditoria", style_h2))
    story.append(Spacer(1, 12))

    info_data = [
        [Paragraph("ID da Folha:", style_body_bold), Paragraph(str(auditoria_data.id_folha), style_body)],
        [Paragraph("Empresa:", style_body_bold), Paragraph(auditoria_data.nome_empresa or "N/A", style_body)],
        [Paragraph("CNPJ:", style_body_bold), Paragraph(auditoria_data.cnpj_empresa_folha or "N/A", style_body)],
        [Paragraph("Mês/Ano Folha:", style_body_bold), Paragraph(auditoria_data.mes_ano_folha or "N/A", style_body)],
        [Paragraph("Status:", style_body_bold), Paragraph(auditoria_data.status_folha or "N/A", style_body)],
        [Paragraph("Contabilidade:", style_body_bold), Paragraph(f"{auditoria_data.nome_contabilidade or 'N/A'} (ID: {auditoria_data.id_contabilidade or 'N/A'})", style_body)],
        [Paragraph("Sindicato:", style_body_bold), Paragraph(f"{auditoria_data.nome_sindicato or 'N/A'} (ID: {auditoria_data.id_sindicato or 'N/A'})", style_body)],
        [Paragraph("Data Envio Cliente:", style_body_bold), Paragraph(str(auditoria_data.data_envio_cliente_folha) if auditoria_data.data_envio_cliente_folha else "N/A", style_body)],
        [Paragraph("Observações:", style_body_bold), Paragraph(auditoria_data.observacoes_folha or "N/A", style_body)],
    ]
    info_table = Table(info_data, colWidths=[120, None])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 24))

    # Pendências da Auditoria
    story.append(Paragraph("Pendências da Auditoria", style_h2))
    story.append(Spacer(1, 12))

    if auditoria_data.erros_auditoria:
        story.append(Paragraph(f"Total de Pendências Encontradas: {len(auditoria_data.erros_auditoria)}", style_body_bold))
        story.append(Spacer(1, 12))

        for i, erro in enumerate(auditoria_data.erros_auditoria):
            get = erro.get if isinstance(erro, dict) else lambda k, default=None: getattr(erro, k, default)
            story.append(Paragraph(f"Pendência {i+1}", styles["h3"]))
            erro_data = [
                [Paragraph("ID Erro:", style_body_bold), Paragraph(str(get("id_erro")), style_body)],
                [Paragraph("Cláusula Auditada:", style_body_bold), Paragraph(get("nome_clausula_auditada") or "N/A", style_body)],
                [Paragraph("Campo Auditado:", style_body_bold), Paragraph(get("campo_auditado_folha") or "N/A", style_body)],
                [Paragraph("Valor Encontrado:", style_body_bold), Paragraph(str(get("valor_encontrado_folha")) if get("valor_encontrado_folha") is not None else "N/A", style_body)],
                [Paragraph("Valor Esperado:", style_body_bold), Paragraph(str(get("valor_esperado_calculado")) if get("valor_esperado_calculado") is not None else "N/A", style_body)],
                [Paragraph("Diferença:", style_body_bold), Paragraph(str(get("diferenca")) if get("diferenca") is not None else "N/A", style_body)],
                [Paragraph("Detalhe:", style_body_bold), Paragraph(get("detalhe_erro") or "N/A", style_body)],
                [Paragraph("Severidade:", style_body_bold), Paragraph(get("severidade") or "N/A", style_body)],
            ]
            erro_table = Table(erro_data, colWidths=[120, None])
            erro_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(erro_table)
            story.append(Spacer(1, 12))
    else:
        story.append(Paragraph("Tudo OK! Nenhuma pendência encontrada nesta auditoria.", style_body))

    doc.build(story)
    buffer.seek(0)
    return buffer

@router.get("/{id_folha}/pdf", response_class=StreamingResponse)
async def gerar_relatorio_pdf(
    request: Request,
    id_folha: str = Path(..., title="ID da Folha", description="O ID da folha para gerar o relatório."),
    config: dict = Depends(get_current_config)
):
    project_id = config.get("gcp_project_id")
    bq_dataset_id = config.get("control_bq_dataset_id")
    if not project_id or not bq_dataset_id:
        raise HTTPException(status_code=500, detail="Configuração do projeto BigQuery ausente.")
    client = src.bq_loader.get_bigquery_client(config)

    query = f"""
    WITH ErrosAgregados AS (
        SELECT
            id_folha,
            ARRAY_AGG(
                STRUCT(
                    id_erro,
                    nome_clausula_auditada,
                    campo_auditado_folha,
                    valor_encontrado_folha,
                    valor_esperado_calculado,
                    diferenca,
                    detalhe_erro,
                    severidade
                ) ORDER BY id_erro
            ) AS erros_auditoria
        FROM `{project_id}.{bq_dataset_id}.auditoria_erros`
        WHERE id_folha = @id_folha
        GROUP BY id_folha
    )
    SELECT
        f.id_folha,
        f.mes_ano AS mes_ano_folha,
        f.status AS status_folha,
        f.data_envio_cliente AS data_envio_cliente_folha,
        f.observacoes AS observacoes_folha,
        f.id_empresa,
        e.nome AS nome_empresa,
        e.cnpj AS cnpj_empresa_folha,
        f.id_contabilidade,
        c.nome AS nome_contabilidade,
        f.id_sindicato,
        s.nome AS nome_sindicato,
        ea.erros_auditoria
    FROM `{project_id}.{bq_dataset_id}.folhas` f
    LEFT JOIN `{project_id}.{bq_dataset_id}.empresas` e ON f.id_empresa = e.id_empresa
    LEFT JOIN `{project_id}.{bq_dataset_id}.contabilidades` c ON f.id_contabilidade = c.id_contabilidade
    LEFT JOIN `{project_id}.{bq_dataset_id}.sindicatos` s ON f.id_sindicato = s.id_sindicato
    LEFT JOIN ErrosAgregados ea ON f.id_folha = ea.id_folha
    WHERE f.id_folha = @id_folha
    LIMIT 1
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
        ]
    )

    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        auditoria_raw = None
        for row in results:
            auditoria_raw = dict(row)
            break
        
        if not auditoria_raw:
            raise HTTPException(status_code=404, detail=f"Auditoria com ID {id_folha} não encontrada.")

        # Transformar os erros em objetos AuditoriaErroDetalhe se existirem
        erros_list = []
        if auditoria_raw.get("erros_auditoria"):
            for erro_dict in auditoria_raw["erros_auditoria"]:
                erros_list.append(AuditoriaErroDetalhe(**erro_dict))
        
        auditoria_data = AuditoriaDetalhe(
            id_folha=auditoria_raw.get("id_folha"),
            mes_ano_folha=auditoria_raw.get("mes_ano_folha"),
            status_folha=auditoria_raw.get("status_folha"),
            data_envio_cliente_folha=auditoria_raw.get("data_envio_cliente_folha"),
            observacoes_folha=auditoria_raw.get("observacoes_folha"),
            id_empresa=auditoria_raw.get("id_empresa"),
            nome_empresa=auditoria_raw.get("nome_empresa"),
            cnpj_empresa_folha=auditoria_raw.get("cnpj_empresa_folha"),
            id_contabilidade=auditoria_raw.get("id_contabilidade"),
            nome_contabilidade=auditoria_raw.get("nome_contabilidade"),
            id_sindicato=auditoria_raw.get("id_sindicato"),
            nome_sindicato=auditoria_raw.get("nome_sindicato"),
            erros_auditoria=erros_list
        )

        pdf_buffer = generate_pdf_content(auditoria_data)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=relatorio_auditoria_{id_folha}.pdf"}
        )

    except Exception as e:
        # Logar o erro e retornar um erro HTTP apropriado
        print(f"Erro ao gerar PDF para auditoria {id_folha}: {e}") # Idealmente, usar um logger
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar relatório PDF: {str(e)}")

@router.get("/exemplo", response_model=None)
async def exemplo(request: Request):
    ...

