"""
Controller administrativo para CRUD de parâmetros legais históricos (INSS, IRRF, Salário Família, Salário Mínimo, FGTS).
"""
from src.utils import bq_utils

# Corrigido: inicialização exige project_id
bq = bq_utils.BigQueryUtils(project_id="auditoria-folha")

# INSS

def listar_inss():
    return bq.query("SELECT * FROM auditoria_folha_dataset.ParametrosINSSHistorico")

def criar_inss(parametro: dict):
    bq.insert_rows_json("auditoria_folha_dataset.ParametrosINSSHistorico", [parametro])
    return {"message": "Parâmetro INSS criado."}

def atualizar_inss(id_parametro_inss: str, parametro: dict):
    # Exemplo simples: update por id
    bq.run_query(f"""
        UPDATE auditoria_folha_dataset.ParametrosINSSHistorico
        SET descricao='{parametro.get('descricao','')}'
        WHERE id_parametro_inss='{id_parametro_inss}'
    """)
    return {"message": "Parâmetro INSS atualizado."}

def deletar_inss(id_parametro_inss: str):
    bq.run_query(f"DELETE FROM auditoria_folha_dataset.ParametrosINSSHistorico WHERE id_parametro_inss='{id_parametro_inss}'")
    return {"message": "Parâmetro INSS deletado."}

# (Repetir para IRRF, Salário Família, Salário Mínimo, FGTS)
