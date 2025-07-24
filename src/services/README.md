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

## Exemplo de uso

```python
from .email_service import EmailService
service = EmailService()
service.send_email("joao@exemplo.com", "Assunto", "Mensagem")
```

## Onboarding rápido

1. Instale dependências: `pip install -r requirements.txt`
2. Importe o serviço desejado:

```python
from .email_service import EmailService
service = EmailService()
service.send_email("joao@exemplo.com", "Assunto", "Mensagem")
```

## Boas práticas
- Separe serviços por domínio (ex: folha, demandas, IA)
- Documente parâmetros e retornos
- Mantenha exemplos de integração para facilitar testes
