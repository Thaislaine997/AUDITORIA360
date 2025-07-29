# 🌐 AUDITORIA360 API - Guia Completo e Exemplos Práticos

Este documento fornece exemplos práticos de uso da nova stack serverless do AUDITORIA360, incluindo integração com FastAPI, Neon PostgreSQL, Cloudflare R2, DuckDB e PaddleOCR.

## 📋 Índice

1. [Arquitetura da Stack](#arquitetura-da-stack)
2. [Configuração Inicial](#configuração-inicial)
3. [API Principal (FastAPI)](#api-principal-fastapi)
4. [Banco de Dados (Neon PostgreSQL)](#banco-de-dados-neon-postgresql)
5. [Armazenamento (Cloudflare R2)](#armazenamento-cloudflare-r2)
6. [Analytics (DuckDB)](#analytics-duckdb)
7. [OCR (PaddleOCR)](#ocr-paddleocr)
8. [Portal Demandas](#portal-demandas)
9. [Integração Completa](#integração-completa)
10. [Monitoramento e Logs](#monitoramento-e-logs)

---

## 🏗️ Arquitetura da Stack

### Stack Serverless Moderna
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Backend       │
│  (Streamlit)    │────│   (Vercel)      │────│  (FastAPI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                    ┌──────────────────────────────────┼──────────────────────────────────┐
                    │                                  │                                  │
         ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
         │   Database      │              │   Storage       │              │   Analytics     │
         │ (Neon PostgreSQL)│              │ (Cloudflare R2) │              │   (DuckDB)      │
         └─────────────────┘              └─────────────────┘              └─────────────────┘
                    │                                  │                                  │
         ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
         │   OCR Engine    │              │   ML Pipeline   │              │   Cache         │
         │  (PaddleOCR)    │              │   (Prefect)     │              │   (Redis)       │
         └─────────────────┘              └─────────────────┘              └─────────────────┘
```

### Componentes Principais
- **API**: FastAPI com endpoints REST
- **Database**: Neon PostgreSQL serverless
- **Storage**: Cloudflare R2 (S3-compatible)
- **Analytics**: DuckDB embedded
- **OCR**: PaddleOCR local
- **Orchestration**: Prefect workflows

---

## ⚙️ Configuração Inicial

### 1. Variáveis de Ambiente
```bash
# .env.local
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/auditoria360?sslmode=require
R2_ACCESS_KEY_ID=your_r2_access_key
R2_SECRET_ACCESS_KEY=your_r2_secret_key
R2_ENDPOINT_URL=https://account.r2.cloudflarestorage.com
R2_BUCKET_NAME=auditoria360-storage
OPENAI_API_KEY=sk-your-openai-key
```

### 2. Instalação e Setup
```bash
# Clone e configure
git clone https://github.com/user/AUDITORIA360
cd AUDITORIA360

# Execute o instalador automatizado
chmod +x installers/setup_dev_env.sh
./installers/setup_dev_env.sh

# Ou manualmente
pip install -r requirements.txt
python installers/init_db.py
```

---

## 🚀 API Principal (FastAPI)

### Estrutura da API
```python
# api/index.py - Ponto de entrada principal
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AUDITORIA360 API",
    description="Portal de Gestão da Folha, Auditoria 360 e CCT",
    version="1.0.0"
)
```

### 📌 Endpoints Principais

#### 1. Health Check
```bash
# Verificar status da API
curl -X GET "http://localhost:8000/health"
```

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "environment": "development",
  "database": "connected",
  "storage": "cloudflare_r2",
  "ai_service": "openai",
  "version": "1.0.0"
}
```

#### 2. Autenticação JWT
```python
# Exemplo de login
import requests

login_data = {
    "username": "admin@auditoria360.com",
    "password": "secure_password"
}

response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json=login_data
)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
```

#### 3. Upload de Documentos
```python
# Upload de arquivo para processamento
import requests

files = {"file": open("folha_pagamento.pdf", "rb")}
data = {
    "document_type": "folha_pagamento",
    "month": "2024-01",
    "process_ocr": True
}

response = requests.post(
    "http://localhost:8000/api/v1/documents/upload",
    files=files,
    data=data,
    headers=headers
)

document_id = response.json()["document_id"]
```

---

## 🗄️ Banco de Dados (Neon PostgreSQL)

### Configuração e Conexão
```python
# src/models/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Modelos de Dados
```python
# Exemplo: Modelo de Funcionário
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from datetime import datetime

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    position = Column(String(100))
    salary = Column(Numeric(10, 2))
    hire_date = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cpf": self.cpf,
            "position": self.position,
            "salary": float(self.salary) if self.salary else None,
            "hire_date": self.hire_date.isoformat(),
            "active": self.active
        }
```

### Operações CRUD
```python
# Exemplo: CRUD de Funcionários
from sqlalchemy.orm import Session
from typing import List, Optional

class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_employee(self, employee_data: dict) -> Employee:
        employee = Employee(**employee_data)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
    
    def list_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        return self.db.query(Employee).offset(skip).limit(limit).all()
    
    def update_employee(self, employee_id: int, update_data: dict) -> Optional[Employee]:
        employee = self.get_employee(employee_id)
        if employee:
            for key, value in update_data.items():
                setattr(employee, key, value)
            self.db.commit()
            self.db.refresh(employee)
        return employee
```

### Uso Prático
```python
# Exemplo de uso em endpoint
from fastapi import Depends
from src.models.database import get_db

@app.post("/api/v1/employees/")
def create_employee(employee_data: dict, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.create_employee(employee_data)
    return employee.to_dict()

@app.get("/api/v1/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.to_dict()
```

---

## ☁️ Armazenamento (Cloudflare R2)

### Configuração do Cliente
```python
# src/services/storage_service.py
import boto3
import os
from botocore.config import Config

class R2StorageService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
            endpoint_url=os.getenv('R2_ENDPOINT_URL'),
            region_name='auto',
            config=Config(
                retries={'max_attempts': 3},
                region_name='auto'
            )
        )
        self.bucket_name = os.getenv('R2_BUCKET_NAME')
    
    def upload_file(self, file_content: bytes, file_key: str, content_type: str = None) -> str:
        """Upload arquivo para R2"""
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
        
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_key,
            Body=file_content,
            **extra_args
        )
        
        # Retorna URL de acesso
        return f"https://{self.bucket_name}.{os.getenv('R2_DOMAIN', 'r2.dev')}/{file_key}"
    
    def download_file(self, file_key: str) -> bytes:
        """Download arquivo do R2"""
        response = self.client.get_object(Bucket=self.bucket_name, Key=file_key)
        return response['Body'].read()
    
    def delete_file(self, file_key: str) -> bool:
        """Deletar arquivo do R2"""
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except Exception:
            return False
    
    def list_files(self, prefix: str = "") -> list:
        """Listar arquivos no R2"""
        response = self.client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=prefix
        )
        return [obj['Key'] for obj in response.get('Contents', [])]
```

### Uso em Endpoints
```python
# Upload de arquivo via API
from fastapi import UploadFile, File
import uuid
from datetime import datetime

@app.post("/api/v1/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "general",
    db: Session = Depends(get_db)
):
    # Validar tipo de arquivo
    allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido")
    
    # Gerar chave única para o arquivo
    file_extension = file.filename.split('.')[-1]
    file_key = f"documents/{document_type}/{datetime.now().strftime('%Y/%m')}/{uuid.uuid4()}.{file_extension}"
    
    # Upload para R2
    storage = R2StorageService()
    file_content = await file.read()
    file_url = storage.upload_file(file_content, file_key, file.content_type)
    
    # Salvar metadados no banco
    document = Document(
        filename=file.filename,
        file_key=file_key,
        file_url=file_url,
        content_type=file.content_type,
        file_size=len(file_content),
        document_type=document_type,
        uploaded_at=datetime.utcnow()
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "document_id": document.id,
        "file_url": file_url,
        "message": "Arquivo enviado com sucesso"
    }
```

---

## 📊 Analytics (DuckDB)

### Configuração e Uso
```python
# src/services/analytics_service.py
import duckdb
import pandas as pd
import os
from typing import Dict, List, Any

class AnalyticsService:
    def __init__(self):
        # Usar DuckDB em memória para desenvolvimento, arquivo para produção
        db_path = os.getenv('DUCKDB_DATABASE_PATH', ':memory:')
        self.conn = duckdb.connect(db_path)
        self._setup_extensions()
    
    def _setup_extensions(self):
        """Configurar extensões necessárias"""
        try:
            self.conn.execute("INSTALL httpfs")
            self.conn.execute("LOAD httpfs")
            self.conn.execute("INSTALL postgres")
            self.conn.execute("LOAD postgres")
        except Exception as e:
            print(f"Warning: Could not load extensions: {e}")
    
    def load_from_postgres(self, query: str, connection_string: str) -> pd.DataFrame:
        """Carregar dados do PostgreSQL"""
        postgres_query = f"""
        ATTACH '{connection_string}' AS postgres_db (TYPE POSTGRES);
        SELECT * FROM postgres_db.({query})
        """
        return self.conn.execute(postgres_query).fetchdf()
    
    def create_payroll_analytics(self) -> Dict[str, Any]:
        """Análise de folha de pagamento"""
        # Exemplo de query analítica
        query = """
        WITH monthly_stats AS (
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                COUNT(*) as total_employees,
                SUM(salary) as total_payroll,
                AVG(salary) as avg_salary,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median_salary
            FROM employees 
            WHERE active = true
            GROUP BY DATE_TRUNC('month', created_at)
        )
        SELECT 
            month,
            total_employees,
            total_payroll,
            avg_salary,
            median_salary,
            LAG(total_payroll) OVER (ORDER BY month) as prev_month_payroll,
            (total_payroll - LAG(total_payroll) OVER (ORDER BY month)) / LAG(total_payroll) OVER (ORDER BY month) * 100 as growth_rate
        FROM monthly_stats
        ORDER BY month DESC
        """
        
        result = self.conn.execute(query).fetchdf()
        return result.to_dict('records')
    
    def audit_compliance_report(self) -> Dict[str, Any]:
        """Relatório de compliance de auditoria"""
        queries = {
            'missing_documents': """
                SELECT employee_id, name, 
                       COUNT(*) as missing_docs
                FROM employees e
                LEFT JOIN documents d ON e.id = d.employee_id
                WHERE d.id IS NULL
                GROUP BY employee_id, name
                HAVING COUNT(*) > 0
            """,
            'salary_outliers': """
                WITH stats AS (
                    SELECT AVG(salary) as avg_sal, STDDEV(salary) as std_sal
                    FROM employees WHERE active = true
                )
                SELECT id, name, salary,
                       (salary - avg_sal) / std_sal as z_score
                FROM employees, stats
                WHERE active = true 
                AND ABS((salary - avg_sal) / std_sal) > 2
            """,
            'compliance_score': """
                SELECT 
                    COUNT(CASE WHEN documents_complete = true THEN 1 END) * 100.0 / COUNT(*) as compliance_percentage
                FROM employees
                WHERE active = true
            """
        }
        
        results = {}
        for key, query in queries.items():
            results[key] = self.conn.execute(query).fetchdf().to_dict('records')
        
        return results
```

### Endpoint de Analytics
```python
@app.get("/api/v1/analytics/payroll")
def get_payroll_analytics(db: Session = Depends(get_db)):
    """Obter análises de folha de pagamento"""
    analytics = AnalyticsService()
    
    # Carregar dados do PostgreSQL para DuckDB
    connection_string = os.getenv('DATABASE_URL')
    payroll_data = analytics.load_from_postgres(
        "SELECT * FROM employees WHERE active = true",
        connection_string
    )
    
    # Gerar relatórios
    results = analytics.create_payroll_analytics()
    
    return {
        "payroll_analytics": results,
        "generated_at": datetime.utcnow().isoformat(),
        "total_records": len(payroll_data)
    }

@app.get("/api/v1/analytics/compliance")
def get_compliance_report(db: Session = Depends(get_db)):
    """Relatório de compliance"""
    analytics = AnalyticsService()
    results = analytics.audit_compliance_report()
    
    return {
        "compliance_report": results,
        "generated_at": datetime.utcnow().isoformat()
    }
```

---

## 🔍 OCR (PaddleOCR)

### Configuração do Serviço
```python
# src/services/ocr_service.py
from paddleocr import PaddleOCR
import cv2
import numpy as np
import logging
from typing import List, Dict, Any
import os

class OCRService:
    def __init__(self):
        # Configurar PaddleOCR
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='pt',  # Português
            use_gpu=os.getenv('PADDLE_OCR_USE_GPU', 'false').lower() == 'true',
            show_log=False
        )
        self.logger = logging.getLogger(__name__)
    
    def preprocess_image(self, image_array: np.ndarray) -> np.ndarray:
        """Pré-processar imagem para melhor OCR"""
        # Converter para escala de cinza
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        # Redimensionar se muito grande
        height, width = gray.shape
        if width > 2000:
            scale = 2000 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            gray = cv2.resize(gray, (new_width, new_height))
        
        # Melhorar contraste
        gray = cv2.equalizeHist(gray)
        
        # Reduzir ruído
        gray = cv2.medianBlur(gray, 3)
        
        return gray
    
    def extract_text(self, image_data: bytes) -> List[Dict[str, Any]]:
        """Extrair texto de imagem"""
        try:
            # Converter bytes para numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Pré-processar
            processed_image = self.preprocess_image(image)
            
            # Executar OCR
            results = self.ocr.ocr(processed_image, cls=True)
            
            # Processar resultados
            extracted_data = []
            for line_result in results[0]:
                if line_result:
                    bbox, (text, confidence) = line_result
                    extracted_data.append({
                        'text': text,
                        'confidence': float(confidence),
                        'bbox': bbox,  # Coordenadas da bounding box
                    })
            
            return extracted_data
            
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            raise Exception(f"Erro na extração de texto: {str(e)}")
    
    def extract_payroll_data(self, image_data: bytes) -> Dict[str, Any]:
        """Extrair dados específicos de folha de pagamento"""
        text_data = self.extract_text(image_data)
        
        # Padrões para identificar informações da folha
        patterns = {
            'employee_name': r'NOME[:\s]+([A-ZÁÀÂÃÉÊÍÔÕÚÇ\s]+)',
            'cpf': r'CPF[:\s]+([\d\.\-\/]+)',
            'salary': r'SALÁRIO[:\s]+([\d\.,]+)',
            'gross_pay': r'BRUTO[:\s]+([\d\.,]+)',
            'net_pay': r'LÍQUIDO[:\s]+([\d\.,]+)',
            'month_year': r'((?:JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ)[A-Z]*[\/\-\s]*\d{4})'
        }
        
        # Combinar todo o texto
        full_text = ' '.join([item['text'] for item in text_data])
        
        # Extrair informações usando regex
        import re
        extracted_info = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, full_text.upper())
            if match:
                extracted_info[key] = match.group(1).strip()
        
        # Calcular score de confiança médio
        avg_confidence = sum([item['confidence'] for item in text_data]) / len(text_data) if text_data else 0
        
        return {
            'extracted_fields': extracted_info,
            'raw_text_data': text_data,
            'confidence_score': avg_confidence,
            'total_text_blocks': len(text_data)
        }
```

### Endpoint de OCR
```python
@app.post("/api/v1/ocr/process")
async def process_document_ocr(
    file: UploadFile = File(...),
    document_type: str = "payroll",
    extract_fields: bool = True
):
    """Processar documento com OCR"""
    
    # Validar tipo de arquivo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Apenas imagens são suportadas")
    
    try:
        # Ler arquivo
        file_content = await file.read()
        
        # Processar OCR
        ocr_service = OCRService()
        
        if document_type == "payroll" and extract_fields:
            # Extração específica para folha de pagamento
            result = ocr_service.extract_payroll_data(file_content)
        else:
            # Extração geral de texto
            text_data = ocr_service.extract_text(file_content)
            result = {
                'raw_text_data': text_data,
                'confidence_score': sum([item['confidence'] for item in text_data]) / len(text_data) if text_data else 0,
                'total_text_blocks': len(text_data)
            }
        
        # Salvar resultado no banco (opcional)
        # ... código para salvar resultado ...
        
        return {
            'status': 'success',
            'filename': file.filename,
            'document_type': document_type,
            'ocr_result': result,
            'processed_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento OCR: {str(e)}")
```

---

## 🎫 Portal Demandas

### Exemplo Completo de Uso
```python
# Exemplo de integração com o Portal Demandas
import requests
import json

class PortalDemandasClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
    
    def create_audit_ticket(self, audit_data: dict) -> dict:
        """Criar ticket de auditoria"""
        ticket_data = {
            "titulo": f"Auditoria - {audit_data['company_name']} - {audit_data['period']}",
            "descricao": f"Auditoria de folha de pagamento para {audit_data['company_name']} referente ao período {audit_data['period']}",
            "etapa": "Análise Inicial",
            "prazo": audit_data['deadline'],
            "responsavel": audit_data['auditor'],
            "prioridade": "alta",
            "categoria": "auditoria",
            "tempo_estimado": 16
        }
        
        response = requests.post(f"{self.base_url}/tickets/", json=ticket_data)
        return response.json()
    
    def update_ticket_progress(self, ticket_id: int, status: str, comments: str) -> dict:
        """Atualizar progresso do ticket"""
        update_data = {
            "status": status,
            "comentarios_internos": comments
        }
        
        response = requests.patch(f"{self.base_url}/tickets/{ticket_id}", json=update_data)
        return response.json()
    
    def add_ocr_result_comment(self, ticket_id: int, ocr_result: dict) -> dict:
        """Adicionar resultado de OCR como comentário"""
        comment_data = {
            "autor": "Sistema OCR",
            "comentario": f"Documento processado com OCR. Confiança: {ocr_result['confidence_score']:.2%}",
            "tipo": "system"
        }
        
        response = requests.post(f"{self.base_url}/tickets/{ticket_id}/comments/", json=comment_data)
        return response.json()
```

---

## 🔗 Integração Completa

### Workflow de Auditoria Completo
```python
# Exemplo de workflow completo de auditoria
from datetime import datetime, timedelta

@app.post("/api/v1/audit/start-process")
async def start_audit_process(
    company_id: int,
    period: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Iniciar processo completo de auditoria"""
    
    try:
        # 1. Criar ticket no Portal Demandas
        portal_client = PortalDemandasClient()
        ticket_data = {
            "company_name": f"Company {company_id}",
            "period": period,
            "deadline": (datetime.now() + timedelta(days=15)).isoformat(),
            "auditor": "Sistema Automatizado"
        }
        ticket = portal_client.create_audit_ticket(ticket_data)
        ticket_id = ticket['id']
        
        # 2. Upload e processamento de arquivos
        storage = R2StorageService()
        ocr_service = OCRService()
        processed_files = []
        
        for file in files:
            # Upload para R2
            file_content = await file.read()
            file_key = f"audit/{company_id}/{period}/{file.filename}"
            file_url = storage.upload_file(file_content, file_key, file.content_type)
            
            # Processar OCR se for imagem
            if file.content_type.startswith('image/'):
                ocr_result = ocr_service.extract_payroll_data(file_content)
                
                # Adicionar resultado como comentário no ticket
                portal_client.add_ocr_result_comment(ticket_id, ocr_result)
            
            processed_files.append({
                "filename": file.filename,
                "file_url": file_url,
                "file_key": file_key,
                "ocr_processed": file.content_type.startswith('image/')
            })
        
        # 3. Atualizar status do ticket
        portal_client.update_ticket_progress(
            ticket_id, 
            "em_andamento", 
            f"Arquivos processados: {len(processed_files)} documentos"
        )
        
        # 4. Iniciar análise com DuckDB
        analytics = AnalyticsService()
        compliance_report = analytics.audit_compliance_report()
        
        # 5. Gerar relatório final
        audit_report = {
            "ticket_id": ticket_id,
            "company_id": company_id,
            "period": period,
            "processed_files": processed_files,
            "compliance_report": compliance_report,
            "started_at": datetime.utcnow().isoformat(),
            "status": "processing"
        }
        
        # 6. Salvar no banco
        audit_record = AuditRecord(**audit_report)
        db.add(audit_record)
        db.commit()
        
        return {
            "message": "Processo de auditoria iniciado com sucesso",
            "audit_id": audit_record.id,
            "ticket_id": ticket_id,
            "files_processed": len(processed_files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar auditoria: {str(e)}")
```

---

## 📊 Monitoramento e Logs

### Sistema de Logs
```python
# src/utils/logging_config.py
import logging
import os
from datetime import datetime

def setup_logging():
    """Configurar sistema de logs"""
    
    # Criar logger
    logger = logging.getLogger("auditoria360")
    logger.setLevel(logging.INFO)
    
    # Criar handler para arquivo
    log_file = f"logs/auditoria360_{datetime.now().strftime('%Y%m%d')}.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Criar handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if os.getenv('DEBUG') == 'true' else logging.INFO)
    
    # Criar formatador
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Usar em toda a aplicação
logger = setup_logging()
```

### Métricas da API
```python
# Middleware para métricas
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log da requisição
    logger.info(f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/api/v1/metrics")
def get_metrics():
    """Endpoint de métricas da aplicação"""
    return {
        "uptime": time.time() - app_start_time,
        "database_status": "connected",
        "storage_status": "connected",
        "ocr_status": "available",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }
```

---

## 🧪 Testes da Integração

### Teste Completo
```python
# tests/test_integration.py
import pytest
import requests
from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_complete_audit_workflow():
    """Teste do workflow completo de auditoria"""
    
    # 1. Health check
    response = client.get("/health")
    assert response.status_code == 200
    
    # 2. Upload de documento
    with open("test_files/payroll_sample.pdf", "rb") as f:
        files = {"file": ("payroll.pdf", f, "application/pdf")}
        data = {"document_type": "payroll"}
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        assert response.status_code == 200
        document_data = response.json()
    
    # 3. Processar OCR
    with open("test_files/payroll_image.jpg", "rb") as f:
        files = {"file": ("payroll.jpg", f, "image/jpeg")}
        
        response = client.post("/api/v1/ocr/process", files=files)
        assert response.status_code == 200
        ocr_data = response.json()
        assert ocr_data['status'] == 'success'
    
    # 4. Criar ticket
    ticket_data = {
        "titulo": "Teste de Auditoria",
        "descricao": "Teste automatizado",
        "etapa": "Teste",
        "prazo": "2024-12-31T23:59:59",
        "responsavel": "Sistema de Teste"
    }
    
    response = requests.post("http://localhost:8001/tickets/", json=ticket_data)
    assert response.status_code == 200
    ticket = response.json()
    
    # 5. Verificar analytics
    response = client.get("/api/v1/analytics/compliance")
    assert response.status_code == 200
    analytics_data = response.json()
    
    print("✅ Teste de integração completo passou!")
    return {
        "document": document_data,
        "ocr": ocr_data,
        "ticket": ticket,
        "analytics": analytics_data
    }

if __name__ == "__main__":
    test_complete_audit_workflow()
```

---

## 📞 Suporte e Recursos

### Links Úteis
- **API Docs**: http://localhost:8000/docs
- **Portal Demandas**: http://localhost:8001/docs
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/api/v1/metrics

### Troubleshooting Comum
```bash
# Verificar conexão com Neon
curl -X GET "http://localhost:8000/health"

# Testar upload de arquivo
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@test.pdf" \
  -F "document_type=test"

# Verificar portal demandas
curl -X GET "http://localhost:8001/health"

# Testar OCR
curl -X POST "http://localhost:8000/api/v1/ocr/process" \
  -F "file=@test_image.jpg"
```

---

**Este guia fornece uma base sólida para uso da nova stack serverless do AUDITORIA360. Para informações mais detalhadas, consulte a documentação específica de cada módulo.**