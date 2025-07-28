import duckdb
import pandas as pd

def analisar_folha(dataframe_folha: pd.DataFrame) -> pd.DataFrame:
    con = duckdb.connect(database=':memory:')
    con.register('folha_tbl', dataframe_folha)
    resultado_df = con.execute("""
        SELECT
            departamento,
            AVG(salario_bruto) as media_salarial,
            COUNT(DISTINCT id_funcionario) as total_funcionarios
        FROM folha_tbl
        GROUP BY departamento
        ORDER BY media_salarial DESC
    """).fetchdf()
    con.close()
    return resultado_df
