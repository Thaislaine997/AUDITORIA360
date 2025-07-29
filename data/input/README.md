# 🧪 Sample Input Data - TEST FILES ONLY

> ⚠️  **WARNING: THESE ARE SAMPLE FILES FOR TESTING PURPOSES ONLY**
> 
> ⚠️  **DO NOT USE IN PRODUCTION ENVIRONMENTS**
> 
> ⚠️  **These files contain fake/test data for development and demonstration**

## 📂 Sample Files

- `sample_extrato.pdf` - **SAMPLE FILE** - Test document for OCR processing

## 🚫 Production Usage

**DO NOT** use these files in production:

- These are test/sample files with fake data
- Real production data should come from your actual systems
- Upload real documents through the application interface
- Follow security guidelines for handling sensitive documents

## 🔧 Purpose

These sample files are used for:

- **Development**: Testing document processing functionality
- **OCR Testing**: Validating OCR accuracy and processing
- **Demo**: Showing example document formats
- **Documentation**: Providing examples for integration guides

## 📖 For Production

In production environments:

1. Users upload real documents through the web interface
2. Documents are stored securely in configured cloud storage
3. Real documents are processed with OCR and validation
4. Follow data privacy and security guidelines for document handling

**Remember**: These are sample files for testing only!

---

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
