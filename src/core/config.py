"""
Central configuration management for AUDITORIA360.
Consolidated from services/core/config_manager.py
"""

import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger(__name__)

CONFIG_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_BASE_PATH, "config.json")
CLIENT_CONFIGS_DIR = os.path.join(CONFIG_BASE_PATH, "client_configs")


class ConfigManager:
    """Central configuration manager for the application."""

    def __init__(self):
        self.config = self.load_config(DEFAULT_CONFIG_FILE)

    def load_config(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not os.path.exists(file_path):
            logger.warning(f"Config file not found: {file_path}")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config from {file_path}: {e}")
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self.config.get(key, default)

    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        self.config.update(updates)

    def save_config(self, file_path: str = None) -> None:
        """Save configuration to file."""
        path = file_path or DEFAULT_CONFIG_FILE
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving config to {path}: {e}")
            raise


# Global config instance
config_manager = ConfigManager()
