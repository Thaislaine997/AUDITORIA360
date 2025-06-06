import json
import os
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
import uuid # For potential client_id format validation if needed later

import logging
logger = logging.getLogger(__name__)

CONFIG_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_BASE_PATH, "config.json")
CLIENT_CONFIGS_DIR = os.path.join(CONFIG_BASE_PATH, "client_configs")

class ConfigManager:
    def __init__(self):
        self.base_config: Dict[str, Any] = self._load_json(DEFAULT_CONFIG_FILE)
        if not self.base_config:
            logger.critical(f"Falha ao carregar configuração base de {DEFAULT_CONFIG_FILE}. O sistema pode não funcionar corretamente.")
            # Consider raising an exception here or ensuring base_config has a minimal valid structure
            self.base_config = {}
        self.client_configs_cache: Dict[str, Dict[str, Any]] = {}
        logger.info(f"ConfigManager inicializado. Base config: {self.base_config}")
        logger.info(f"Client configs directory: {CLIENT_CONFIGS_DIR}")

    def _load_json(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.info(f"Arquivo de configuração não encontrado: {file_path}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON no arquivo: {file_path}")
            return {}

    def _validate_config(self, config: Dict[str, Any], client_id: str) -> None:
        """Valida se a configuração mesclada contém todas as chaves obrigatórias."""
        current_required_keys = list(self.base_config.get("required_keys_for_api", [
            "gcp_project_id", 
            "control_bq_dataset_id",
            # Adicione outras chaves que são universalmente necessárias aqui
        ]))
        # Adiciona 'client_id' às chaves obrigatórias se não estiver presente, 
        # pois é fundamental para a lógica de multi-tenancy.
        if "client_id" not in current_required_keys:
            current_required_keys.append("client_id")
        
        logger.debug(f"Verificando chaves obrigatórias: {current_required_keys} em config para client_id: {client_id}")

        missing_keys = [key for key in current_required_keys if key not in config or not config[key]]

        if missing_keys:
            error_detail = f"Configuração incompleta para o cliente '{client_id}'. Chaves ausentes ou vazias: {', '.join(missing_keys)}. Config fornecida: {config}"
            logger.error(f"ERRO DE CONFIGURAÇÃO: {error_detail}")
            # Esta exceção será capturada por quem chamou a validação
            raise ValueError(f"Erro interno de configuração do servidor para o cliente '{client_id}'. Chaves ausentes: {missing_keys}")

    def get_config_for_client_id(self, client_id_str: str) -> Dict[str, Any]:
        """Carrega, mescla e valida a configuração para um client_id específico."""
        if not client_id_str or not isinstance(client_id_str, str):
            logger.error(f"Tentativa de obter configuração com client_id inválido: {client_id_str}")
            raise ValueError("client_id_str deve ser uma string não vazia.")

        # Validar formato do client_id_str se necessário (ex: UUID)
        # try:
        #     uuid.UUID(client_id_str)
        # except ValueError:
        #     logger.warning(f"Formato de client_id '{client_id_str}' não é um UUID válido.")
        #     # Dependendo da política, pode-se levantar um erro aqui ou apenas logar.
        #     # raise ValueError(f"Formato de client_id '{client_id_str}' inválido.")

        if client_id_str in self.client_configs_cache:
            cached_config = self.client_configs_cache[client_id_str]
            # Verifica se o client_id no cache corresponde ao solicitado, para integridade do cache.
            if cached_config.get("client_id") == client_id_str:
                logger.debug(f"Retornando config do cache para client_id: {client_id_str}")
                return cached_config
            logger.warning(f"Cache para {client_id_str} inválido (client_id não correspondia). Reconstruindo.")

        client_config_path = os.path.join(CLIENT_CONFIGS_DIR, f"{client_id_str}.json")
        client_specific_config = self._load_json(client_config_path)

        if not client_specific_config and not os.path.exists(client_config_path):
            logger.warning(f"Arquivo de configuração para cliente '{client_id_str}' não encontrado em {client_config_path}.")
            # Decide se isso é um erro fatal ou se pode prosseguir com config base + client_id apenas
            # Por agora, vamos considerar um erro se o arquivo específico do cliente não existir.
            raise FileNotFoundError(f"Configuração para cliente '{client_id_str}' não encontrada.")

        merged_config = self.base_config.copy()
        merged_config.update(client_specific_config) # Sobrescreve chaves da base com as específicas do cliente
        merged_config["client_id"] = client_id_str # Garante que o client_id está na config final

        try:
            self._validate_config(merged_config, client_id_str)
        except ValueError as e_val:
            # Re-levanta como HTTPException para ser tratado pelo FastAPI se originado de um request
            # Ou pode ser capturado internamente se chamado por um background task.
            raise HTTPException(status_code=500, detail=str(e_val))

        logger.info(f"Configuração carregada e validada para client_id '{client_id_str}': {merged_config}")
        self.client_configs_cache[client_id_str] = merged_config.copy() # Armazena uma cópia no cache
        return merged_config

    def _get_client_id_from_request(self, request: Request) -> Optional[str]:
        if request is None:
            logger.warning("_get_client_id_from_request chamado com request None")
            return None
        # Removida a checagem de hasattr(request, 'headers') pois Request sempre terá.

        header_client_id = request.headers.get("X-Client-ID")
        if not header_client_id:
            logger.debug("Nenhum X-Client-ID no header.")
            return None
        
        # Validação básica do client_id do header (ex: não vazio)
        # Poderia adicionar validação de formato aqui também se desejado.
        if not isinstance(header_client_id, str) or not header_client_id.strip():
            logger.warning(f"X-Client-ID header presente mas vazio ou tipo inválido: '{header_client_id}'")
            return None
        
        # A verificação da existência do arquivo de configuração foi movida para get_config_for_client_id
        # Aqui, apenas retornamos o ID se ele estiver presente e parecer válido.
        logger.debug(f"Client ID from header: {header_client_id}")
        return header_client_id.strip()

    def get_config(self, request: Request) -> Dict[str, Any]:
        if request is None:
            logger.error("get_config chamado com request None. Isso é um erro do chamador.")
            # Levanta ValueError que será convertido em 400 Bad Request por get_current_config
            raise ValueError("Request não pode ser None para get_config")

        logger.debug(f"get_config chamado. Request path: {getattr(request.url, 'path', 'N/A')}")
        client_id_str = self._get_client_id_from_request(request)

        if not client_id_str:
            # Se _get_client_id_from_request não encontrou um client_id válido no header.
            logger.warning("Tentativa de acesso sem X-Client-ID header válido ou presente.")
            raise HTTPException(status_code=401, detail="X-Client-ID header ausente ou inválido.")

        try:
            return self.get_config_for_client_id(client_id_str)
        except FileNotFoundError:
            logger.warning(f"X-Client-ID '{client_id_str}' fornecido, mas arquivo de configuração não encontrado.")
            raise HTTPException(status_code=401, detail=f"Client ID '{client_id_str}' inválido ou configuração não encontrada.")
        # HTTPException de _validate_config (dentro de get_config_for_client_id) será propagada.
        # Outros ValueErrors de get_config_for_client_id (como client_id_str inválido) também podem ser tratados aqui se necessário.

config_manager = ConfigManager()

def get_current_config(request: Request) -> Dict[str, Any]:
    try:
        logger.debug(f"get_current_config chamado. Request path: {getattr(request.url, 'path', 'N/A')}, Headers: {dict(request.headers)}")
        config = config_manager.get_config(request)
        logger.debug(f"get_current_config: config_manager.get_config retornou: {config}")
        return config
    except HTTPException as e:
        logger.error(f"get_current_config: HTTPException capturada: status={e.status_code}, detail={e.detail}")
        raise
    except ValueError as ve:
        logger.error(f"get_current_config: ValueError capturado de get_config: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Erro inesperado em get_current_config: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno ao processar configuração.")

# Adicionar uma função para obter configuração para tarefas de background
def get_background_task_config(client_id: str) -> Dict[str, Any]:
    """
    Obtém a configuração para um client_id específico, destinado a tarefas de background
    que não têm um objeto Request.
    """
    if not client_id:
        logger.error("get_background_task_config chamado sem client_id.")
        raise ValueError("client_id é obrigatório para obter configuração de background task.")
    
    try:
        # config_manager é a instância global
        return config_manager.get_config_for_client_id(client_id)
    except FileNotFoundError as e_fnf:
        logger.error(f"Configuração para background task com client_id '{client_id}' não encontrada: {e_fnf}")
        # Decidir como lidar com isso. Pode ser uma exceção fatal para a task.
        raise # Re-levanta para ser tratada pelo chamador da background task
    except HTTPException as e_http:
        # Se get_config_for_client_id levantar HTTPException (ex: de _validate_config),
        # precisamos converter para um erro que faça sentido no contexto de background.
        logger.error(f"Erro de configuração (HTTPException) ao obter config para background task client '{client_id}': {e_http.detail}")
        raise ValueError(f"Erro de configuração para client '{client_id}': {e_http.detail}")
    except Exception as e:
        logger.error(f"Erro inesperado ao obter config para background task client '{client_id}': {e}", exc_info=True)
        raise

