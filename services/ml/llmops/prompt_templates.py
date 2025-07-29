from jinja2 import Template

SUMMARY_PROMPT = Template(
    """
Resumo da auditoria:
- Total de documentos: {{ total_docs }}
- Anomalias detectadas: {{ anomalies }}
- Viés estatístico: {{ bias_info }}
"""
)


def render_summary(total_docs, anomalies, bias_info):
    return SUMMARY_PROMPT.render(
        total_docs=total_docs, anomalies=anomalies, bias_info=bias_info
    )
