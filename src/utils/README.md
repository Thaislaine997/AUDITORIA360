# 🛠️ AUDITORIA360 - Utilitários e Helpers

> **🔧 Ferramentas auxiliares** com funções reutilizáveis para todo o sistema AUDITORIA360

Este módulo centraliza todas as funções utilitárias, helpers e ferramentas auxiliares que são utilizadas em diferentes partes do sistema, promovendo reutilização e consistência.

## 🏗️ **ESTRUTURA DOS UTILITÁRIOS**

### 📋 **Organização dos Módulos**
```
src/utils/
├── 📅 date_utils.py          # Manipulação de datas
├── 🔢 validation_utils.py    # Validações comuns
├── 🔐 crypto_utils.py        # Criptografia e segurança
├── 📄 file_utils.py          # Manipulação de arquivos
├── 🌐 api_integration.py     # Integrações com APIs
├── 📊 monitoring.py          # Monitoramento e métricas
├── ⚡ performance.py         # Otimizações de performance
├── 📝 text_utils.py          # Processamento de texto
├── 💰 financial_utils.py     # Cálculos financeiros
└── 🔧 general_utils.py       # Utilitários gerais
```

## 📅 **Date Utils** - Manipulação de Datas

### 🕒 **Funções de Data e Hora**
```python
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

def get_current_timestamp():
    """Retorna timestamp atual UTC"""
    return datetime.now(timezone.utc)

def format_brazilian_date(date_obj: datetime) -> str:
    """Formata data no padrão brasileiro"""
    return date_obj.strftime('%d/%m/%Y')

def format_competency(year: int, month: int) -> str:
    """Formata competência no formato YYYY-MM"""
    return f"{year:04d}-{month:02d}"

def get_month_range(competency: str) -> tuple:
    """Retorna primeiro e último dia do mês da competência"""
    year, month = map(int, competency.split('-'))
    start_date = datetime(year, month, 1)
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
    return start_date, end_date

def calculate_working_days(start_date: datetime, end_date: datetime) -> int:
    """Calcula dias úteis entre duas datas"""
    # Implementação considerando feriados brasileiros
    pass
```

### 📊 **Exemplo de Uso**
```python
from src.utils.date_utils import format_competency, get_month_range

# Formatar competência
competencia = format_competency(2025, 1)  # "2025-01"

# Obter range do mês
inicio, fim = get_month_range("2025-01")
print(f"Período: {inicio} até {fim}")
```

## 🔢 **Validation Utils** - Validações

### ✅ **Validações Brasileiras**
```python
import re
from typing import Optional

def validate_cpf(cpf: str) -> bool:
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return cpf[-2:] == f"{digito1}{digito2}"

def validate_cnpj(cnpj: str) -> bool:
    """Valida CNPJ brasileiro"""
    # Implementação similar ao CPF
    pass

def validate_pis(pis: str) -> bool:
    """Valida PIS/PASEP"""
    # Implementação da validação PIS
    pass

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

### 📊 **Exemplo de Uso**
```python
from src.utils.validation_utils import validate_cpf, validate_cnpj

# Validar CPF
cpf_valido = validate_cpf("123.456.789-09")
print(f"CPF válido: {cpf_valido}")

# Validar CNPJ
cnpj_valido = validate_cnpj("12.345.678/0001-95")
print(f"CNPJ válido: {cnpj_valido}")
```

## 🔐 **Crypto Utils** - Criptografia

### 🛡️ **Funções de Segurança**
```python
import hashlib
import secrets
from cryptography.fernet import Fernet
from passlib.context import CryptContext

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera hash seguro da senha"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha contra hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_token(length: int = 32) -> str:
    """Gera token aleatório seguro"""
    return secrets.token_urlsafe(length)

def encrypt_sensitive_data(data: str, key: bytes) -> str:
    """Criptografa dados sensíveis"""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data: str, key: bytes) -> str:
    """Descriptografa dados sensíveis"""
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

def generate_encryption_key() -> bytes:
    """Gera chave de criptografia"""
    return Fernet.generate_key()
```

## 📄 **File Utils** - Manipulação de Arquivos

### 📁 **Processamento de Arquivos**
```python
import os
import mimetypes
from pathlib import Path
from typing import List, Optional

def get_file_extension(filename: str) -> str:
    """Retorna extensão do arquivo"""
    return Path(filename).suffix.lower()

def is_allowed_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Verifica se tipo de arquivo é permitido"""
    extension = get_file_extension(filename)
    return extension in allowed_types

def get_file_size_mb(file_path: str) -> float:
    """Retorna tamanho do arquivo em MB"""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def sanitize_filename(filename: str) -> str:
    """Sanitiza nome do arquivo"""
    import re
    # Remove caracteres perigosos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limita tamanho
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename

def read_file_chunks(file_path: str, chunk_size: int = 8192):
    """Lê arquivo em chunks para economizar memória"""
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk
```

## 💰 **Financial Utils** - Cálculos Financeiros

### 💵 **Cálculos Trabalhistas**
```python
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import Dict, Optional

def calculate_inss(salary: Decimal, year: int) -> Decimal:
    """Calcula desconto de INSS"""
    # Tabelas atualizadas por ano
    inss_tables = {
        2025: [
            (Decimal('1412.00'), Decimal('0.075')),
            (Decimal('2666.68'), Decimal('0.09')),
            (Decimal('4000.03'), Decimal('0.12')),
            (Decimal('7786.02'), Decimal('0.14')),
        ]
    }
    
    table = inss_tables.get(year, inss_tables[2025])
    
    total_inss = Decimal('0')
    previous_limit = Decimal('0')
    
    for limit, rate in table:
        if salary <= previous_limit:
            break
        
        taxable_amount = min(salary, limit) - previous_limit
        total_inss += taxable_amount * rate
        previous_limit = limit
    
    return total_inss.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calculate_irrf(salary: Decimal, dependents: int, year: int) -> Decimal:
    """Calcula desconto de IRRF"""
    # Implementação das tabelas de IRRF
    pass

def calculate_fgts(salary: Decimal) -> Decimal:
    """Calcula FGTS (8% do salário)"""
    return (salary * Decimal('0.08')).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )

def calculate_vacation_pay(salary: Decimal, days: int) -> Decimal:
    """Calcula valor das férias"""
    daily_salary = salary / Decimal('30')
    vacation_pay = daily_salary * Decimal(str(days))
    # Adiciona 1/3 constitucional
    vacation_bonus = vacation_pay / Decimal('3')
    return (vacation_pay + vacation_bonus).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
```

## 📊 **Performance Utils** - Otimização

### ⚡ **Ferramentas de Performance**
```python
import time
import functools
from typing import Any, Callable

def timer_decorator(func: Callable) -> Callable:
    """Decorator para medir tempo de execução"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executou em {end_time - start_time:.4f}s")
        return result
    return wrapper

def cache_result(ttl: int = 3600):
    """Decorator para cache de resultados"""
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            
            if key in cache:
                cached_result, timestamp = cache[key]
                if current_time - timestamp < ttl:
                    return cached_result
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        return wrapper
    return decorator

def batch_process(items: list, batch_size: int = 100, callback: Callable = None):
    """Processa lista em lotes para otimizar memória"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        if callback:
            callback(batch)
        yield batch
```

## 🌐 **API Integration Utils** - Integrações

### 🔌 **Helpers para APIs**
```python
import requests
from typing import Dict, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    """Cliente HTTP com retry automático"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = self._create_session()
    
    def _create_session(self):
        session = requests.Session()
        
        # Configurar retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get(self, endpoint: str, params: Dict = None) -> Dict:
        """GET request with error handling"""
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIIntegrationError(f"API request failed: {e}")
    
    def post(self, endpoint: str, data: Dict = None) -> Dict:
        """POST request with error handling"""
        # Implementação similar ao GET
        pass
```

## 🧪 **TESTES DE UTILITÁRIOS**

### 📊 **Exemplos de Testes**
```python
import pytest
from decimal import Decimal
from src.utils.validation_utils import validate_cpf
from src.utils.financial_utils import calculate_inss

class TestValidationUtils:
    def test_validate_cpf_valid(self):
        """Testa validação de CPF válido"""
        assert validate_cpf("123.456.789-09") == True
    
    def test_validate_cpf_invalid(self):
        """Testa validação de CPF inválido"""
        assert validate_cpf("111.111.111-11") == False

class TestFinancialUtils:
    def test_calculate_inss(self):
        """Testa cálculo de INSS"""
        salary = Decimal('3000.00')
        inss = calculate_inss(salary, 2025)
        
        assert isinstance(inss, Decimal)
        assert inss > Decimal('0')
        assert inss < salary

    def test_calculate_fgts(self):
        """Testa cálculo de FGTS"""
        from src.utils.financial_utils import calculate_fgts
        
        salary = Decimal('5000.00')
        fgts = calculate_fgts(salary)
        
        expected = Decimal('400.00')  # 8% de 5000
        assert fgts == expected
```

## 📖 **DOCUMENTAÇÃO ADICIONAL**

### 🔗 **Links Relacionados**
- **[🏗️ Arquitetura](../../docs/tecnico/arquitetura/visao-geral.md)** - Visão geral do sistema
- **[📊 Modelos](../models/README.md)** - Estrutura de dados
- **[🔧 Serviços](../services/README.md)** - Lógica de negócio
- **[🧪 Testes](../../docs/qualidade/estrategia-testes.md)** - Estratégia de testes

### 📚 **Boas Práticas**
1. **Reutilização**: Mantenha funções genéricas e reutilizáveis
2. **Documentação**: Documente claramente parâmetros e retornos
3. **Type Hints**: Use tipagem para maior clareza
4. **Error Handling**: Trate erros de forma consistente
5. **Performance**: Otimize funções que são chamadas frequentemente
6. **Testing**: Mantenha alta cobertura de testes
7. **Dependencies**: Minimize dependências externas

---

> **💡 Dica**: Os utilitários devem ser independentes e não ter dependências de outros módulos do sistema, exceto configurações básicas.

**Última atualização**: Janeiro 2025 | **Status**: Documentação Atualizada
