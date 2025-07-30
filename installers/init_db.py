#!/usr/bin/env python3
"""
AUDITORIA360 Database Initialization Script
This script initializes the database with required tables and seed data
using the service layer architecture for maintainable code.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from typing import List, Dict, Any

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Import our new service layer and constants
from src.core.constants import (
    DatabaseTableNames, 
    EnvironmentVariables,
    SystemDefaults
)
from src.services.user_service import UserService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_url():
    """
    Get database URL from environment variables with secure fallback handling.
    
    Returns:
        Database URL string
    """
    # Try to get from .env.local first, then from environment
    env_file = project_root / ".env.local"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    if key.strip() == EnvironmentVariables.DATABASE_URL:
                        return value.strip()

    # Fallback to environment variable
    database_url = os.getenv(EnvironmentVariables.DATABASE_URL)
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

        # Fallback: create basic tables manually using our centralized SQL function
        database_url = get_database_url()
        engine = create_engine(database_url)

        basic_tables_sql = _create_basic_tables_sql()

        with engine.connect() as conn:
            # Execute each statement separately for better error handling
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


def _create_basic_tables_sql() -> str:
    """
    Generate SQL for creating basic database tables.
    This function encapsulates table creation logic for better maintainability.
    
    Returns:
        SQL string for creating basic tables
    """
    return f"""
    -- Users and Authentication
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.USERS} (
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
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.TICKETS} (
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
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.DOCUMENTS} (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        original_filename VARCHAR(255) NOT NULL,
        file_path VARCHAR(500),
        file_size INTEGER,
        content_type VARCHAR(100),
        uploaded_by INTEGER REFERENCES {DatabaseTableNames.USERS}(id),
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed BOOLEAN DEFAULT false
    );
    
    -- Audit Logs
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.AUDIT_LOGS} (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES {DatabaseTableNames.USERS}(id),
        action VARCHAR(100) NOT NULL,
        resource_type VARCHAR(50),
        resource_id VARCHAR(50),
        details JSONB,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address INET
    );
    """


def _create_companies_and_users_with_service(user_service: UserService) -> List[str]:
    """
    Create companies and users using the service layer.
    This encapsulates the business logic for creating test data.
    
    Args:
        user_service: UserService instance for business operations
        
    Returns:
        List of SQL statements to execute
    """
    sql_statements = []
    
    # Create companies table first
    companies_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.COMPANIES} (
        id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        company_type VARCHAR(50) NOT NULL,
        contact_email VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    sql_statements.append(companies_table_sql)
    
    # Create enhanced users table
    enhanced_users_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.USERS_ENHANCED} (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        user_type VARCHAR(50) NOT NULL,
        company_id VARCHAR(100) REFERENCES {DatabaseTableNames.COMPANIES}(id),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    sql_statements.append(enhanced_users_table_sql)
    
    # Generate companies data
    companies = user_service.create_test_companies()
    for company in companies:
        company_sql = f"""
        INSERT INTO {DatabaseTableNames.COMPANIES} (id, name, company_type, contact_email, is_active, created_at)
        VALUES ('{company["id"]}', '{company["name"]}', '{company["company_type"]}', 
                '{company["contact_email"]}', {company["is_active"]}, CURRENT_TIMESTAMP)
        ON CONFLICT (id) DO NOTHING;
        """
        sql_statements.append(company_sql)
    
    # Generate super admin user
    try:
        admin_user = user_service.create_super_admin_user()
        admin_sql = f"""
        INSERT INTO {DatabaseTableNames.USERS_ENHANCED} 
        (username, email, password_hash, full_name, user_type, company_id, is_active, created_at)
        VALUES ('{admin_user["username"]}', '{admin_user["email"]}', '{admin_user["password_hash"]}',
                '{admin_user["full_name"]}', '{admin_user["user_type"]}', NULL, 
                {admin_user["is_active"]}, CURRENT_TIMESTAMP)
        ON CONFLICT (username) DO NOTHING;
        """
        sql_statements.append(admin_sql)
    except ValueError as e:
        logger.error(f"Failed to create super admin user: {e}")
        raise
    
    # Generate test users
    try:
        test_users = user_service.create_test_users()
        for user in test_users:
            user_sql = f"""
            INSERT INTO {DatabaseTableNames.USERS_ENHANCED} 
            (username, email, password_hash, full_name, user_type, company_id, is_active, created_at)
            VALUES ('{user["username"]}', '{user["email"]}', '{user["password_hash"]}',
                    '{user["full_name"]}', '{user["user_type"]}', '{user["company_id"]}', 
                    {user["is_active"]}, CURRENT_TIMESTAMP)
            ON CONFLICT (username) DO NOTHING;
            """
            sql_statements.append(user_sql)
    except ValueError as e:
        logger.error(f"Failed to create test users: {e}")
        raise
    
    return sql_statements


def _create_notification_templates_with_service(user_service: UserService) -> List[str]:
    """
    Create notification templates using the service layer.
    
    Args:
        user_service: UserService instance for business operations
        
    Returns:
        List of SQL statements to execute
    """
    sql_statements = []
    
    # Create notification templates table
    templates_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {DatabaseTableNames.NOTIFICATION_TEMPLATES} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        subject VARCHAR(200) NOT NULL,
        body_template TEXT NOT NULL,
        template_type VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    sql_statements.append(templates_table_sql)
    
    # Generate notification templates
    templates = user_service.create_notification_templates()
    for template in templates:
        template_sql = f"""
        INSERT INTO {DatabaseTableNames.NOTIFICATION_TEMPLATES} 
        (name, subject, body_template, template_type, created_at)
        VALUES ('{template["name"]}', '{template["subject"]}', 
                '{template["body_template"]}', '{template["template_type"]}', CURRENT_TIMESTAMP)
        ON CONFLICT (name) DO NOTHING;
        """
        sql_statements.append(template_sql)
    
    return sql_statements


def create_seed_data():
    """
    Create initial seed data using the service layer architecture.
    This function has been refactored to use business logic encapsulation.
    """
    try:
        # Initialize the user service for business operations
        user_service = UserService()
        
        database_url = get_database_url()
        engine = create_engine(database_url)

        logger.info("Creating seed data using service layer...")

        # Generate all SQL statements using service layer
        all_sql_statements = []
        
        # Add companies and users
        all_sql_statements.extend(_create_companies_and_users_with_service(user_service))
        
        # Add notification templates  
        all_sql_statements.extend(_create_notification_templates_with_service(user_service))

        # Execute all statements in a transaction
        with engine.connect() as conn:
            for sql_statement in all_sql_statements:
                # Split and execute each statement separately for better error handling
                for statement in sql_statement.split(";"):
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
            conn.commit()

        logger.info("✅ Seed data created successfully using service layer")
        return True

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file has all required password variables set")
        return False
    except SQLAlchemyError as e:
        logger.error(f"Database error creating seed data: {e}")
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
    """
    Main initialization function with comprehensive error handling.
    This function orchestrates the complete database setup process.
    """
    logger.info("🚀 Starting AUDITORIA360 database initialization...")

    # Step 1: Test database connectivity before proceeding
    logger.info("Step 1: Testing database connection...")
    if not test_database_connection():
        logger.error("Failed to connect to database. Please check your configuration.")
        logger.error("Ensure DATABASE_URL is properly set in your environment.")
        sys.exit(1)

    # Step 2: Create database schema and tables
    logger.info("Step 2: Creating database tables...")
    if not create_database_tables():
        logger.error("Failed to create database tables.")
        sys.exit(1)

    # Step 3: Populate with initial seed data using service layer
    logger.info("Step 3: Creating seed data...")
    if not create_seed_data():
        logger.error("Failed to create seed data.")
        logger.error("Check that all required environment variables are set in your .env file:")
        logger.error(f"- {EnvironmentVariables.DEFAULT_ADMIN_PASSWORD}")
        logger.error(f"- {EnvironmentVariables.DEFAULT_GESTOR_A_PASSWORD}")
        logger.error(f"- {EnvironmentVariables.DEFAULT_GESTOR_B_PASSWORD}")
        logger.error(f"- {EnvironmentVariables.DEFAULT_CLIENT_X_PASSWORD}")
        sys.exit(1)

    logger.info("🎉 Database initialization completed successfully!")
    logger.info("✅ All users and companies have been created with secure passwords from environment variables")
    logger.info("🔐 Check your .env file for the configured passwords")
    logger.info("📊 System ready for multi-tenant operations")


if __name__ == "__main__":
    main()
