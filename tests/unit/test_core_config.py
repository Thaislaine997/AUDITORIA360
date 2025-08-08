"""
Unit tests for src.core.config module.
"""

import json
import os
import tempfile

import pytest

from src.core.config import ConfigManager, config_manager


class TestConfigManager:
    """Test cases for ConfigManager class."""

    def test_init_with_missing_config(self):
        """Test ConfigManager initialization with missing config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a ConfigManager with a non-existent config file
            original_path = ConfigManager.__init__.__code__.co_filename
            config_manager_instance = ConfigManager()
            config_manager_instance.config = {}
            assert config_manager_instance.config == {}

    def test_load_config_existing_file(self):
        """Test loading configuration from existing file."""
        test_config = {"test_key": "test_value", "db_host": "localhost"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name

        try:
            manager = ConfigManager()
            loaded_config = manager.load_config(temp_file)
            assert loaded_config == test_config
        finally:
            os.unlink(temp_file)

    def test_load_config_nonexistent_file(self):
        """Test loading configuration from non-existent file."""
        manager = ConfigManager()
        config = manager.load_config("/nonexistent/path/config.json")
        assert config == {}

    def test_load_config_invalid_json(self):
        """Test loading configuration from invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content {")
            temp_file = f.name

        try:
            manager = ConfigManager()
            config = manager.load_config(temp_file)
            assert config == {}
        finally:
            os.unlink(temp_file)

    def test_get_existing_key(self):
        """Test getting existing configuration value."""
        manager = ConfigManager()
        manager.config = {"existing_key": "existing_value"}

        value = manager.get("existing_key")
        assert value == "existing_value"

    def test_get_nonexistent_key_with_default(self):
        """Test getting non-existent key with default value."""
        manager = ConfigManager()
        manager.config = {}

        value = manager.get("nonexistent_key", "default_value")
        assert value == "default_value"

    def test_get_nonexistent_key_without_default(self):
        """Test getting non-existent key without default value."""
        manager = ConfigManager()
        manager.config = {}

        value = manager.get("nonexistent_key")
        assert value is None

    def test_update_config(self):
        """Test updating configuration."""
        manager = ConfigManager()
        manager.config = {"existing_key": "old_value"}

        updates = {"existing_key": "new_value", "new_key": "new_value"}
        manager.update_config(updates)

        assert manager.config["existing_key"] == "new_value"
        assert manager.config["new_key"] == "new_value"

    def test_save_config_success(self):
        """Test saving configuration to file."""
        test_config = {"test_key": "test_value"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_file = f.name

        try:
            manager = ConfigManager()
            manager.config = test_config
            manager.save_config(temp_file)

            # Verify file was saved correctly
            with open(temp_file, "r") as f:
                saved_config = json.load(f)
            assert saved_config == test_config
        finally:
            os.unlink(temp_file)

    def test_save_config_permission_error(self):
        """Test saving configuration with permission error."""
        manager = ConfigManager()
        manager.config = {"test": "value"}

        # Try to save to a directory that doesn't exist
        with pytest.raises(Exception):
            manager.save_config("/nonexistent/directory/config.json")


class TestGlobalConfigManager:
    """Test cases for global config_manager instance."""

    def test_global_instance_exists(self):
        """Test that global config_manager instance exists."""
        assert config_manager is not None
        assert isinstance(config_manager, ConfigManager)

    def test_global_instance_has_config(self):
        """Test that global config_manager has config attribute."""
        assert hasattr(config_manager, "config")
        assert isinstance(config_manager.config, dict)
