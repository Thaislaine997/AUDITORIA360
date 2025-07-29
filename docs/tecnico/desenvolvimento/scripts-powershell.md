# 🔧 Scripts PowerShell - AUDITORIA360

> **Documentação completa dos scripts PowerShell** para desenvolvimento e deploy

---

## 📋 **VISÃO GERAL**

O projeto AUDITORIA360 inclui scripts PowerShell padronizados para:
- **Configuração do ambiente de desenvolvimento** (Windows)
- **Deploy automatizado** do backend e frontend no Google Cloud Run
- **Manutenção e administração** do sistema

### 🎯 **Características dos Scripts**
- **Padronização**: Comandos e parâmetros consistentes
- **Robustez**: Tratamento de erros e validações
- **Flexibilidade**: Parâmetros configuráveis
- **Clareza**: Comentários explicativos e output colorido

---

## 📁 **SCRIPTS DISPONÍVEIS**

### 1. **Setup do Ambiente de Desenvolvimento**
```powershell
# Localização: installers/setup_dev_env.ps1
.\installers\setup_dev_env.ps1 -VerboseOutputOutput
```

**Propósito**: Configuração automática do ambiente de desenvolvimento Windows

**Parâmetros**:
- `-SkipPython`: Pula instalação do Python
- `-SkipGit`: Pula instalação do Git
- `-VerboseOutputOutput`: Output detalhado

**Funcionalidades**:
- ✅ Instalação do Chocolatey
- ✅ Instalação do Python 3.11+
- ✅ Instalação do Git
- ✅ Criação do ambiente virtual
- ✅ Instalação de dependências
- ✅ Configuração de arquivos .env
- ✅ Setup de pre-commit hooks
- ✅ Inicialização do banco de dados
- ✅ Testes de validação

### 2. **Deploy do Backend (Cloud Run)**
```powershell
# Localização: deploy/cloudrun_deploy_backend.ps1
.\deploy\cloudrun_deploy_backend.ps1 -ProjectId "meu-projeto" -ProcessorId "processor123" -VerboseOutputOutput
```

**Propósito**: Build e deploy automatizado do backend FastAPI

**Parâmetros Obrigatórios**:
- `-ProjectId`: ID do projeto Google Cloud

**Parâmetros Opcionais**:
- `-Region`: Região do Cloud Run (padrão: us-central1)
- `-ServiceName`: Nome do serviço (padrão: auditoria360-backend)
- `-ImageName`: Nome da imagem Docker
- `-ProcessorId`: ID do Document AI Processor
- `-BQDatasetId`: ID do dataset BigQuery
- `-TextBucketName`: Nome do bucket para textos
- `-SkipBuild`: Pula o build da imagem
- `-AllowUnauthenticated`: Permite acesso não autenticado
- `-VerboseOutputOutput`: Output detalhado

### 3. **Deploy do Frontend (Cloud Run)**
```powershell
# Localização: deploy/cloudrun_deploy_streamlit.ps1
.\deploy\cloudrun_deploy_streamlit.ps1 -ProjectId "meu-projeto" -ApiBaseUrl "https://api.exemplo.com" -VerboseOutputOutput
```

**Propósito**: Build e deploy automatizado do frontend Streamlit

**Parâmetros Obrigatórios**:
- `-ProjectId`: ID do projeto Google Cloud
- `-ApiBaseUrl`: URL base da API backend

**Parâmetros Opcionais**:
- `-Region`: Região do Cloud Run (padrão: us-central1)
- `-ServiceName`: Nome do serviço (padrão: auditoria360-streamlit)
- `-ImageName`: Nome da imagem Docker
- `-DockerfilePath`: Caminho do Dockerfile (padrão: deploy/Dockerfile.streamlit)
- `-SkipBuild`: Pula o build da imagem
- `-AllowUnauthenticated`: Permite acesso não autenticado
- `-VerboseOutputOutput`: Output detalhado

---

## 🚀 **GUIAS DE USO**

### 🏗️ **Setup Completo do Ambiente**

```powershell
# 1. Executar como Administrador (recomendado)
# Abrir PowerShell como Administrador

# 2. Navegar para o diretório do projeto
cd C:\caminho\para\AUDITORIA360

# 3. Executar script de setup
.\installers\setup_dev_env.ps1 -VerboseOutput

# 4. Seguir instruções pós-instalação
# - Editar .env.local com suas configurações
# - Configurar credenciais do banco de dados
# - Testar a instalação
```

### ☁️ **Deploy Completo (Backend + Frontend)**

```powershell
# 1. Configurar gcloud CLI
gcloud auth login
gcloud config set project SEU_PROJECT_ID

# 2. Deploy do Backend
.\deploy\cloudrun_deploy_backend.ps1 `
    -ProjectId "meu-projeto-gcp" `
    -ProcessorId "1234567890abcdef" `
    -AllowUnauthenticated `
    -VerboseOutput

# 3. Aguardar deployment e copiar URL da API

# 4. Deploy do Frontend
.\deploy\cloudrun_deploy_streamlit.ps1 `
    -ProjectId "meu-projeto-gcp" `
    -ApiBaseUrl "https://auditoria360-backend-xxx-uc.a.run.app" `
    -AllowUnauthenticated `
    -VerboseOutput
```

### 🔄 **Deploy Incremental (Re-deploy)**

```powershell
# Para re-deploy apenas do backend (após mudanças)
.\deploy\cloudrun_deploy_backend.ps1 `
    -ProjectId "meu-projeto-gcp" `
    -ProcessorId "1234567890abcdef"

# Para re-deploy apenas do frontend
.\deploy\cloudrun_deploy_streamlit.ps1 `
    -ProjectId "meu-projeto-gcp" `
    -ApiBaseUrl "https://api-url-existente.com"

# Para pular build (usar imagem existente)
.\deploy\cloudrun_deploy_backend.ps1 `
    -ProjectId "meu-projeto-gcp" `
    -SkipBuild
```

---

## ⚙️ **CONFIGURAÇÕES E VARIÁVEIS**

### 🏠 **Variáveis de Ambiente - Setup**
```bash
# Criadas automaticamente no .env.local
DATABASE_URL=postgresql://...
CLOUDFLARE_R2_ENDPOINT=https://...
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret-key
ENVIRONMENT=development
DEBUG=true
```

### ☁️ **Variáveis de Ambiente - Cloud Run**

**Backend**:
```bash
GCP_PROJECT_ID=meu-projeto
BQ_DATASET_ID=auditoria_folha_dataset
CCT_TEXT_BUCKET_NAME=auditoria360-ccts-textos-extraidos
CCT_EXTRATOR_PROCESSOR_ID=processor-id
```

**Frontend**:
```bash
API_BASE_URL=https://backend-url.com
```

---

## 🛠️ **TROUBLESHOOTING**

### ❌ **Problemas Comuns - Setup**

#### 🔐 **Erro de Política de Execução**
```powershell
# Solução: Permitir execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ou executar com bypass temporário
powershell -ExecutionPolicy Bypass -File .\installers\setup_dev_env.ps1
```

#### 📦 **Erro de Chocolatey**
```powershell
# Verificar instalação
choco --version

# Reinstalar se necessário
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### 🐍 **Problemas com Python**
```powershell
# Verificar versão
python --version

# Reinstalar se necessário
choco uninstall python311
choco install python311 --force

# Recrear ambiente virtual
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ **Problemas Comuns - Deploy**

#### ☁️ **Erro de Autenticação gcloud**
```powershell
# Re-autenticar
gcloud auth login
gcloud auth application-default login

# Verificar projeto
gcloud config get-value project
gcloud config set project SEU_PROJECT_ID
```

#### 🐳 **Erro de Build de Container**
```powershell
# Verificar se Docker está rodando (Cloud Build usa Docker remoto)
gcloud auth configure-docker

# Build manual para debug
gcloud builds submit --tag gcr.io/PROJECT_ID/auditoria360-backend --verbosity=debug
```

#### 🌐 **Erro de Deploy Cloud Run**
```powershell
# Verificar permissões
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:EMAIL" \
    --role="roles/run.admin"

# Verificar quota
gcloud compute regions describe REGION
```

### 🔍 **Debug e Logs**

```powershell
# Ver logs do Cloud Run
gcloud run services logs read auditoria360-backend --region=us-central1

# Ver builds anteriores
gcloud builds list --limit=10

# Testar conectividade
gcloud run services describe auditoria360-backend --region=us-central1 --format="value(status.url)"
```

---

## 📋 **CHECKLIST DE VALIDAÇÃO**

### ✅ **Pós-Setup (Desenvolvimento)**
- [ ] Python 3.11+ instalado e funcionando
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas sem erros
- [ ] Arquivo .env.local configurado
- [ ] Banco de dados conectando
- [ ] Testes básicos passando
- [ ] API executando em localhost:8000
- [ ] Frontend executando em localhost:3000

### ✅ **Pós-Deploy (Produção)**
- [ ] Backend deploy concluído sem erros
- [ ] Frontend deploy concluído sem erros
- [ ] URLs dos serviços funcionando
- [ ] API respondendo no Cloud Run
- [ ] Frontend carregando e conectando à API
- [ ] Variáveis de ambiente configuradas
- [ ] Logs sem erros críticos
- [ ] Testes de smoke passando

---

## 📚 **REFERÊNCIAS TÉCNICAS**

### 🔗 **Links Úteis**
- [PowerShell Documentation](https://docs.microsoft.com/powershell/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [Chocolatey Packages](https://chocolatey.org/packages)

### 📖 **Documentação Relacionada**
- [Setup do Ambiente](setup-ambiente.md)
- [Deploy Checklist](../deploy/deploy-checklist.md)
- [Monitoramento](../deploy/monitoring-setup-guide.md)
- [APIs](../apis/api-documentation.md)

---

## 🔄 **VERSIONAMENTO E ATUALIZAÇÕES**

### 📋 **Histórico de Mudanças**
- **v1.0** (Jan 2025): Scripts iniciais básicos
- **v2.0** (Jan 2025): Refatoração completa com padronização
  - ✅ Tratamento de erros robusto
  - ✅ Parâmetros configuráveis
  - ✅ Output colorido e informativo
  - ✅ Validações de pré-requisitos
  - ✅ Documentação completa

### 🚀 **Roadmap**
- [ ] Support para Linux/macOS (bash equivalents)
- [ ] Integração com CI/CD
- [ ] Scripts de rollback automático
- [ ] Monitoring automático pós-deploy

---

> 💡 **Dica**: Execute sempre com `-VerboseOutput` para debug detalhado, especialmente em caso de problemas.

**Última atualização**: Janeiro 2025 | **Versão**: 2.0 | **Compatibilidade**: PowerShell 5.1+, Windows 10+