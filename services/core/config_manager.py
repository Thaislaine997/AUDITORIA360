import json
import os
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
import uuid
import logging
logger = logging.getLogger(__name__)

CONFIG_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_BASE_PATH, "config.json")
CLIENT_CONFIGS_DIR = os.path.join(CONFIG_BASE_PATH, "client_configs")

class ConfigManager:
    def __init__(self):
        self.config = self.load_config(DEFAULT_CONFIG_FILE)

    def load_config(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail=f"Config file not found: {file_path}")
        with open(file_path, "r") as file:
            return json.load(file)

    def get_client_config(self, client_id: str) -> Dict[str, Any]:
        client_config_file = os.path.join(CLIENT_CONFIGS_DIR, f"{client_id}.json")
        if not os.path.exists(client_config_file):
            raise HTTPException(status_code=404, detail=f"Client config not found: {client_id}")
        with open(client_config_file, "r") as file:
            return json.load(file)

    def save_client_config(self, client_id: str, config_data: Dict[str, Any]):
        client_config_file = os.path.join(CLIENT_CONFIGS_DIR, f"{client_id}.json")
        with open(client_config_file, "w") as file:
            json.dump(config_data, file, indent=4)

config_manager = ConfigManager()

def get_current_config(request: Request) -> Dict[str, Any]:
    client_id = request.headers.get("X-Client-ID")
    if not client_id:
        raise HTTPException(status_code=400, detail="X-Client-ID header missing")
    return config_manager.get_client_config(client_id)

def get_background_task_config(client_id: str) -> Dict[str, Any]:
    config = config_manager.get_client_config(client_id)
    return config.get("background_tasks", {})
