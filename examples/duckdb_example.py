"""
Exemplo de uso do DuckDB com Pandas.
Requer: duckdb, pandas
"""
import duckdb
import pandas as pd

def main():
    # Exemplo: cria um DataFrame
    df = pd.DataFrame({
        'departamento': ['RH', 'TI', 'TI', 'RH'],
        'salario_bruto': [3000, 5000, 7000, 3500],
        'id_funcionario': [1, 2, 3, 4]
    })
    con = duckdb.connect(database=':memory:')
    con.register('folha_tbl', df)
    resultado_df = con.execute('''
        SELECT departamento, AVG(salario_bruto) as media_salarial, COUNT(DISTINCT id_funcionario) as total_funcionarios
        FROM folha_tbl
        GROUP BY departamento
        ORDER BY media_salarial DESC
    ''').fetchdf()
    print(resultado_df)
    con.close()

if __name__ == "__main__":
    main()
