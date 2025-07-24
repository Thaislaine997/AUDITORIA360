# src/services/

Lógica de negócio e integrações externas.

## Recomendações
- Coloque funções de processamento, integração com APIs, regras de negócio
- Evite lógica de apresentação ou visual

## Exemplos

### Serviço de integração com API externa
```python
def consultar_cnpj(cnpj):
    import requests
    url = f"https://api.cnpjs.io/v1/{cnpj}"
    resp = requests.get(url)
    return resp.json()
```

### Serviço de processamento de folha
```python
def calcular_total_folha(funcionarios):
    return sum(f["salario"] for f in funcionarios)
```

## Boas práticas
- Separe serviços por domínio (ex: folha, demandas, IA)
- Documente parâmetros e retornos
- Mantenha exemplos de integração para facilitar testes
