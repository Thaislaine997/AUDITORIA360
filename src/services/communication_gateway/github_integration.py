"""
GitHub Integration Service for AUDITORIA360
Integração com GitHub para criação automática de Issues
"""

from typing import Dict, List, Optional, Any
import logging
import requests
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class GitHubIntegrationService:
    """
    Serviço para integração com GitHub API
    Cria Issues automaticamente a partir de mensagens recebidas
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Configurações do GitHub
        self.github_token = self.config.get("github_token")
        self.repo_owner = self.config.get("repo_owner") 
        self.repo_name = self.config.get("repo_name")
        self.base_url = "https://api.github.com"
        
        logger.info("GitHubIntegrationService initialized")
    
    def is_configured(self) -> bool:
        """Verifica se o serviço está configurado corretamente"""
        required_configs = ["github_token", "repo_owner", "repo_name"]
        return all(self.config.get(key) for key in required_configs)
    
    def create_issue_from_message(
        self, 
        message_data: Dict[str, Any],
        provider: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Cria uma Issue no GitHub a partir de dados de mensagem
        
        Args:
            message_data: Dados da mensagem recebida
            provider: Nome do provedor que recebeu a mensagem
            
        Returns:
            Dict com resultado da criação da Issue
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "GitHub integration not configured"
            }
        
        try:
            # Extrai informações da mensagem
            from_number = message_data.get("from_number", "unknown")
            body = message_data.get("body", "")
            message_type = message_data.get("type", "unknown")
            timestamp = message_data.get("timestamp", datetime.now().isoformat())
            
            # Define título e conteúdo da Issue
            title = f"Nova mensagem via {provider.title()} - {message_type.upper()}"
            
            issue_body = self._build_issue_body(
                from_number=from_number,
                message_body=body,
                message_type=message_type,
                provider=provider,
                timestamp=timestamp,
                original_data=message_data
            )
            
            # Define labels baseadas no provedor e tipo
            labels = self._get_labels_for_message(provider, message_type)
            
            # Dados da Issue
            issue_data = {
                "title": title,
                "body": issue_body,
                "labels": labels
            }
            
            # Faz a requisição para criar a Issue
            response = self._create_github_issue(issue_data)
            
            if response["success"]:
                logger.info(f"GitHub Issue created successfully: {response['issue_url']}")
                return {
                    "success": True,
                    "issue_number": response["issue_number"],
                    "issue_url": response["issue_url"],
                    "message": "Issue created successfully"
                }
            else:
                logger.error(f"Failed to create GitHub Issue: {response['error']}")
                return response
                
        except Exception as e:
            logger.error(f"Error creating GitHub Issue: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_issue_body(
        self,
        from_number: str,
        message_body: str,
        message_type: str,
        provider: str,
        timestamp: str,
        original_data: Dict[str, Any]
    ) -> str:
        """Constrói o corpo da Issue com as informações da mensagem"""
        
        body_template = f"""## Nova Mensagem Recebida via {provider.title()}

### Informações da Mensagem
- **Tipo**: {message_type.upper()}
- **Número de Origem**: {from_number}
- **Data/Hora**: {timestamp}
- **Provedor**: {provider}

### Conteúdo da Mensagem
```
{message_body}
```

### Dados Técnicos
```json
{json.dumps(original_data, indent=2, ensure_ascii=False)}
```

---
*Esta Issue foi criada automaticamente pelo sistema AUDITORIA360 através do Gateway de Comunicação.*
"""
        return body_template
    
    def _get_labels_for_message(self, provider: str, message_type: str) -> List[str]:
        """
        Determina as labels apropriadas para a Issue baseada no provedor e tipo
        
        Args:
            provider: Nome do provedor
            message_type: Tipo da mensagem
            
        Returns:
            Lista de labels para a Issue
        """
        labels = ["mensagem-recebida", "gateway-comunicacao"]
        
        # Labels específicas por provedor
        if provider.lower() == "twilio":
            if message_type.lower() == "whatsapp":
                labels.append("via-twilio-whatsapp")
            elif message_type.lower() == "sms":
                labels.append("via-twilio-sms")
            else:
                labels.append("via-twilio")
        elif provider.lower() == "email":
            labels.append("via-email")
        
        return labels
    
    def _create_github_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz a requisição HTTP para criar a Issue no GitHub
        
        Args:
            issue_data: Dados da Issue (title, body, labels)
            
        Returns:
            Dict com resultado da operação
        """
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
            
            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=issue_data)
            
            if response.status_code == 201:
                issue_response = response.json()
                return {
                    "success": True,
                    "issue_number": issue_response["number"],
                    "issue_url": issue_response["html_url"],
                    "api_response": issue_response
                }
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def send_response_message(
        self, 
        issue_number: int,
        response_message: str = None
    ) -> Dict[str, Any]:
        """
        Envia uma mensagem de confirmação de recebimento
        (Esta função pode ser usada para responder automaticamente)
        
        Args:
            issue_number: Número da Issue criada
            response_message: Mensagem personalizada de resposta
            
        Returns:
            Dict com dados da mensagem de resposta
        """
        if response_message is None:
            response_message = (
                f"Mensagem recebida com sucesso! "
                f"Sua solicitação foi registrada como Issue #{issue_number} "
                f"no sistema AUDITORIA360. Nossa equipe entrará em contato em breve."
            )
        
        return {
            "response_message": response_message,
            "issue_number": issue_number,
            "auto_generated": True
        }