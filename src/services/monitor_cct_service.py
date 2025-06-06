# src/services/monitor_cct_service.py
"""
Serviço de monitoramento de sindicatos para detecção de novas CCTs.
Executar periodicamente via Cloud Scheduler + Cloud Function/Run.
"""
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Optional
from src.utils.bq_utils import BigQueryUtils
import uuid
import asyncio

# Configurações
GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET", "auditoria_folha_dataset")
TABLE_SINDICATOS = f"{GCP_PROJECT}.{BQ_DATASET}.SindicatosMonitorados"
TABLE_ALERTAS = f"{GCP_PROJECT}.{BQ_DATASET}.AlertasNovasCCTsEncontradas"

bq_utils = BigQueryUtils(project_id=GCP_PROJECT)

# Substituir fetch_sindicatos_monitorados para usar fetch_data
async def fetch_sindicatos_monitorados() -> List[dict]:
    sql = f"SELECT id_sindicato, cnpj_sindicato FROM `{TABLE_SINDICATOS}` WHERE ativo_para_monitoramento = TRUE"
    df = bq_utils.fetch_data(sql)
    return df.to_dict(orient='records')

# Função para gerar alerta apenas se não existir
async def verificar_e_gerar_alerta(
    id_sindicato: str,
    numero_registro: str,
    vigencia_inicio: str,
    fonte: str,
    sindicatos_partes: Optional[str] = None
):
    # Verificar existência de alerta semelhante
    check_sql = f"SELECT COUNT(1) AS cnt FROM `{TABLE_ALERTAS}` " \
                f"WHERE numero_registro_mte_detectado = '{numero_registro}' " \
                f"AND vigencia_inicio_detectada = '{vigencia_inicio}' " \
                f"AND status_alerta != 'DESCARTADO'"
    df_check = bq_utils.fetch_data(check_sql)
    if not df_check.empty and df_check.iloc[0]['cnt'] > 0:
        return  # alerta já existente

    alerta = {
        'id_alerta_cct': str(uuid.uuid4()),
        'id_sindicato_monitorado_fk': id_sindicato,
        'numero_registro_mte_detectado': numero_registro,
        'sindicatos_partes_detectados': sindicatos_partes,
        'vigencia_inicio_detectada': vigencia_inicio,
        'fonte_deteccao': fonte,
        'status_alerta': 'NOVO',
        'data_deteccao': datetime.now().isoformat()
    }
    bq_utils.insert_rows_json(TABLE_ALERTAS, [alerta])

# Implementação de scraping detalhado
async def monitorar_novas_ccts():
    sindicatos = await fetch_sindicatos_monitorados()
    for sind in sindicatos:
        cnpj = sind.get('cnpj_sindicato')
        id_sind = sind.get('id_sindicato')
        if not cnpj or not id_sind:
            continue  # sem dados essenciais, pula
        url = f"http://www3.mte.gov.br/sistemas/mediador/ConsultarInstColetivo?cnpj={cnpj}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Supondo que a tabela de resultados tenha id 'tblResultados'
        table = soup.find('table', id='tblResultados') or soup.find('table')  # type: ignore
        if not table:
            continue
        # Garante que 'table' é realmente uma Tag do BeautifulSoup
        from bs4 import Tag
        if not isinstance(table, Tag):
            continue
        rows = table.find_all('tr')
        for tr in rows[1:]:
            if not isinstance(tr, Tag):
                continue
            cols = tr.find_all(['th','td'])
            if len(cols) < 3:
                continue
            numero = cols[0].get_text(strip=True)
            data_inicio = cols[1].get_text(strip=True)
            link = None
            # Busca manualmente por uma tag <a> apenas se for Tag e tenta acessar .find('a') só se for Tag
            if type(cols[2]).__name__ == 'Tag':
                a_tag = getattr(cols[2], 'find', lambda *a, **kw: None)('a')
                if a_tag and type(a_tag).__name__ == 'Tag' and getattr(a_tag, 'has_attr', lambda x: False)('href'):
                    link = a_tag['href']
            partes = cols[3].get_text(strip=True) if len(cols) > 3 and type(cols[3]).__name__ == 'Tag' else None
            await verificar_e_gerar_alerta(
                id_sind,
                numero,
                data_inicio,
                url,
                sindicatos_partes=partes
            )

if __name__ == '__main__':
    import asyncio; asyncio.run(monitorar_novas_ccts())
