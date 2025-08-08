#!/usr/bin/env python3
"""
Database Setup Script for AUDITORIA360
Creates all necessary tables and initializes data for development
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from portal_demandas.db import init_portal_db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def run_sql_migrations():
    """Execute SQL migration files to create required tables"""
    print("🗃️ Executing SQL migrations...")
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL", "sqlite:///./auditoria360_dev.db")
    engine = create_engine(database_url, echo=True)
    
    migrations_dir = project_root / "migrations"
    
    # List of SQL migration files to execute in order
    sql_migrations = [
        "002_simplify_employee_model.sql",
        "003_criar_tabela_parametros_legais.sql", 
        "004_criar_tabela_documentos.sql",
        "005_evoluir_schema_ia.sql",
        "007_modulo_cct_sindicatos.sql",
        "008_controle_mensal_templates.sql",
    ]
    
    with engine.connect() as conn:
        # Start a transaction
        trans = conn.begin()
        
        try:
            # Create basic tables first (manually since we may not have all dependencies)
            
            # Create Contabilidades table (required by many others)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "Contabilidades" (
                    id BIGINT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    cnpj TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insert sample contabilidade for development
            conn.execute(text("""
                INSERT OR IGNORE INTO "Contabilidades" (id, nome, cnpj, email) 
                VALUES (1, 'Contabilidade Demo LTDA', '12.345.678/0001-00', 'demo@auditoria360.com')
            """))
            
            # Create Empresas table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "Empresas" (
                    id BIGINT PRIMARY KEY,
                    contabilidade_id BIGINT NOT NULL,
                    nome TEXT NOT NULL,
                    cnpj TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contabilidade_id) REFERENCES "Contabilidades"(id)
                )
            """))
            
            # Insert sample empresas
            conn.execute(text("""
                INSERT OR IGNORE INTO "Empresas" (id, contabilidade_id, nome, cnpj) VALUES
                (1, 1, 'Empresa Demo Alpha LTDA', '11.222.333/0001-01'),
                (2, 1, 'Empresa Demo Beta LTDA', '22.333.444/0001-02'),
                (3, 1, 'Empresa Demo Gamma LTDA', '33.444.555/0001-03')
            """))
            
            # Create ControlesMensais table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "ControlesMensais" (
                    id BIGINT PRIMARY KEY,
                    empresa_id BIGINT NOT NULL,
                    mes INTEGER NOT NULL,
                    ano INTEGER NOT NULL,
                    status TEXT DEFAULT 'AGUARD. DADOS',
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (empresa_id) REFERENCES "Empresas"(id)
                )
            """))
            
            # Create TarefasControle table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "TarefasControle" (
                    id BIGINT PRIMARY KEY,
                    controle_mensal_id BIGINT NOT NULL,
                    descricao_tarefa TEXT NOT NULL,
                    concluida BOOLEAN DEFAULT FALSE,
                    data_conclusao TIMESTAMP NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (controle_mensal_id) REFERENCES "ControlesMensais"(id)
                )
            """))
            
            # Create TemplatesControle table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "TemplatesControle" (
                    id BIGINT PRIMARY KEY,
                    contabilidade_id BIGINT NOT NULL,
                    nome_template TEXT NOT NULL,
                    descricao TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contabilidade_id) REFERENCES "Contabilidades"(id),
                    UNIQUE(contabilidade_id, nome_template)
                )
            """))
            
            # Create TemplatesControle_Tarefas table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "TemplatesControle_Tarefas" (
                    id BIGINT PRIMARY KEY,
                    template_id BIGINT NOT NULL,
                    descricao_tarefa TEXT NOT NULL,
                    FOREIGN KEY (template_id) REFERENCES "TemplatesControle"(id)
                )
            """))
            
            # Create ProcessamentosFolha table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "ProcessamentosFolha" (
                    id BIGINT PRIMARY KEY,
                    empresa_id BIGINT NOT NULL,
                    mes INTEGER NOT NULL,
                    ano INTEGER NOT NULL,
                    arquivo_pdf TEXT,
                    status_processamento TEXT DEFAULT 'PROCESSANDO',
                    dados_extraidos TEXT,
                    relatorio_divergencias TEXT,
                    total_funcionarios INTEGER,
                    total_divergencias INTEGER,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    concluido_em TIMESTAMP NULL,
                    FOREIGN KEY (empresa_id) REFERENCES "Empresas"(id)
                )
            """))
            
            # Create Sindicatos table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "Sindicatos" (
                    id BIGINT PRIMARY KEY,
                    nome_sindicato TEXT NOT NULL,
                    cnpj TEXT UNIQUE,
                    base_territorial TEXT,
                    categoria_representada TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create ConvencoesColetivas table  
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "ConvencoesColetivas" (
                    id BIGINT PRIMARY KEY,
                    sindicato_id BIGINT NOT NULL,
                    numero_registro_mte TEXT UNIQUE,
                    vigencia_inicio DATE NOT NULL,
                    vigencia_fim DATE NOT NULL,
                    link_documento_oficial TEXT,
                    dados_cct TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sindicato_id) REFERENCES "Sindicatos"(id)
                )
            """))
            
            # Create LegislacaoDocumentos table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "LegislacaoDocumentos" (
                    id BIGINT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    tipo_documento TEXT NOT NULL,
                    numero_documento TEXT,
                    data_publicacao DATE,
                    orgao_emissor TEXT,
                    status_processamento TEXT DEFAULT 'pendente',
                    arquivo_pdf TEXT,
                    dados_extraidos TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processado_em TIMESTAMP NULL
                )
            """))
            
            # Create HistoricoAnalisesRisco table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "HistoricoAnalisesRisco" (
                    id BIGINT PRIMARY KEY,
                    empresa_id BIGINT NOT NULL,
                    contabilidade_id BIGINT NOT NULL,
                    score_risco INTEGER NOT NULL,
                    relatorio_completo TEXT,
                    analisado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    analisado_por_user_id TEXT,
                    FOREIGN KEY (empresa_id) REFERENCES "Empresas"(id),
                    FOREIGN KEY (contabilidade_id) REFERENCES "Contabilidades"(id)
                )
            """))
            
            # Insert sample templates
            conn.execute(text("""
                INSERT OR IGNORE INTO "TemplatesControle" (id, contabilidade_id, nome_template, descricao) VALUES
                (1, 1, 'Simples Nacional - Padrão', 'Template padrão para empresas do Simples Nacional'),
                (2, 1, 'Lucro Presumido - Completo', 'Template completo para empresas de Lucro Presumido'),
                (3, 1, 'MEI - Simplificado', 'Template simplificado para MEI')
            """))
            
            # Insert sample template tasks
            conn.execute(text("""
                INSERT OR IGNORE INTO "TemplatesControle_Tarefas" (template_id, descricao_tarefa) VALUES
                (1, 'INFO_FOLHA'),
                (1, 'ENVIO_CLIENTE'),
                (1, 'GUIA_FGTS'),
                (1, 'DARF_INSS'),
                (1, 'ESOCIAL_DCTFWEB'),
                (2, 'INFO_FOLHA'),
                (2, 'ENVIO_CLIENTE'),
                (2, 'GUIA_FGTS'),
                (2, 'DARF_INSS'),
                (2, 'ESOCIAL_DCTFWEB'),
                (2, 'APURACAO_IRPJ'),
                (2, 'APURACAO_CSLL'),
                (2, 'SPED_FISCAL'),
                (3, 'INFO_FOLHA'),
                (3, 'ENVIO_CLIENTE'),
                (3, 'DAS_MEI')
            """))
            
            # Insert sample sindicatos
            conn.execute(text("""
                INSERT OR IGNORE INTO "Sindicatos" (id, nome_sindicato, cnpj, base_territorial, categoria_representada) VALUES
                (1, 'Sindicato dos Comerciários de São Paulo', '10.123.456/0001-00', 'São Paulo - SP', 'Trabalhadores no Comércio'),
                (2, 'Sindicato dos Metalúrgicos do ABC', '20.234.567/0001-11', 'ABC Paulista - SP', 'Trabalhadores Metalúrgicos'),
                (3, 'Sindicato dos Bancários de São Paulo', '30.345.678/0001-22', 'São Paulo - SP', 'Trabalhadores Bancários')
            """))
            
            trans.commit()
            print("✅ Database setup completed successfully!")
            
        except Exception as e:
            trans.rollback()
            print(f"❌ Error setting up database: {e}")
            raise


def test_database_connection():
    """Test if database connection and tables are working"""
    print("🧪 Testing database connection...")
    
    try:
        from portal_demandas.db import get_db
        from portal_demandas.db import EmpresaDB, ControleMensalDB
        
        # Test database session
        db = next(get_db())
        
        # Test querying companies
        empresas = db.query(EmpresaDB).limit(5).all()
        print(f"✅ Found {len(empresas)} companies in database")
        for empresa in empresas:
            print(f"  - {empresa.nome} (ID: {empresa.id})")
        
        # Test querying controls
        controles = db.query(ControleMensalDB).limit(3).all()
        print(f"✅ Found {len(controles)} monthly controls in database")
        
        db.close()
        print("✅ Database connection test successful!")
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Setting up AUDITORIA360 database...")
    
    try:
        # Create database and tables
        run_sql_migrations()
        
        # Initialize portal database (creates additional tables if needed)
        print("🗃️ Initializing portal database...")
        init_portal_db()
        
        # Test the connection
        test_database_connection()
        
        print("🎉 Database setup completed successfully!")
        print("💡 You can now run the API server with: python -m portal_demandas.api")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)