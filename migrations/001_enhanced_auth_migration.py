"""
Database Migration Script for Enhanced Multi-Level Access Control
Creates necessary tables and initial data for the new authentication system
"""

import asyncio
import os

import asyncpg
from passlib.context import CryptContext

# Import secure secrets manager
try:
    from src.core.secrets import secrets_manager
except ImportError:
    # Fallback for direct execution
    class SimpleSecretsManager:
        def get_database_url(self):
            return os.getenv(
                "DATABASE_URL", "postgresql://user:password@localhost/auditoria360"
            )

        def get_default_passwords(self):
            return {
                "admin": os.getenv("DEFAULT_ADMIN_PASSWORD", "secure_admin_pass_123!"),
                "gestor_a": os.getenv(
                    "DEFAULT_GESTOR_A_PASSWORD", "secure_gestor_a_123!"
                ),
                "gestor_b": os.getenv(
                    "DEFAULT_GESTOR_B_PASSWORD", "secure_gestor_b_123!"
                ),
                "client_x": os.getenv(
                    "DEFAULT_CLIENT_X_PASSWORD", "secure_client_x_123!"
                ),
            }

    secrets_manager = SimpleSecretsManager()

# Configuration - using secrets manager
DATABASE_URL = secrets_manager.get_database_url()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_enhanced_user_tables():
    """Create enhanced user and access control tables"""

    migration_sql = """
    -- Enhanced Users table with multi-level access support
    CREATE TABLE IF NOT EXISTS users_enhanced (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('super_admin', 'contabilidade', 'cliente_final')),
        company_id VARCHAR(100),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        login_attempts INTEGER DEFAULT 0,
        locked_until TIMESTAMP
    );

    -- User roles table
    CREATE TABLE IF NOT EXISTS user_roles (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users_enhanced(id) ON DELETE CASCADE,
        role_name VARCHAR(100) NOT NULL,
        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        granted_by INTEGER REFERENCES users_enhanced(id)
    );

    -- User permissions table
    CREATE TABLE IF NOT EXISTS user_permissions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users_enhanced(id) ON DELETE CASCADE,
        permission_name VARCHAR(100) NOT NULL,
        resource_type VARCHAR(100),
        resource_id VARCHAR(100),
        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        granted_by INTEGER REFERENCES users_enhanced(id)
    );

    -- Companies/Contabilidades table
    CREATE TABLE IF NOT EXISTS companies (
        id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        company_type VARCHAR(50) NOT NULL CHECK (company_type IN ('contabilidade', 'empresa')),
        parent_company_id VARCHAR(100) REFERENCES companies(id),
        contact_email VARCHAR(255),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Data access scopes table
    CREATE TABLE IF NOT EXISTS user_data_scopes (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users_enhanced(id) ON DELETE CASCADE,
        scope_type VARCHAR(50) NOT NULL CHECK (scope_type IN ('all', 'company', 'enterprise')),
        contabilidade_id VARCHAR(100) REFERENCES companies(id),
        empresa_id VARCHAR(100) REFERENCES companies(id),
        additional_filters JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Audit log table for access tracking
    CREATE TABLE IF NOT EXISTS access_audit_log (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users_enhanced(id),
        action VARCHAR(100) NOT NULL,
        resource_type VARCHAR(100),
        resource_id VARCHAR(100),
        ip_address INET,
        user_agent TEXT,
        success BOOLEAN NOT NULL,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Session management table
    CREATE TABLE IF NOT EXISTS user_sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users_enhanced(id) ON DELETE CASCADE,
        session_token VARCHAR(255) UNIQUE NOT NULL,
        refresh_token VARCHAR(255) UNIQUE,
        expires_at TIMESTAMP NOT NULL,
        ip_address INET,
        user_agent TEXT,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_users_enhanced_email ON users_enhanced(email);
    CREATE INDEX IF NOT EXISTS idx_users_enhanced_username ON users_enhanced(username);
    CREATE INDEX IF NOT EXISTS idx_users_enhanced_user_type ON users_enhanced(user_type);
    CREATE INDEX IF NOT EXISTS idx_users_enhanced_company_id ON users_enhanced(company_id);
    CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON user_roles(user_id);
    CREATE INDEX IF NOT EXISTS idx_user_permissions_user_id ON user_permissions(user_id);
    CREATE INDEX IF NOT EXISTS idx_user_data_scopes_user_id ON user_data_scopes(user_id);
    CREATE INDEX IF NOT EXISTS idx_access_audit_log_user_id ON access_audit_log(user_id);
    CREATE INDEX IF NOT EXISTS idx_access_audit_log_created_at ON access_audit_log(created_at);
    CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
    CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);

    -- Update trigger for updated_at timestamps
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    CREATE TRIGGER update_users_enhanced_updated_at 
        BEFORE UPDATE ON users_enhanced 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

    CREATE TRIGGER update_companies_updated_at 
        BEFORE UPDATE ON companies 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """

    return migration_sql


async def insert_initial_data():
    """Insert initial companies and test users with secure passwords"""

    # Get secure passwords from secrets manager
    secure_passwords = secrets_manager.get_default_passwords()

    # Hash passwords securely
    admin_password = pwd_context.hash(secure_passwords["admin"])
    gestor_a_password = pwd_context.hash(secure_passwords["gestor_a"])
    gestor_b_password = pwd_context.hash(secure_passwords["gestor_b"])
    cliente_x_password = pwd_context.hash(secure_passwords["client_x"])

    data_sql = f"""
    -- Insert companies
    INSERT INTO companies (id, name, company_type, contact_email) VALUES
    ('CONTAB_A', 'Contabilidade Exemplo A Ltda', 'contabilidade', 'contato@contabilidade-exemplo-a.com'),
    ('CONTAB_B', 'Contabilidade Exemplo B Ltda', 'contabilidade', 'contato@contabilidade-exemplo-b.com'),
    ('EMPRESA_X', 'Empresa Teste X S.A.', 'empresa', 'contato@empresa-teste-x.com'),
    ('EMPRESA_Y', 'Empresa Teste Y Ltda', 'empresa', 'contato@empresa-teste-y.com'),
    ('EMPRESA_Z', 'Empresa Teste Z EIRELI', 'empresa', 'contato@empresa-teste-z.com')
    ON CONFLICT (id) DO NOTHING;

    -- Set parent relationships (empresas belong to contabilidades)
    UPDATE companies SET parent_company_id = 'CONTAB_A' WHERE id IN ('EMPRESA_X', 'EMPRESA_Y');
    UPDATE companies SET parent_company_id = 'CONTAB_B' WHERE id = 'EMPRESA_Z';

    -- Insert test users
    INSERT INTO users_enhanced (username, email, password_hash, full_name, user_type, company_id) VALUES
    ('admin@auditoria360-exemplo.com', 'admin@auditoria360-exemplo.com', '{admin_password}', 'Super Administrator', 'super_admin', NULL),
    ('gestor@contabilidade-exemplo-a.com', 'gestor@contabilidade-exemplo-a.com', '{gestor_a_password}', 'Gestor Contabilidade Exemplo A', 'contabilidade', 'CONTAB_A'),
    ('gestor@contabilidade-exemplo-b.com', 'gestor@contabilidade-exemplo-b.com', '{gestor_b_password}', 'Gestor Contabilidade Exemplo B', 'contabilidade', 'CONTAB_B'),
    ('contato@empresa-teste-x.com', 'contato@empresa-teste-x.com', '{cliente_x_password}', 'Cliente Empresa Teste X', 'cliente_final', 'EMPRESA_X')
    ON CONFLICT (username) DO NOTHING;

    -- Insert user roles
    INSERT INTO user_roles (user_id, role_name) 
    SELECT u.id, 'super_admin' FROM users_enhanced u WHERE u.user_type = 'super_admin'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_roles (user_id, role_name) 
    SELECT u.id, 'gestor' FROM users_enhanced u WHERE u.user_type = 'contabilidade'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_roles (user_id, role_name) 
    SELECT u.id, 'cliente' FROM users_enhanced u WHERE u.user_type = 'cliente_final'
    ON CONFLICT DO NOTHING;

    -- Insert user permissions
    INSERT INTO user_permissions (user_id, permission_name) 
    SELECT u.id, 'full_access' FROM users_enhanced u WHERE u.user_type = 'super_admin'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_permissions (user_id, permission_name) 
    SELECT u.id, 'view_company_data' FROM users_enhanced u WHERE u.user_type = 'contabilidade'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_permissions (user_id, permission_name) 
    SELECT u.id, 'manage_clients' FROM users_enhanced u WHERE u.user_type = 'contabilidade'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_permissions (user_id, permission_name) 
    SELECT u.id, 'view_own_data' FROM users_enhanced u WHERE u.user_type = 'cliente_final'
    ON CONFLICT DO NOTHING;

    -- Insert data scopes
    INSERT INTO user_data_scopes (user_id, scope_type) 
    SELECT u.id, 'all' FROM users_enhanced u WHERE u.user_type = 'super_admin'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_data_scopes (user_id, scope_type, contabilidade_id) 
    SELECT u.id, 'company', u.company_id FROM users_enhanced u WHERE u.user_type = 'contabilidade'
    ON CONFLICT DO NOTHING;

    INSERT INTO user_data_scopes (user_id, scope_type, empresa_id, contabilidade_id) 
    SELECT u.id, 'enterprise', u.company_id, c.parent_company_id 
    FROM users_enhanced u 
    JOIN companies c ON u.company_id = c.id 
    WHERE u.user_type = 'cliente_final'
    ON CONFLICT DO NOTHING;
    """

    return data_sql


async def run_migration():
    """Execute the complete migration"""
    print("🚀 Starting Enhanced Authentication Migration...")

    try:
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to database")

        # Create tables
        print("📋 Creating enhanced tables...")
        migration_sql = await create_enhanced_user_tables()
        await conn.execute(migration_sql)
        print("✅ Tables created successfully")

        # Insert initial data
        print("📊 Inserting initial data...")
        data_sql = await insert_initial_data()
        await conn.execute(data_sql)
        print("✅ Initial data inserted successfully")

        # Verify installation
        user_count = await conn.fetchval("SELECT COUNT(*) FROM users_enhanced")
        company_count = await conn.fetchval("SELECT COUNT(*) FROM companies")

        print(f"✅ Migration completed successfully!")
        print(f"   - Created {user_count} test users")
        print(f"   - Created {company_count} companies")
        print(f"   - Enhanced security tables are ready")

        await conn.close()

    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise


async def rollback_migration():
    """Rollback the migration (for development/testing)"""
    print("🔄 Rolling back Enhanced Authentication Migration...")

    rollback_sql = """
    DROP TABLE IF EXISTS user_sessions CASCADE;
    DROP TABLE IF EXISTS access_audit_log CASCADE;
    DROP TABLE IF EXISTS user_data_scopes CASCADE;
    DROP TABLE IF EXISTS user_permissions CASCADE;
    DROP TABLE IF EXISTS user_roles CASCADE;
    DROP TABLE IF EXISTS users_enhanced CASCADE;
    DROP TABLE IF EXISTS companies CASCADE;
    DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
    """

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(rollback_sql)
        print("✅ Rollback completed successfully")
        await conn.close()

    except Exception as e:
        print(f"❌ Rollback failed: {str(e)}")
        raise


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        asyncio.run(rollback_migration())
    else:
        asyncio.run(run_migration())
