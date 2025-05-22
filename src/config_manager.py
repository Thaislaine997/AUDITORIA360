import json
import os
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException

import logging
logger = logging.getLogger(__name__)

CONFIG_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_BASE_PATH, "config.json")
CLIENT_CONFIGS_DIR = os.path.join(CONFIG_BASE_PATH, "client_configs")

class ConfigManager:
    def __init__(self):
        self.base_config: Dict[str, Any] = self._load_json(DEFAULT_CONFIG_FILE)
        if not self.base_config:
            logger.warning(f"Falha ao carregar configuração base de {DEFAULT_CONFIG_FILE}. Usando config vazia.")
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

    def _get_client_id_from_request(self, request: Request) -> Optional[str]:
        if request is None:
            logger.warning("_get_client_id_from_request chamado com request None")
            return None
        if not hasattr(request, 'headers'):
            logger.warning("_get_client_id_from_request chamado com request sem atributo 'headers'")
            return None

        header_client_id = request.headers.get("X-Client-ID")
        if header_client_id:
            client_config_file = os.path.join(CLIENT_CONFIGS_DIR, f"{header_client_id}.json")
            if os.path.exists(client_config_file):
                logger.debug(f"Client ID from header: {header_client_id}, file exists: {client_config_file}")
                return header_client_id
            else:
                logger.warning(f"X-Client-ID '{header_client_id}' fornecido, mas arquivo de configuração '{client_config_file}' não encontrado.")
                return None
        
        logger.debug("Nenhum X-Client-ID no header.")
        return None

    def get_config(self, request: Request) -> Dict[str, Any]:
        if request is None:
            logger.error("get_config chamado com request None. Isso é um erro do chamador.")
            raise ValueError("Request não pode ser None para get_config")

        logger.debug(f"get_config chamado. Request path: {getattr(request.url, 'path', 'N/A')}, Headers: {dict(request.headers)}")
        client_id_str = self._get_client_id_from_request(request)
        logger.debug(f"Client ID from _get_client_id_from_request: {client_id_str}")

        if client_id_str is None:
            header_value = request.headers.get("X-Client-ID")
            if not header_value:
                logger.warning("Tentativa de acesso sem X-Client-ID header válido.")
                raise HTTPException(status_code=401, detail="X-Client-ID header ausente ou inválido.")
            else:
                logger.warning(f"X-Client-ID '{header_value}' fornecido, mas configuração do cliente não encontrada ou inválida.")
                raise HTTPException(status_code=401, detail=f"Client ID '{header_value}' inválido ou configuração não encontrada.")

        if client_id_str in self.client_configs_cache:
            cached_config = self.client_configs_cache[client_id_str]
            if "client_id" in cached_config and cached_config["client_id"] == client_id_str:
                logger.debug(f"Retornando config do cache para client_id: {client_id_str}")
                return cached_config
            logger.warning(f"Cache para {client_id_str} inválido ou não continha 'client_id' correto. Reconstruindo.")

        client_config_path = os.path.join(CLIENT_CONFIGS_DIR, f"{client_id_str}.json")
        client_specific_config = self._load_json(client_config_path)
        logger.debug(f"Client specific config para '{client_id_str}' de '{client_config_path}': {client_specific_config}")

        if not client_specific_config and not os.path.exists(client_config_path):
            logger.error(f"Arquivo de configuração para cliente '{client_id_str}' não encontrado em {client_config_path} (verificação tardia).")
            raise HTTPException(status_code=500, detail=f"Erro interno: Configuração do cliente '{client_id_str}' desapareceu.")

        merged_config = self.base_config.copy()
        logger.debug(f"Base config copiado para merged_config (antes de update): {merged_config}")
        merged_config.update(client_specific_config)
        logger.debug(f"Merged_config após update com client_specific_config: {merged_config}")
        
        merged_config["client_id"] = client_id_str 
        logger.debug(f"Client_id '{client_id_str}' adicionado/atualizado em merged_config. merged_config agora: {merged_config}")

        current_required_keys = list(self.base_config.get("required_keys_for_api", ["gcp_project_id", "control_bq_dataset_id"]))
        if "client_id" not in current_required_keys:
            current_required_keys.append("client_id")
        
        logger.debug(f"Verificando chaves obrigatórias: {current_required_keys} em merged_config: {merged_config}")

        missing_keys = [key for key in current_required_keys if key not in merged_config or not merged_config[key]]

        if missing_keys:
            error_detail = f"Configuração incompleta para o cliente '{client_id_str}'. Chaves ausentes ou vazias: {', '.join(missing_keys)}. Config atual: {merged_config}"
            logger.error(f"ERRO DE CONFIGURAÇÃO: {error_detail}")
            raise HTTPException(status_code=500, detail=f"Erro interno de configuração do servidor para o cliente '{client_id_str}'.")

        logger.info(f"Configuração final para client_id '{client_id_str}': {merged_config}")
        self.client_configs_cache[client_id_str] = merged_config.copy()
        return merged_config

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

