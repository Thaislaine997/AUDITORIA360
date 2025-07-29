from weasyprint import HTML


def generate_pdf_report(html_content: str, output_path: str):
    HTML(string=html_content).write_pdf(output_path)
