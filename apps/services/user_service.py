"""
User Service Layer for AUDITORIA360
Encapsulates business logic for user and profile management.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from passlib.context import CryptContext

from src.core.constants import (
    CompanyTypes,
    DefaultCompanies,
    DefaultUsernames,
    EnvironmentVariables,
    ProfileNames,
    SecurityConstants,
    UserTypes,
)

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user and profile management operations"""

    def __init__(self):
        """Initialize the user service with password context"""
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=SecurityConstants.BCRYPT_ROUNDS,
        )

    def _get_secure_password(self, password_key: str) -> str:
        """
        Get secure password from environment variables.

        Args:
            password_key: Environment variable key for the password

        Returns:
            Secure password string

        Raises:
            ValueError: If password is not found in environment variables
        """
        password = os.getenv(password_key)
        if not password:
            raise ValueError(
                f"Password environment variable {password_key} not found. "
                "Please check your .env configuration."
            )
        return password

    def _hash_password(self, plain_password: str) -> str:
        """
        Hash a plain text password using bcrypt.

        Args:
            plain_password: Plain text password to hash

        Returns:
            Hashed password string
        """
        return self.pwd_context.hash(plain_password)

    def create_default_profiles(self) -> List[Dict[str, str]]:
        """
        Create default user profiles configuration.

        Returns:
            List of profile dictionaries with name and user_type
        """
        return [
            {
                "name": ProfileNames.SUPER_ADMIN,
                "user_type": UserTypes.SUPER_ADMIN,
                "description": "Administrador com acesso total ao sistema",
            },
            {
                "name": ProfileNames.CONTABILIDADE,
                "user_type": UserTypes.CONTABILIDADE,
                "description": "Escritório de contabilidade com acesso a múltiplos clientes",
            },
            {
                "name": ProfileNames.CLIENTE_FINAL,
                "user_type": UserTypes.CLIENTE_FINAL,
                "description": "Cliente final com acesso restrito aos próprios dados",
            },
            {
                "name": ProfileNames.GESTOR_A,
                "user_type": UserTypes.CONTABILIDADE,
                "description": "Gestor nível A com permissões administrativas",
            },
            {
                "name": ProfileNames.GESTOR_B,
                "user_type": UserTypes.CONTABILIDADE,
                "description": "Gestor nível B com permissões limitadas",
            },
        ]

    def create_super_admin_user(self) -> Dict[str, any]:
        """
        Create super administrator user configuration.

        Returns:
            Dictionary with super admin user data

        Raises:
            ValueError: If admin password environment variable is missing
        """
        admin_password = self._get_secure_password(
            EnvironmentVariables.DEFAULT_ADMIN_PASSWORD
        )

        return {
            "username": DefaultUsernames.ADMIN,
            "email": "admin@auditoria360.com",
            "full_name": "Administrador do Sistema",
            "password_hash": self._hash_password(admin_password),
            "user_type": UserTypes.SUPER_ADMIN,
            "company_id": None,  # Super admin não pertence a uma empresa específica
            "is_active": True,
            "created_at": datetime.utcnow(),
        }

    def create_test_companies(self) -> List[Dict[str, any]]:
        """
        Create test companies for development and demonstration.

        Returns:
            List of company dictionaries
        """
        return [
            {
                "id": DefaultCompanies.CONTAB_A_ID,
                "name": "Contabilidade Exemplo A Ltda",
                "company_type": CompanyTypes.CONTABILIDADE,
                "contact_email": "contato@contabilidade-exemplo-a.com",
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
            {
                "id": DefaultCompanies.CONTAB_B_ID,
                "name": "Contabilidade Exemplo B Ltda",
                "company_type": CompanyTypes.CONTABILIDADE,
                "contact_email": "contato@contabilidade-exemplo-b.com",
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
            {
                "id": DefaultCompanies.CLIENT_X_ID,
                "name": "Cliente Exemplo X S.A.",
                "company_type": CompanyTypes.CLIENTE,
                "contact_email": "contato@cliente-exemplo-x.com",
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
            {
                "id": DefaultCompanies.CLIENT_Y_ID,
                "name": "Cliente Exemplo Y Ltda",
                "company_type": CompanyTypes.CLIENTE,
                "contact_email": "contato@cliente-exemplo-y.com",
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
        ]

    def create_test_users(self) -> List[Dict[str, any]]:
        """
        Create test users for development and demonstration.

        Returns:
            List of user dictionaries

        Raises:
            ValueError: If any required password environment variable is missing
        """
        # Get secure passwords from environment variables
        gestor_a_password = self._get_secure_password(
            EnvironmentVariables.DEFAULT_GESTOR_A_PASSWORD
        )
        gestor_b_password = self._get_secure_password(
            EnvironmentVariables.DEFAULT_GESTOR_B_PASSWORD
        )
        client_x_password = self._get_secure_password(
            EnvironmentVariables.DEFAULT_CLIENT_X_PASSWORD
        )

        return [
            {
                "username": DefaultUsernames.GESTOR_A,
                "email": "gestor.a@contabilidade-exemplo-a.com",
                "full_name": "Gestor A - Contabilidade A",
                "password_hash": self._hash_password(gestor_a_password),
                "user_type": UserTypes.CONTABILIDADE,
                "company_id": DefaultCompanies.CONTAB_A_ID,
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
            {
                "username": DefaultUsernames.GESTOR_B,
                "email": "gestor.b@contabilidade-exemplo-b.com",
                "full_name": "Gestor B - Contabilidade B",
                "password_hash": self._hash_password(gestor_b_password),
                "user_type": UserTypes.CONTABILIDADE,
                "company_id": DefaultCompanies.CONTAB_B_ID,
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
            {
                "username": DefaultUsernames.CLIENT_X,
                "email": "cliente@cliente-exemplo-x.com",
                "full_name": "Cliente X - Usuário Principal",
                "password_hash": self._hash_password(client_x_password),
                "user_type": UserTypes.CLIENTE_FINAL,
                "company_id": DefaultCompanies.CLIENT_X_ID,
                "is_active": True,
                "created_at": datetime.utcnow(),
            },
        ]

    def validate_user_data(
        self, user_data: Dict[str, any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate user data before creation.

        Args:
            user_data: Dictionary containing user information

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = [
            "username",
            "email",
            "full_name",
            "password_hash",
            "user_type",
        ]

        for field in required_fields:
            if field not in user_data or not user_data[field]:
                return False, f"Campo obrigatório ausente: {field}"

        # Validate email format (basic validation)
        email = user_data["email"]
        if "@" not in email or "." not in email:
            return False, "Formato de email inválido"

        # Validate user type
        valid_user_types = [
            UserTypes.SUPER_ADMIN,
            UserTypes.CONTABILIDADE,
            UserTypes.CLIENTE_FINAL,
        ]
        if user_data["user_type"] not in valid_user_types:
            return False, f"Tipo de usuário inválido: {user_data['user_type']}"

        return True, None

    def validate_company_data(
        self, company_data: Dict[str, any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate company data before creation.

        Args:
            company_data: Dictionary containing company information

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ["id", "name", "company_type", "contact_email"]

        for field in required_fields:
            if field not in company_data or not company_data[field]:
                return False, f"Campo obrigatório ausente: {field}"

        # Validate company type
        valid_company_types = [CompanyTypes.CONTABILIDADE, CompanyTypes.CLIENTE]
        if company_data["company_type"] not in valid_company_types:
            return False, f"Tipo de empresa inválido: {company_data['company_type']}"

        return True, None

    def create_notification_templates(self) -> List[Dict[str, any]]:
        """
        Create default notification templates.

        Returns:
            List of notification template dictionaries
        """
        from src.core.constants import NotificationTemplates, NotificationTypes

        return [
            {
                "name": NotificationTemplates.WELCOME_USER,
                "subject": "Bem-vindo ao AUDITORIA360",
                "body_template": "Olá {{full_name}}, bem-vindo ao sistema AUDITORIA360! Seu usuário {{username}} foi criado com sucesso.",
                "template_type": NotificationTypes.EMAIL,
                "created_at": datetime.utcnow(),
            },
            {
                "name": NotificationTemplates.DOCUMENT_PROCESSED,
                "subject": "Documento Processado",
                "body_template": "O documento {{filename}} foi processado com sucesso. Status: {{status}}",
                "template_type": NotificationTypes.EMAIL,
                "created_at": datetime.utcnow(),
            },
            {
                "name": NotificationTemplates.AUDIT_ALERT,
                "subject": "Alerta de Auditoria",
                "body_template": "Foi detectada uma inconsistência no sistema: {{details}}. Por favor, verifique os dados.",
                "template_type": NotificationTypes.EMAIL,
                "created_at": datetime.utcnow(),
            },
            {
                "name": NotificationTemplates.PASSWORD_RESET,
                "subject": "Redefinição de Senha",
                "body_template": "Solicitação de redefinição de senha para o usuário {{username}}. Use o código: {{reset_code}}",
                "template_type": NotificationTypes.EMAIL,
                "created_at": datetime.utcnow(),
            },
        ]

    def log_action(
        self, user_id: Optional[int], action: str, details: Dict[str, any] = None
    ) -> Dict[str, any]:
        """
        Create an audit log entry for user actions.

        Args:
            user_id: ID of the user performing the action
            action: Action being performed
            details: Additional details about the action

        Returns:
            Dictionary with audit log data
        """
        return {
            "user_id": user_id,
            "action": action,
            "details": details or {},
            "timestamp": datetime.utcnow(),
            "ip_address": None,  # Will be filled by the calling context
        }
