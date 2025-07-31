# 📏 Padrões de Código - AUDITORIA360

## 🎯 Objetivo

Este documento estabelece os padrões de codificação para manter consistência, legibilidade e qualidade do código na AUDITORIA360.

## 🐍 Padrões Python (Backend)

### Formatação e Estilo

#### Formatador: Black
```bash
# Instalar
pip install black

# Formatar arquivo
black arquivo.py

# Formatar projeto
black src/

# Verificar sem modificar
black --check src/
```

#### Linter: Flake8
```bash
# Configuração em .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = migrations, venv
```

#### Import Sorting: isort
```bash
# Instalar
pip install isort

# Configuração em pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
```

### Convenções de Nomenclatura

```python
# ✅ Classes - PascalCase
class ClienteService:
    pass

# ✅ Funções e variáveis - snake_case
def calcular_folha_pagamento():
    valor_total = 0
    
# ✅ Constantes - UPPER_SNAKE_CASE
MAX_TENTATIVAS_LOGIN = 3
DATABASE_URL = "postgresql://..."

# ✅ Métodos privados - _snake_case
def _validar_dados_internos(self):
    pass

# ✅ Atributos privados - _snake_case
class Usuario:
    def __init__(self):
        self._senha_hash = None
```

### Estrutura de Código

#### Organização de Imports
```python
# 1. Bibliotecas padrão
import os
import sys
from datetime import datetime

# 2. Bibliotecas de terceiros
import pandas as pd
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# 3. Imports locais
from src.models.user import User
from src.services.auth import AuthService
from src.utils.helpers import format_currency
```

#### Docstrings
```python
def calcular_imposto(valor_bruto: float, aliquota: float) -> float:
    """
    Calcula o valor do imposto baseado no valor bruto e alíquota.
    
    Args:
        valor_bruto (float): Valor bruto para cálculo
        aliquota (float): Alíquota do imposto (0.0 a 1.0)
    
    Returns:
        float: Valor do imposto calculado
        
    Raises:
        ValueError: Se alíquota estiver fora do range válido
        
    Examples:
        >>> calcular_imposto(1000.0, 0.15)
        150.0
    """
    if not 0.0 <= aliquota <= 1.0:
        raise ValueError("Alíquota deve estar entre 0.0 e 1.0")
    
    return valor_bruto * aliquota
```

#### Type Hints
```python
from typing import List, Dict, Optional, Union
from pydantic import BaseModel

# ✅ Sempre usar type hints
def processar_folha(
    funcionarios: List[Dict[str, Union[str, float]]],
    mes_referencia: str,
    aplicar_bonus: bool = False
) -> Dict[str, float]:
    """Processa folha de pagamento."""
    pass

# ✅ Classes com tipos explícitos
class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    salario: float
    departamento: Optional[str] = None
    ativo: bool = True
```

### Tratamento de Erros

```python
# ✅ Exceções específicas
class FolhaPagamentoError(Exception):
    """Erro base para operações de folha de pagamento."""
    pass

class SalarioInvalidoError(FolhaPagamentoError):
    """Erro quando salário está inválido."""
    pass

# ✅ Uso adequado de try/except
def processar_pagamento(funcionario_id: int) -> bool:
    try:
        funcionario = get_funcionario(funcionario_id)
        calcular_salario(funcionario)
        return True
    except FuncionarioNotFoundError:
        logger.warning(f"Funcionário {funcionario_id} não encontrado")
        return False
    except SalarioInvalidoError as e:
        logger.error(f"Salário inválido para {funcionario_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise ProcessamentoError(f"Falha ao processar {funcionario_id}")
```

## ⚛️ Padrões React/TypeScript (Frontend)

### Formatação e Linting

#### ESLint Configuration
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "react-hooks/recommended"
  ],
  "rules": {
    "react-hooks/exhaustive-deps": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "prefer-const": "error"
  }
}
```

#### Prettier Configuration
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### Convenções React

#### Componentes Funcionais
```tsx
// ✅ Componente funcional com tipos
interface FuncionarioCardProps {
  funcionario: Funcionario;
  onEdit: (id: number) => void;
  className?: string;
}

export const FuncionarioCard: React.FC<FuncionarioCardProps> = ({
  funcionario,
  onEdit,
  className = '',
}) => {
  const [loading, setLoading] = useState(false);

  const handleEdit = useCallback(() => {
    onEdit(funcionario.id);
  }, [funcionario.id, onEdit]);

  return (
    <Card className={`funcionario-card ${className}`}>
      <CardContent>
        <Typography variant="h6">{funcionario.nome}</Typography>
        <Button onClick={handleEdit} disabled={loading}>
          Editar
        </Button>
      </CardContent>
    </Card>
  );
};
```

#### Custom Hooks
```tsx
// ✅ Hook customizado
interface UseFuncionariosReturn {
  funcionarios: Funcionario[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export const useFuncionarios = (): UseFuncionariosReturn => {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFuncionarios = useCallback(async () => {
    try {
      setLoading(true);
      const data = await api.getFuncionarios();
      setFuncionarios(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFuncionarios();
  }, [fetchFuncionarios]);

  return {
    funcionarios,
    loading,
    error,
    refetch: fetchFuncionarios,
  };
};
```

### Estrutura de Arquivos

```
src/
├── components/
│   ├── ui/                    # Componentes base reutilizáveis
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   └── Card/
│   └── features/              # Componentes específicos de funcionalidade
│       ├── auth/
│       ├── dashboard/
│       └── funcionarios/
├── hooks/                     # Custom hooks
├── services/                  # Camada de API
├── stores/                    # Gerenciamento de estado (Zustand)
├── types/                     # Definições de tipos TypeScript
└── utils/                     # Funções utilitárias
```

## 🧪 Padrões de Teste

### Testes Python (Pytest)

```python
# test_funcionario_service.py
import pytest
from unittest.mock import Mock, patch
from src.services.funcionario_service import FuncionarioService
from src.models.funcionario import Funcionario

class TestFuncionarioService:
    """Testes para FuncionarioService."""
    
    @pytest.fixture
    def funcionario_service(self):
        """Fixture para serviço de funcionário."""
        return FuncionarioService()
    
    @pytest.fixture
    def funcionario_sample(self):
        """Fixture para funcionário de exemplo."""
        return Funcionario(
            id=1,
            nome="João Silva",
            salario=5000.0,
            departamento="TI"
        )
    
    def test_calcular_salario_liquido_success(
        self, funcionario_service, funcionario_sample
    ):
        """Testa cálculo de salário líquido com sucesso."""
        # Arrange
        desconto_esperado = 500.0
        salario_liquido_esperado = 4500.0
        
        # Act
        resultado = funcionario_service.calcular_salario_liquido(funcionario_sample)
        
        # Assert
        assert resultado == salario_liquido_esperado
        assert funcionario_sample.salario == 5000.0  # Não deve modificar original
    
    @patch('src.services.funcionario_service.CalculadoraImposto')
    def test_calcular_salario_com_mock(
        self, mock_calculadora, funcionario_service, funcionario_sample
    ):
        """Testa cálculo com dependência mockada."""
        # Arrange
        mock_calculadora.return_value.calcular.return_value = 300.0
        
        # Act
        resultado = funcionario_service.calcular_salario_liquido(funcionario_sample)
        
        # Assert
        assert resultado == 4700.0
        mock_calculadora.return_value.calcular.assert_called_once()
```

### Testes React (Jest + Testing Library)

```tsx
// FuncionarioCard.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FuncionarioCard } from './FuncionarioCard';
import { Funcionario } from '../types/funcionario';

const mockFuncionario: Funcionario = {
  id: 1,
  nome: 'João Silva',
  salario: 5000,
  departamento: 'TI',
};

const mockOnEdit = jest.fn();

describe('FuncionarioCard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('deve renderizar informações do funcionário', () => {
    render(
      <FuncionarioCard funcionario={mockFuncionario} onEdit={mockOnEdit} />
    );

    expect(screen.getByText('João Silva')).toBeInTheDocument();
    expect(screen.getByText('TI')).toBeInTheDocument();
  });

  it('deve chamar onEdit quando botão for clicado', async () => {
    render(
      <FuncionarioCard funcionario={mockFuncionario} onEdit={mockOnEdit} />
    );

    const editButton = screen.getByRole('button', { name: /editar/i });
    fireEvent.click(editButton);

    await waitFor(() => {
      expect(mockOnEdit).toHaveBeenCalledWith(1);
    });
  });
});
```

## 📝 Commits e Versionamento

### Conventional Commits
```bash
# Formato: tipo(escopo): descrição

# Exemplos:
feat(auth): adicionar autenticação por token JWT
fix(api): corrigir validação de CPF
docs(readme): atualizar instruções de instalação
refactor(frontend): reorganizar componentes de UI
test(api): adicionar testes para endpoint de usuários
chore(deps): atualizar dependências do projeto
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

## 🔍 Code Review

### Checklist para Reviews

#### Funcionalidade
- [ ] Código faz o que deveria fazer?
- [ ] Testes cobrem casos importantes?
- [ ] Tratamento de erros adequado?

#### Qualidade
- [ ] Código é legível e bem documentado?
- [ ] Nomes são descritivos?
- [ ] Não há duplicação desnecessária?

#### Performance
- [ ] Não há loops desnecessários?
- [ ] Queries são otimizadas?
- [ ] Memória é gerenciada adequadamente?

#### Segurança
- [ ] Dados sensíveis são protegidos?
- [ ] Validação de entrada adequada?
- [ ] Não há vulnerabilidades óbvias?

---

💡 **Lembre-se**: Código é escrito uma vez, mas lido muitas vezes. Priorize clareza e manutenibilidade.