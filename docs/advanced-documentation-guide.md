# 📚 Advanced Documentation & Tutorials - AUDITORIA360

## Visão Geral

Este documento serve como um índice completo para toda a documentação avançada do AUDITORIA360, incluindo guias detalhados, tutoriais passo-a-passo e melhores práticas.

---

## 📖 Estrutura da Documentação

```
docs/
├── README.md                           # Documentação principal
├── api/                               # Documentação da API
│   ├── authentication.md
│   ├── endpoints.md
│   └── examples.md
├── performance-optimization-guide.md   # Guia de otimização
├── monitoring-setup-guide.md          # Guia de monitoramento
├── deployment/                        # Deployment e DevOps
│   ├── vercel-deployment.md
│   ├── database-setup.md
│   └── environment-variables.md
├── tutorials/                         # Tutoriais passo-a-passo
│   ├── getting-started.md
│   ├── ocr-integration.md
│   ├── cct-management.md
│   └── audit-workflows.md
├── architecture/                      # Arquitetura do sistema
│   ├── system-overview.md
│   ├── database-schema.md
│   └── serverless-architecture.md
└── troubleshooting/                   # Solução de problemas
    ├── common-issues.md
    ├── performance-issues.md
    └── error-handling.md
```

---

## 🚀 Tutoriais Essenciais

### 1. Getting Started - Primeiros Passos

#### Configuração do Ambiente de Desenvolvimento

```bash
# 1. Clone do repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# 2. Configuração do ambiente Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalação de dependências
pip install -r requirements.txt

# 4. Configuração de variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações
```

#### Configuração de Variáveis de Ambiente

```bash
# .env
# Database (Neon)
DATABASE_URL=postgresql://user:password@host/db

# Storage (Cloudflare R2)
R2_ACCESS_KEY_ID=seu_access_key
R2_SECRET_ACCESS_KEY=seu_secret_key
R2_BUCKET_NAME=auditoria360-bucket
R2_ENDPOINT_URL=https://account.r2.cloudflarestorage.com

# Authentication
JWT_SECRET_KEY=sua_chave_secreta_jwt
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Monitoring (opcional)
MONITORING_ENABLED=true
ALERT_EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=alerts@auditoria360.com
SMTP_PASSWORD=senha_do_app

# External APIs
OPENAI_API_KEY=sua_chave_openai  # Para IA/chatbot
```

#### Primeira Execução

```bash
# 1. Executar testes para verificar configuração
python -m pytest tests/test_basic_health.py -v

# 2. Inicializar banco de dados
python scripts/init_database.py

# 3. Executar servidor de desenvolvimento
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# 4. Verificar health check
curl http://localhost:8000/health
```

### 2. Integração OCR - Tutorial Completo

#### Configuração do PaddleOCR

```python
# src/services/ocr_service.py
from paddleocr import PaddleOCR
import os
from typing import List, Dict, Any

class OCRService:
    def __init__(self):
        # Configurar PaddleOCR com português
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='pt',  # Português
            show_log=False
        )
    
    async def extract_text_from_image(self, image_path: str) -> Dict[str, Any]:
        """Extrair texto de uma imagem"""
        try:
            # Processar imagem
            result = self.ocr.ocr(image_path, cls=True)
            
            # Extrair texto e coordenadas
            extracted_data = {
                'text': '',
                'blocks': [],
                'confidence': 0.0
            }
            
            if result and len(result) > 0:
                for line in result[0]:
                    bbox, (text, confidence) = line
                    
                    extracted_data['blocks'].append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
                    
                    extracted_data['text'] += text + ' '
                
                # Calcular confiança média
                confidences = [block['confidence'] for block in extracted_data['blocks']]
                extracted_data['confidence'] = sum(confidences) / len(confidences) if confidences else 0.0
            
            return extracted_data
            
        except Exception as e:
            raise Exception(f"Erro no OCR: {str(e)}")

# Exemplo de uso
ocr_service = OCRService()

@app.post("/api/v1/documents/ocr")
async def process_document_ocr(file: UploadFile):
    # Salvar arquivo temporário
    temp_path = f"/tmp/{file.filename}"
    
    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Extrair texto
        result = await ocr_service.extract_text_from_image(temp_path)
        
        # Salvar resultado no banco
        document = Document(
            filename=file.filename,
            extracted_text=result['text'],
            confidence=result['confidence'],
            ocr_blocks=result['blocks']
        )
        db.save(document)
        
        return {
            "message": "Documento processado com sucesso",
            "document_id": document.id,
            "extracted_text": result['text'],
            "confidence": result['confidence']
        }
        
    finally:
        # Limpar arquivo temporário
        os.remove(temp_path)
```

#### Processamento de CCT com OCR

```python
class CCTProcessor:
    def __init__(self, ocr_service: OCRService):
        self.ocr_service = ocr_service
    
    async def process_cct_document(self, file_path: str, empresa_id: int) -> Dict[str, Any]:
        """Processar documento CCT completo"""
        
        # 1. Extrair texto com OCR
        ocr_result = await self.ocr_service.extract_text_from_image(file_path)
        
        # 2. Identificar seções importantes
        sections = self._identify_cct_sections(ocr_result['text'])
        
        # 3. Extrair dados estruturados
        structured_data = self._extract_structured_data(sections)
        
        # 4. Salvar no banco
        cct = CCTDocument(
            empresa_id=empresa_id,
            raw_text=ocr_result['text'],
            structured_data=structured_data,
            confidence=ocr_result['confidence']
        )
        
        return {
            "cct_id": cct.id,
            "sections_found": list(sections.keys()),
            "structured_data": structured_data,
            "confidence": ocr_result['confidence']
        }
    
    def _identify_cct_sections(self, text: str) -> Dict[str, str]:
        """Identificar seções da CCT usando regex"""
        import re
        
        sections = {}
        
        # Padrões para seções típicas de CCT
        patterns = {
            'salario_minimo': r'salário mínimo.*?(\d+[,.]?\d*)',
            'jornada_trabalho': r'jornada.*?trabalho.*?(\d+.*?horas)',
            'ferias': r'férias.*?([\s\S]*?)(?=\n\n|\nartigo|\ncláusula)',
            'rescisao': r'rescisão.*?([\s\S]*?)(?=\n\n|\nartigo|\ncláusula)'
        }
        
        for section_name, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                sections[section_name] = match.group(0)
        
        return sections
```

### 3. Gestão de Auditoria - Workflow Completo

#### Criação de Auditoria

```python
# models/audit_models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from src.models.database import Base
import enum

class AuditStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Audit(Base):
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, nullable=False)
    tipo_auditoria = Column(String(100), nullable=False)
    status = Column(Enum(AuditStatus), default=AuditStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    results = Column(JSON, nullable=True)
    issues_found = Column(JSON, nullable=True)

# services/audit_service.py
class AuditService:
    def __init__(self, db_session):
        self.db = db_session
    
    async def create_audit(self, empresa_id: int, tipo: str) -> Audit:
        """Criar nova auditoria"""
        audit = Audit(
            empresa_id=empresa_id,
            tipo_auditoria=tipo,
            status=AuditStatus.PENDING
        )
        
        self.db.add(audit)
        self.db.commit()
        
        # Iniciar processamento assíncrono
        await self._start_audit_processing(audit.id)
        
        return audit
    
    async def _start_audit_processing(self, audit_id: int):
        """Iniciar processamento da auditoria"""
        audit = self.db.get(Audit, audit_id)
        audit.status = AuditStatus.IN_PROGRESS
        self.db.commit()
        
        try:
            # Executar verificações específicas do tipo
            if audit.tipo_auditoria == "folha_pagamento":
                results = await self._audit_folha_pagamento(audit.empresa_id)
            elif audit.tipo_auditoria == "cct_compliance":
                results = await self._audit_cct_compliance(audit.empresa_id)
            else:
                results = await self._audit_general(audit.empresa_id)
            
            # Salvar resultados
            audit.results = results
            audit.status = AuditStatus.COMPLETED
            audit.completed_at = datetime.utcnow()
            
        except Exception as e:
            audit.status = AuditStatus.FAILED
            audit.results = {"error": str(e)}
        
        self.db.commit()
    
    async def _audit_folha_pagamento(self, empresa_id: int) -> Dict[str, Any]:
        """Auditoria específica de folha de pagamento"""
        issues = []
        
        # Verificar cálculos INSS
        folhas = self.db.query(FolhaPagamento).filter_by(empresa_id=empresa_id).all()
        
        for folha in folhas:
            # Recalcular INSS
            inss_expected = calcular_inss(folha.salario_base)
            
            if abs(folha.desconto_inss - inss_expected) > 0.01:
                issues.append({
                    "tipo": "calculo_inss_incorreto",
                    "funcionario_id": folha.funcionario_id,
                    "valor_atual": folha.desconto_inss,
                    "valor_esperado": inss_expected,
                    "diferenca": folha.desconto_inss - inss_expected
                })
        
        return {
            "total_folhas_verificadas": len(folhas),
            "issues_encontradas": len(issues),
            "detalhes": issues
        }

# API endpoint
@app.post("/api/v1/audits")
async def create_audit(audit_request: AuditCreateRequest):
    audit_service = AuditService(db_session)
    audit = await audit_service.create_audit(
        empresa_id=audit_request.empresa_id,
        tipo=audit_request.tipo_auditoria
    )
    
    return {
        "audit_id": audit.id,
        "status": audit.status.value,
        "message": "Auditoria iniciada com sucesso"
    }
```

---

## 🔧 API Documentation

### Autenticação

```python
# Obter token JWT
POST /api/v1/auth/login
{
    "username": "usuario@empresa.com",
    "password": "senha123"
}

# Resposta
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
}

# Usar token nas requisições
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Principais Endpoints

#### Auditorias
```python
# Listar auditorias
GET /api/v1/audits?empresa_id=123&status=completed

# Criar auditoria
POST /api/v1/audits
{
    "empresa_id": 123,
    "tipo_auditoria": "folha_pagamento"
}

# Obter detalhes
GET /api/v1/audits/456

# Obter resultados
GET /api/v1/audits/456/results
```

#### Documentos e OCR
```python
# Upload de documento
POST /api/v1/documents/upload
Content-Type: multipart/form-data
file: [arquivo]
empresa_id: 123
document_type: "cct"

# Processar OCR
POST /api/v1/documents/456/process-ocr

# Obter texto extraído
GET /api/v1/documents/456/extracted-text
```

#### Folha de Pagamento
```python
# Importar folha
POST /api/v1/payroll/import
{
    "empresa_id": 123,
    "mes_ano": "2024-01",
    "arquivo_url": "https://storage.com/folha.csv"
}

# Calcular folha
POST /api/v1/payroll/calculate
{
    "empresa_id": 123,
    "funcionario_ids": [1, 2, 3],
    "periodo": "2024-01"
}

# Obter relatório
GET /api/v1/payroll/123/report?periodo=2024-01
```

---

## 🏗️ Arquitetura do Sistema

### Arquitetura Serverless

```mermaid
graph TB
    Frontend[Frontend Streamlit] --> API[Vercel - FastAPI]
    API --> DB[(Neon PostgreSQL)]
    API --> Storage[Cloudflare R2]
    API --> Analytics[(DuckDB)]
    API --> ML[PaddleOCR + AI]
    
    API --> Monitor[Monitoring System]
    Monitor --> Alerts[Email/Slack Alerts]
    Monitor --> Metrics[Prometheus Metrics]
    
    subgraph "Vercel Functions"
        API
        Jobs[Background Jobs]
    end
    
    subgraph "Data Layer"
        DB
        Storage
        Analytics
    end
```

### Fluxo de Dados

1. **Upload de Documentos**
   - Frontend → API → Cloudflare R2
   - Trigger de processamento OCR
   - Armazenamento de metadados no Neon

2. **Processamento OCR**
   - PaddleOCR extrai texto
   - IA analisa e estrutura dados
   - Resultados salvos no banco

3. **Auditoria**
   - Coleta dados de múltiplas fontes
   - Executa regras de compliance
   - Gera relatórios e alertas

---

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Banco

```bash
# Verificar conectividade
python -c "
import psycopg2
try:
    conn = psycopg2.connect('$DATABASE_URL')
    print('✅ Conexão OK')
except Exception as e:
    print(f'❌ Erro: {e}')
"
```

#### 2. OCR Não Funciona

```python
# Verificar instalação PaddleOCR
import paddleocr
try:
    ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='pt')
    print("✅ PaddleOCR OK")
except Exception as e:
    print(f"❌ Erro PaddleOCR: {e}")
    print("Solução: pip install paddlepaddle paddleocr")
```

#### 3. Performance Issues

```python
# Verificar bottlenecks
from src.utils.performance import profiler

# Analisar últimas 24h
bottlenecks = profiler.get_bottlenecks(hours=24)
for b in bottlenecks:
    print(f"Função lenta: {b['function_name']}")
    print(f"Tempo médio: {b['stats']['avg_time']:.2f}s")
```

### Logs e Debugging

```python
# Configurar logging detalhado
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auditoria360.log'),
        logging.StreamHandler()
    ]
)

# Logger específico para módulos
logger = logging.getLogger('auditoria360.ocr')
logger.debug("Processando documento...")
```

---

## 📊 Melhores Práticas

### Desenvolvimento

1. **Code Style**
   ```bash
   # Usar formatação automática
   black src/
   isort src/
   flake8 src/
   ```

2. **Testing**
   ```bash
   # Testes unitários
   pytest tests/unit/ -v
   
   # Testes de integração
   pytest tests/integration/ -v
   
   # Cobertura
   pytest --cov=src tests/
   ```

3. **Performance**
   - Usar profiling em funções críticas
   - Implementar cache para operações custosas
   - Monitorar métricas continuamente

### Deployment

1. **Environment Variables**
   - Nunca commitar secrets
   - Usar .env.example como template
   - Validar configurações no startup

2. **Monitoring**
   - Configurar alertas antes do deploy
   - Implementar health checks
   - Monitorar métricas de negócio

3. **Backup**
   - Backup automático do banco
   - Versionamento de documentos
   - Plano de disaster recovery

---

## 📞 Suporte e Comunidade

### Canais de Suporte

1. **Issues GitHub**: Para bugs e feature requests
2. **Documentação**: Wiki completo no repositório
3. **Email**: support@auditoria360.com
4. **Slack**: Canal interno da equipe

### Contribuindo

1. Fork do repositório
2. Criar branch feature/fix
3. Implementar mudanças com testes
4. Abrir Pull Request com descrição detalhada

### Roadmap

- **Q1 2025**: IA avançada para análise de documentos
- **Q2 2025**: Dashboard analytics em tempo real
- **Q3 2025**: Mobile app para auditores
- **Q4 2025**: Integração com ERPs principais

---

*Última atualização: 2025-01-28*
*Versão: 1.0.0*

---

## 📁 Índice de Documentos

- [Performance Optimization Guide](./performance-optimization-guide.md)
- [Monitoring Setup Guide](./monitoring-setup-guide.md)
- [API Documentation](./api-documentation.md)
- [Deployment Guide](./deployment-guide.md)
- [Database Schema](./database-schema.md)
- [Troubleshooting Guide](./troubleshooting-guide.md)