# Documentação AUDITORIA360

Este diretório contém a documentação completa do sistema AUDITORIA360, organizada de forma modular e com geração automática.

## 📋 Estrutura da Documentação

```
docs/
├── sphinx/                     # Documentação técnica (Sphinx)
│   ├── conf.py                 # Configuração do Sphinx
│   ├── index.rst               # Índice principal da API docs
│   ├── modules/                # Documentação por módulo
│   └── _build/html/            # Documentação gerada
├── content/                    # Documentação de usuário
│   ├── index.md                # Página inicial
│   ├── api/                    # Introdução à API
│   ├── tecnico/                # Documentação técnica
│   ├── usuario/                # Manuais de usuário
│   ├── estrategico/            # Documentação estratégica
│   ├── compliance/             # Auditoria e compliance
│   └── relatorios/            # Relatórios de projeto
├── scripts/build_docs.sh       # Script de build unificado
├── documentation_index.html    # Índice unificado (gerado)
└── mkdocs.yml                  # Configuração MkDocs
```

## 🚀 Como Gerar a Documentação

### Comandos Makefile

```bash
# Gerar apenas documentação da API (Sphinx)
make docs-build

# Gerar documentação completa
make docs-full

# Limpar arquivos de build
make docs-clean

# Rebuild completo
make docs-rebuild

# Servir documentação localmente
make docs-serve

# Preparar para deploy
make docs-deploy
```

### Scripts Diretos

```bash
# Build completo com script
./scripts/build_docs.sh

# Build apenas Sphinx
cd docs/sphinx && sphinx-build -b html . _build/html
```

## 📚 Tipos de Documentação

### 1. Documentação da API (Sphinx)
- **Localização**: `docs/sphinx/_build/html/`
- **Fonte**: Docstrings do código-fonte
- **Conteúdo**: APIs, modelos, serviços, utilitários
- **Atualização**: Automática a partir do código

### 2. Documentação de Usuário
- **Localização**: `docs/content/`
- **Fonte**: Markdown files
- **Conteúdo**: Manuais, guias, tutoriais
- **Atualização**: Manual

## 🔧 Configuração

### Sphinx (API Documentation)
- **Configuração**: `docs/sphinx/conf.py`
- **Tema**: Alabaster
- **Idioma**: Português (pt_BR)
- **Extensions**: autodoc, napoleon, viewcode

### MkDocs (User Documentation)
- **Configuração**: `docs/mkdocs.yml`
- **Tema**: Material
- **Plugins**: mkdocstrings para integração Python

## 📝 Mantendo a Documentação Atualizada

### Para Desenvolvedores

1. **Sempre documente funções e classes**:
   ```python
   def minha_funcao(param1: str, param2: int) -> bool:
       """
       Descrição breve da função.
       
       Args:
           param1: Descrição do parâmetro 1
           param2: Descrição do parâmetro 2
           
       Returns:
           Descrição do retorno
           
       Raises:
           ValueError: Quando param2 é negativo
       """
   ```

2. **Execute a build após mudanças**:
   ```bash
   make docs-build
   ```

3. **Revise a documentação gerada**:
   - Abra `docs/documentation_index.html`
   - Verifique links e formatting

4. **Commit as mudanças**:
   ```bash
   git add docs/
   git commit -m "docs: update module documentation"
   ```

### Para Documentação de Usuário

1. **Edite arquivos Markdown** em `docs/content/`
2. **Use sintaxe padrão Markdown**
3. **Mantenha links relativos funcionais**
4. **Teste localmente** com `make docs-serve`

## 🌐 Acesso à Documentação

### Local Development
```bash
# Servir documentação na porta 8080
make docs-serve

# Acessar:
# - Índice unificado: http://localhost:8080/documentation_index.html
# - API docs: http://localhost:8080/sphinx/_build/html/
# - User docs: http://localhost:8080/content/
```

### Production
A documentação pode ser servida diretamente dos arquivos estáticos gerados ou integrada a serviços como GitHub Pages, Netlify, etc.

## 🔄 Sincronização Automática

O sistema está configurado para:

1. **Gerar docs da API** automaticamente a partir dos docstrings
2. **Criar índice unificado** que liga ambos os tipos de documentação
3. **Manter estrutura consistente** entre user e technical docs
4. **Facilitar integração com CI/CD** através dos comandos make

## 🆘 Troubleshooting

### Problemas Comuns

1. **Erro de import modules**:
   - Verifique se todas as dependências estão instaladas
   - Configure mock_imports no `conf.py` se necessário

2. **Links quebrados**:
   - Verifique caminhos relativos nos arquivos .md
   - Certifique-se que arquivos referenciados existem

3. **Build falha**:
   - Execute `make docs-clean` antes de rebuild
   - Verifique logs de erro para módulos específicos

4. **Documentação não atualiza**:
   - Force rebuild com `make docs-rebuild`
   - Verifique se docstrings seguem formato Google style

## 📧 Contribuição

Para contribuir com a documentação:

1. Siga os padrões de docstring estabelecidos
2. Teste builds localmente antes de commit
3. Mantenha documentação de usuário sincronizada
4. Use linguagem clara e exemplos práticos