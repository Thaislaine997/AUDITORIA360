from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def gerar_dossie_pdf(destino, empresa, competencia, resultado_df):
    c = canvas.Canvas(destino, pagesize=A4)
    largura, altura = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, altura - 50, f"Dossiê de Auditoria - {empresa}")
    c.setFont("Helvetica", 12)
    c.drawString(40, altura - 70, f"Competência: {competencia}")
    c.drawString(40, altura - 90, f"Data de Geração: {datetime.today().strftime('%d/%m/%Y')}")

    y = altura - 130
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Verba")
    c.drawString(200, y, "Valor Pago")
    c.drawString(300, y, "Esperado")
    c.drawString(400, y, "Resultado")

    c.setFont("Helvetica", 10)
    y -= 20
    for _, row in resultado_df.iterrows():
        c.drawString(40, y, str(row.get("item", "")))
        c.drawString(200, y, str(row.get("pago", "")))
        c.drawString(300, y, str(row.get("esperado", "")))
        c.drawString(400, y, str(row.get("resultado", "")))
        y -= 15
        if y < 50:
            c.showPage()
            y = altura - 50

    c.save()
    return destino
