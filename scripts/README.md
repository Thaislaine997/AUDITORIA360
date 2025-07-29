# 📜 Scripts AUDITORIA360 - Documentação Completa

> **Diretório organizadado de scripts** para automação, deploy, monitoramento e utilitários do sistema AUDITORIA360

---

## 🗂️ Estrutura Modularizada

### 📁 Por Tipo de Script

#### 🐚 **shell/** - Scripts Shell/Bash
- Scripts para automação em sistemas Unix/Linux
- Deploy e configuração de servidores
- Monitoramento e backup automatizado

#### 💙 **powershell/** - Scripts PowerShell  
- Automação para ambiente Windows/Azure
- Configuração de infraestrutura Microsoft
- Integração com Azure DevOps

#### 🐍 **python/** - Scripts Python
Scripts Python especializados para diferentes funcionalidades:

**🚀 Deploy e Produção**:
- `deploy_production.py` - Deploy completo em produção
- `validate_config.py` - Validação de configurações
- `setup_monitoring.py` - Configuração de monitoramento

**👥 Onboarding e Gestão**:
- `onboarding_cliente.py` - Onboarding automático de clientes
- `monitoramento.py` - Sistema de monitoramento contínuo

**🔐 Segurança e Hash**:
- `generate_hash.py` - Geração de hashes para documentos
- `generate_data_hash.py` - Hash de dados sensíveis

**🤖 Integração MCP**:
- `demo_mcp_integration.py` - Demonstração da integração MCP
- `test_mcp_simple.py` - Testes simples do MCP

**📊 Auditoria e Relatórios**:
- `exportar_auditorias_csv.py` - Exportação de auditorias

#### ⚙️ **batch/** - Scripts Batch
- Scripts para Windows em formato .bat
- Automação de tarefas Windows

### 📋 Scripts Principais do Diretório Raiz

#### `main.py`
**Responsabilidade**: Script principal de entrada do sistema
```bash
python main.py --help
```

#### `__main__.py`
**Responsabilidade**: Módulo de execução principal
```bash
python -m scripts --command process
```

#### `merge_folhas.sql`
**Responsabilidade**: Script SQL para merge de folhas de pagamento
```sql
-- Usado para consolidar dados de múltiplas fontes
```

---

## 🚀 **Guia de Uso dos Scripts Python**

### 🏭 **Deploy em Produção**

#### `deploy_production.py`
```bash
# Deploy completo
python scripts/python/deploy_production.py

# Deploy com ambiente específico
python scripts/python/deploy_production.py --environment prod

# Deploy com verificações extras
python scripts/python/deploy_production.py --environment prod --check-health --run-tests
```

**Funcionalidades**:
- ✅ Verificação de pré-requisitos
- ✅ Build e deploy automático
- ✅ Configuração de variáveis de ambiente
- ✅ Health check pós-deploy
- ✅ Rollback automático em caso de falha

#### `validate_config.py`
```bash
# Validar todas as configurações
python scripts/python/validate_config.py

# Validar configuração específica
python scripts/python/validate_config.py --config database

# Validar e corrigir automaticamente
python scripts/python/validate_config.py --auto-fix
```

### 📊 **Monitoramento**

#### `setup_monitoring.py`
```bash
# Setup completo de monitoramento
python scripts/python/setup_monitoring.py

# Habilitar alertas
python scripts/python/setup_monitoring.py --enable-alerts

# Configurar métricas específicas
python scripts/python/setup_monitoring.py --metrics payroll,documents,api
```

**Configura**:
- 📈 Prometheus para métricas
- 📊 Grafana para dashboards
- 🚨 Alertas automáticos
- 📋 Logs estruturados

#### `monitoramento.py`
```bash
# Monitoramento contínuo
python scripts/python/monitoramento.py

# Monitoramento com relatório
python scripts/python/monitoramento.py --report

# Monitoramento silencioso
python scripts/python/monitoramento.py --silent
```

### 👥 **Onboarding**

#### `onboarding_cliente.py`
```bash
# Onboarding de novo cliente
python scripts/python/onboarding_cliente.py --client-id empresa-xyz

# Onboarding com configuração customizada
python scripts/python/onboarding_cliente.py --client-id empresa-xyz --config custom.json

# Onboarding com dados de teste
python scripts/python/onboarding_cliente.py --client-id empresa-xyz --demo-data
```

**Processo incluí**:
- 🏢 Criação do ambiente do cliente
- 👤 Setup de usuários iniciais
- 📁 Configuração de documentos
- 🔐 Configuração de permissões
- 📊 Dashboard personalizado

### 🤖 **Integração MCP**

#### `demo_mcp_integration.py`
```bash
# Demonstração básica
python scripts/python/demo_mcp_integration.py

# Demo com ferramentas específicas
python scripts/python/demo_mcp_integration.py --tools payroll,audit

# Demo interativo
python scripts/python/demo_mcp_integration.py --interactive
```

**Demonstra**:
- 🔧 Ferramentas MCP disponíveis
- 🤖 Integração com IA
- 📊 Cálculos automatizados
- 🔍 Análises inteligentes

#### `test_mcp_simple.py`
```bash
# Testes básicos do MCP
python scripts/python/test_mcp_simple.py

# Testes com verbose
python scripts/python/test_mcp_simple.py --verbose

# Testes de performance
python scripts/python/test_mcp_simple.py --performance
```

### 🔐 **Segurança e Hash**

#### `generate_hash.py`
```bash
# Gerar hash de arquivo
python scripts/python/generate_hash.py --file documento.pdf

# Gerar múltiplos hashes
python scripts/python/generate_hash.py --file documento.pdf --algorithms md5,sha256,sha512

# Verificar integridade
python scripts/python/generate_hash.py --file documento.pdf --verify hash_conhecido
```

#### `generate_data_hash.py`
```bash
# Hash de dados sensíveis
python scripts/python/generate_data_hash.py --data "dados confidenciais"

# Hash com salt customizado
python scripts/python/generate_data_hash.py --data "dados" --salt custom_salt

# Hash para conformidade LGPD
python scripts/python/generate_data_hash.py --data "cpf:123.456.789-00" --lgpd-compliant
```

### 📊 **Auditoria e Relatórios**

#### `exportar_auditorias_csv.py`
```bash
# Exportar todas as auditorias
python scripts/python/exportar_auditorias_csv.py

# Exportar período específico
python scripts/python/exportar_auditorias_csv.py --start-date 2025-01-01 --end-date 2025-01-31

# Exportar com filtros
python scripts/python/exportar_auditorias_csv.py --client-id empresa-xyz --status completed
```

---

## 🤖 **ML Training**

### 📁 `ml_training/`
Scripts específicos para treinamento de Machine Learning:

```bash
# Treinar modelo de classificação de documentos
python scripts/ml_training/train_document_classifier.py

# Treinar modelo de detecção de anomalias
python scripts/ml_training/train_anomaly_detector.py

# Avaliar modelos treinados
python scripts/ml_training/evaluate_models.py
```

---

## 🎯 **Como Usar**

### 1. **Preparação**
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. **Execução**
```bash
# Navegue para o tipo de script desejado
cd scripts/python

# Execute o script desejado
python script_name.py --help
```

### 3. **Logs e Monitoramento**
```bash
# Ver logs em tempo real
tail -f logs/scripts.log

# Verificar status de execução
python scripts/python/monitoramento.py --status
```

---

## 📚 **Documentação por Subdiretório**

### `shell/`
- ✅ Instalação automática de dependências
- ✅ Deploy em servidores Linux
- ✅ Backup e restore de dados
- ✅ Monitoramento de recursos

### `powershell/`
- ✅ Configuração de ambiente Windows
- ✅ Integração com Azure
- ✅ Deploy em IIS
- ✅ Monitoramento Windows

### `python/`
- ✅ Automação completa de processos
- ✅ Integração com APIs
- ✅ Processamento de dados
- ✅ Machine Learning

### `batch/`
- ✅ Tarefas Windows automatizadas
- ✅ Integração com Task Scheduler
- ✅ Deploy simples

---

## ✅ **Benefícios da Modularização**

### 🔍 **Organização**
- Scripts organizados por tecnologia
- Fácil localização e manutenção
- Documentação segmentada

### 🚀 **Eficiência**
- Reutilização de código
- Padronização de processos
- Automação completa

### 📊 **Monitoramento**
- Logs centralizados
- Métricas de execução
- Alertas automáticos

### 🔐 **Segurança**
- Validação de configurações
- Hashes de integridade
- Conformidade LGPD

---

## 🔗 **Integração com Outros Módulos**

### API Integration
```python
# Os scripts podem usar a API diretamente
from src.api.client import APIClient

client = APIClient()
result = client.call_endpoint("/api/v1/payroll/calculate")
```

### Database Integration
```python
# Acesso direto ao banco quando necessário
from src.models.database import get_session

session = get_session()
# Operações de banco
```

### MCP Integration
```python
# Usar ferramentas MCP nos scripts
from src.mcp.client import MCPClient

client = MCPClient()
result = await client.call_tool("payroll_calculator", params)
```

---

## 📞 **Suporte e Contribuição**

### 🤝 **Como Contribuir**
1. Siga os padrões de nomenclatura
2. Documente todos os parâmetros
3. Adicione testes quando aplicável
4. Use logging estruturado

### 🆘 **Suporte**
- **Issues**: Use GitHub Issues para problemas
- **Documentação**: Consulte esta documentação
- **Exemplos**: Veja `examples/` para exemplos práticos

---

> 💡 **Nota**: Exemplos práticos da stack completa (OCR, DuckDB, R2, etc.) estão centralizados na pasta `examples/`.

> 📊 **Estatísticas**: 15+ scripts Python | 4 categorias principais | Documentação completa | Integração MCP

**Última atualização**: Janeiro 2025 | **Status**: Documentação Completa
