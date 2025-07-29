#!/usr/bin/env python3
"""
AUDITORIA360 Database Initialization Script
This script initializes the database with required tables and seed data
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_url():
    """Get database URL from environment variables"""
    # Try to get from .env.local first, then from environment
    env_file = project_root / ".env.local"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    if key.strip() == "DATABASE_URL":
                        return value.strip()

    # Fallback to environment variable
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Use SQLite for development if no database URL is provided
        database_url = f"sqlite:///{project_root}/dev_auditoria360.db"
        logger.warning(f"No DATABASE_URL found, using SQLite: {database_url}")

    return database_url


def create_database_tables():
    """Create all database tables"""
    try:
        # Import models to register them with SQLAlchemy
        from portal_demandas.db import Base as PortalBase
        from src.models.database import Base, engine

        logger.info("Creating database tables...")

        # Create main application tables
        Base.metadata.create_all(bind=engine)

        # Create portal_demandas tables
        PortalBase.metadata.create_all(bind=engine)

        logger.info("✅ Database tables created successfully")
        return True

    except ImportError as e:
        logger.warning(f"Some models not found: {e}")
        logger.info("Creating basic database structure...")

        # Fallback: create basic tables manually
        database_url = get_database_url()
        engine = create_engine(database_url)

        # Create basic tables SQL
        basic_tables_sql = """
        -- Users and Authentication
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT true,
            is_superuser BOOLEAN DEFAULT false,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Portal Demandas Tickets
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            etapa VARCHAR(50),
            prazo TIMESTAMP,
            responsavel VARCHAR(100),
            status VARCHAR(20) DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Documents
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500),
            file_size INTEGER,
            content_type VARCHAR(100),
            uploaded_by INTEGER REFERENCES users(id),
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed BOOLEAN DEFAULT false
        );
        
        -- Audit Logs
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            action VARCHAR(100) NOT NULL,
            resource_type VARCHAR(50),
            resource_id VARCHAR(50),
            details JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address INET
        );
        """

        with engine.connect() as conn:
            # Execute each statement separately
            for statement in basic_tables_sql.split(";"):
                statement = statement.strip()
                if statement:
                    conn.execute(text(statement))
            conn.commit()

        logger.info("✅ Basic database structure created")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


def create_seed_data():
    """Create initial seed data"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)

        logger.info("Creating seed data...")

        # Create default admin user
        admin_user_sql = """
        INSERT INTO users (username, email, hashed_password, is_superuser, is_active)
        VALUES ('admin', 'admin@auditoria360.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewfYD2sD9GfvOTH.', true, true)
        ON CONFLICT (username) DO NOTHING;
        """

        # Create sample notification templates
        notification_templates_sql = """
        CREATE TABLE IF NOT EXISTS notification_templates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            subject VARCHAR(200) NOT NULL,
            body_template TEXT NOT NULL,
            template_type VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        INSERT INTO notification_templates (name, subject, body_template, template_type)
        VALUES 
        ('welcome_user', 'Bem-vindo ao AUDITORIA360', 'Olá {{username}}, bem-vindo ao sistema AUDITORIA360!', 'email'),
        ('document_processed', 'Documento Processado', 'O documento {{filename}} foi processado com sucesso.', 'email'),
        ('audit_alert', 'Alerta de Auditoria', 'Foi detectada uma inconsistência: {{details}}', 'email')
        ON CONFLICT (name) DO NOTHING;
        """

        with engine.connect() as conn:
            # Execute each statement
            for statement in [admin_user_sql, notification_templates_sql]:
                for sql in statement.split(";"):
                    sql = sql.strip()
                    if sql:
                        conn.execute(text(sql))
            conn.commit()

        logger.info("✅ Seed data created successfully")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Error creating seed data: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error creating seed data: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]

        if test_value == 1:
            logger.info("✅ Database connection test passed")
            return True
        else:
            logger.error("❌ Database connection test failed")
            return False

    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def main():
    """Main initialization function"""
    logger.info("🚀 Starting AUDITORIA360 database initialization...")

    # Test connection first
    if not test_database_connection():
        logger.error("Failed to connect to database. Please check your configuration.")
        sys.exit(1)

    # Create tables
    if not create_database_tables():
        logger.error("Failed to create database tables.")
        sys.exit(1)

    # Create seed data
    if not create_seed_data():
        logger.error("Failed to create seed data.")
        sys.exit(1)

    logger.info("🎉 Database initialization completed successfully!")
    logger.info("Default admin user created: admin@auditoria360.com / admin")


if __name__ == "__main__":
    main()
