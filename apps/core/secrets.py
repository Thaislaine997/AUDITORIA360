"""
Secure Secrets Management for AUDITORIA360
Handles credentials securely with fallback mechanisms
"""

import os
import secrets
import string
from typing import Dict, Optional
import boto3
import json
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class SecretsManager:
    """Secure secrets management with AWS Secrets Manager integration"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.secret_name = os.getenv("SECRET_MANAGER_SECRET_NAME", "auditoria360/credentials")
        
    def generate_secure_password(self, length: int = 16) -> str:
        """Generate a cryptographically secure password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def get_secret_from_aws(self, secret_name: str) -> Optional[Dict]:
        """Retrieve secrets from AWS Secrets Manager"""
        try:
            if self.environment == "production":
                session = boto3.session.Session()
                client = session.client(
                    service_name='secretsmanager',
                    region_name=self.aws_region
                )
                
                response = client.get_secret_value(SecretId=secret_name)
                return json.loads(response['SecretString'])
            else:
                logger.info("Development environment - using environment variables")
                return None
                
        except Exception as e:
            logger.warning(f"Failed to retrieve from AWS Secrets Manager: {e}")
            return None
    
    @lru_cache(maxsize=1)
    def get_default_passwords(self) -> Dict[str, str]:
        """Get default passwords with secure fallbacks"""
        
        # Try AWS Secrets Manager first for production
        if self.environment == "production":
            aws_secrets = self.get_secret_from_aws(self.secret_name)
            if aws_secrets:
                return {
                    "admin": aws_secrets.get("admin_password"),
                    "gestor_a": aws_secrets.get("gestor_a_password"),
                    "gestor_b": aws_secrets.get("gestor_b_password"),
                    "client_x": aws_secrets.get("client_x_password"),
                }
        
        # Fallback to environment variables with validation
        passwords = {
            "admin": os.getenv("DEFAULT_ADMIN_PASSWORD"),
            "gestor_a": os.getenv("DEFAULT_GESTOR_A_PASSWORD"), 
            "gestor_b": os.getenv("DEFAULT_GESTOR_B_PASSWORD"),
            "client_x": os.getenv("DEFAULT_CLIENT_X_PASSWORD"),
        }
        
        # Validate that no default passwords are being used
        for key, password in passwords.items():
            if not password or password.startswith("changeme"):
                if self.environment == "production":
                    raise ValueError(f"Production environment requires secure {key} password")
                else:
                    # Generate secure password for development
                    passwords[key] = self.generate_secure_password()
                    logger.warning(f"Generated secure password for {key} - change in production")
        
        return passwords
    
    def get_database_url(self) -> str:
        """Get database URL with validation"""
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is required")
            
        # Check for default/insecure values
        if "user:password@localhost" in db_url:
            if self.environment == "production":
                raise ValueError("Production environment requires secure database credentials")
            logger.warning("Using default database URL - change for production")
        
        return db_url
    
    def get_secret_key(self) -> str:
        """Get JWT secret key with validation"""
        secret_key = os.getenv("SECRET_KEY")
        
        if not secret_key:
            if self.environment == "production":
                raise ValueError("SECRET_KEY environment variable is required in production")
            else:
                # Generate secure key for development
                secret_key = secrets.token_urlsafe(32)
                logger.warning("Generated temporary secret key - set SECRET_KEY environment variable")
        
        if len(secret_key) < 32:
            if self.environment == "production":
                raise ValueError("SECRET_KEY must be at least 32 characters in production")
            logger.warning("SECRET_KEY should be at least 32 characters")
        
        return secret_key


# Global instance
secrets_manager = SecretsManager()