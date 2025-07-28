# Exemplo de dados para testes locais

Coloque aqui arquivos CSV ou Parquet para testar queries DuckDB localmente.

Exemplo de uso DuckDB em Python:

```python
import duckdb
import pandas as pd

df = pd.read_csv('data/input/exemplo.csv')
con = duckdb.connect(database=':memory:')
con.register('tabela', df)
resultado = con.execute('SELECT * FROM tabela LIMIT 10').fetchdf()
print(resultado)
```
