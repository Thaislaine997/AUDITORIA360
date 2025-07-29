"""
MCP Configuration Management for AUDITORIA360
Handles configuration for MCP servers, clients, and development environment
"""

import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

from .protocol import MCPVersion


class MCPTransportType(str, Enum):
    """Supported MCP transport types"""

    HTTP = "http"
    WEBSOCKET = "websocket"
    STDIO = "stdio"
    TCP = "tcp"


class MCPServerConfig(BaseModel):
    """Configuration for an MCP server"""

    name: str
    description: Optional[str] = None
    transport: MCPTransportType
    host: Optional[str] = "localhost"
    port: Optional[int] = None
    path: Optional[str] = None
    command: Optional[str] = None  # For stdio transport
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    timeout: int = 30
    auto_start: bool = True
    enabled: bool = True


class MCPClientConfig(BaseModel):
    """Configuration for an MCP client"""

    name: str
    target_server: str
    auto_connect: bool = True
    retry_attempts: int = 3
    retry_delay: int = 5
    enabled: bool = True


class MCPDevelopmentConfig(BaseModel):
    """Development environment configuration for MCP"""

    debug_mode: bool = False
    log_level: str = "INFO"
    log_file: Optional[str] = None
    enable_metrics: bool = True
    metrics_port: int = 9090
    enable_health_checks: bool = True
    health_check_interval: int = 60


class CopilotIntegrationConfig(BaseModel):
    """Configuration for GitHub Copilot integration"""

    enabled: bool = True
    mcp_server_url: Optional[str] = None
    tools_enabled: List[str] = Field(default_factory=list)
    resources_enabled: List[str] = Field(default_factory=list)
    context_window_size: int = 8000
    max_tool_calls_per_request: int = 5
    enable_streaming: bool = True


class MCPConfiguration(BaseModel):
    """Main MCP configuration"""

    version: str = "1.0.0"
    protocol_version: MCPVersion = MCPVersion.V1_0

    # Server configurations
    servers: Dict[str, MCPServerConfig] = Field(default_factory=dict)

    # Client configurations
    clients: Dict[str, MCPClientConfig] = Field(default_factory=dict)

    # Development settings
    development: MCPDevelopmentConfig = Field(default_factory=MCPDevelopmentConfig)

    # Copilot integration
    copilot: CopilotIntegrationConfig = Field(default_factory=CopilotIntegrationConfig)

    # Security settings
    security: Dict[str, Any] = Field(default_factory=dict)

    # Feature flags
    features: Dict[str, bool] = Field(default_factory=dict)


class MCPConfigManager:
    """Manages MCP configuration loading, saving, and validation"""

    def __init__(self, config_dir: str = None):
        self.config_dir = Path(
            config_dir or os.path.join(os.getcwd(), "configs", "mcp")
        )
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / "mcp_config.yaml"
        self.servers_dir = self.config_dir / "servers"
        self.clients_dir = self.config_dir / "clients"

        # Create subdirectories
        self.servers_dir.mkdir(exist_ok=True)
        self.clients_dir.mkdir(exist_ok=True)

        self._config: Optional[MCPConfiguration] = None

    def load_config(self) -> MCPConfiguration:
        """Load MCP configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f)

                self._config = MCPConfiguration.model_validate(config_data)

                # Load additional server configurations
                self._load_server_configs()

                # Load additional client configurations
                self._load_client_configs()

                return self._config

            except Exception as e:
                print(f"Error loading MCP configuration: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()

    def save_config(self, config: MCPConfiguration = None):
        """Save MCP configuration to file"""
        if config:
            self._config = config

        if not self._config:
            raise ValueError("No configuration to save")

        try:
            config_data = self._config.model_dump()

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

            # Save individual server configurations
            self._save_server_configs()

            # Save individual client configurations
            self._save_client_configs()

            print(f"MCP configuration saved to {self.config_file}")

        except Exception as e:
            print(f"Error saving MCP configuration: {e}")
            raise

    def _load_server_configs(self):
        """Load individual server configuration files"""
        for config_file in self.servers_dir.glob("*.yaml"):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    server_data = yaml.safe_load(f)

                server_config = MCPServerConfig.model_validate(server_data)
                self._config.servers[server_config.name] = server_config

            except Exception as e:
                print(f"Error loading server config {config_file}: {e}")

    def _load_client_configs(self):
        """Load individual client configuration files"""
        for config_file in self.clients_dir.glob("*.yaml"):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    client_data = yaml.safe_load(f)

                client_config = MCPClientConfig.model_validate(client_data)
                self._config.clients[client_config.name] = client_config

            except Exception as e:
                print(f"Error loading client config {config_file}: {e}")

    def _save_server_configs(self):
        """Save individual server configuration files"""
        for name, server_config in self._config.servers.items():
            config_file = self.servers_dir / f"{name}.yaml"
            try:
                with open(config_file, "w", encoding="utf-8") as f:
                    yaml.dump(server_config.model_dump(), f, default_flow_style=False)
            except Exception as e:
                print(f"Error saving server config {name}: {e}")

    def _save_client_configs(self):
        """Save individual client configuration files"""
        for name, client_config in self._config.clients.items():
            config_file = self.clients_dir / f"{name}.yaml"
            try:
                with open(config_file, "w", encoding="utf-8") as f:
                    yaml.dump(client_config.model_dump(), f, default_flow_style=False)
            except Exception as e:
                print(f"Error saving client config {name}: {e}")

    def _get_default_config(self) -> MCPConfiguration:
        """Get default MCP configuration"""
        config = MCPConfiguration()

        # Add default AUDITORIA360 MCP server
        auditoria_server = MCPServerConfig(
            name="auditoria360-main",
            description="Main AUDITORIA360 MCP server for payroll and compliance tools",
            transport=MCPTransportType.HTTP,
            host="localhost",
            port=8001,
            path="/mcp",
            enabled=True,
        )
        config.servers["auditoria360-main"] = auditoria_server

        # Add default client for self-connection
        auditoria_client = MCPClientConfig(
            name="auditoria360-client",
            target_server="auditoria360-main",
            auto_connect=True,
            enabled=True,
        )
        config.clients["auditoria360-client"] = auditoria_client

        # Configure Copilot integration
        config.copilot.enabled = True
        config.copilot.tools_enabled = [
            "payroll_calculator",
            "compliance_checker",
            "document_analyzer",
            "audit_executor",
            "cct_comparator",
        ]
        config.copilot.resources_enabled = [
            "auditoria://payroll/data",
            "auditoria://employees/info",
            "auditoria://cct/documents",
            "auditoria://compliance/rules",
            "auditoria://knowledge/base",
        ]

        # Set feature flags
        config.features = {
            "enable_caching": True,
            "enable_compression": True,
            "enable_encryption": False,
            "enable_rate_limiting": True,
            "enable_analytics": True,
        }

        # Set security configuration
        config.security = {
            "require_authentication": False,
            "allowed_origins": ["*"],
            "max_request_size": 10485760,  # 10MB
            "rate_limit_requests_per_minute": 100,
        }

        self._config = config
        return config

    def get_config(self) -> MCPConfiguration:
        """Get current configuration"""
        if not self._config:
            return self.load_config()
        return self._config

    def add_server(self, server_config: MCPServerConfig):
        """Add a new server configuration"""
        if not self._config:
            self.load_config()

        self._config.servers[server_config.name] = server_config
        self.save_config()

    def add_client(self, client_config: MCPClientConfig):
        """Add a new client configuration"""
        if not self._config:
            self.load_config()

        self._config.clients[client_config.name] = client_config
        self.save_config()

    def remove_server(self, name: str):
        """Remove a server configuration"""
        if not self._config:
            self.load_config()

        if name in self._config.servers:
            del self._config.servers[name]

            # Remove config file
            config_file = self.servers_dir / f"{name}.yaml"
            if config_file.exists():
                config_file.unlink()

            self.save_config()

    def remove_client(self, name: str):
        """Remove a client configuration"""
        if not self._config:
            self.load_config()

        if name in self._config.clients:
            del self._config.clients[name]

            # Remove config file
            config_file = self.clients_dir / f"{name}.yaml"
            if config_file.exists():
                config_file.unlink()

            self.save_config()

    def validate_config(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []

        if not self._config:
            errors.append("No configuration loaded")
            return errors

        # Validate server configurations
        for name, server_config in self._config.servers.items():
            if server_config.transport == MCPTransportType.HTTP:
                if not server_config.host or not server_config.port:
                    errors.append(
                        f"Server {name}: HTTP transport requires host and port"
                    )
            elif server_config.transport == MCPTransportType.STDIO:
                if not server_config.command:
                    errors.append(f"Server {name}: STDIO transport requires command")

        # Validate client configurations
        for name, client_config in self._config.clients.items():
            if client_config.target_server not in self._config.servers:
                errors.append(
                    f"Client {name}: target server '{client_config.target_server}' not found"
                )

        return errors

    def generate_copilot_config(self) -> Dict[str, Any]:
        """Generate GitHub Copilot configuration for MCP integration"""
        if not self._config:
            self.load_config()

        copilot_config = {"mcpServers": {}, "tools": {}, "resources": {}}

        # Add server configurations for Copilot
        for name, server_config in self._config.servers.items():
            if server_config.enabled:
                server_url = f"http://{server_config.host}:{server_config.port}{server_config.path or ''}"
                copilot_config["mcpServers"][name] = {
                    "command": "node",
                    "args": ["/path/to/mcp-client.js", "--server-url", server_url],
                    "env": server_config.env or {},
                }

        # Add enabled tools
        if self._config.copilot.enabled:
            for tool_name in self._config.copilot.tools_enabled:
                copilot_config["tools"][tool_name] = {
                    "description": f"AUDITORIA360 {tool_name} tool",
                    "server": "auditoria360-main",
                }

            for resource_uri in self._config.copilot.resources_enabled:
                resource_name = resource_uri.split("/")[-1]
                copilot_config["resources"][resource_name] = {
                    "description": f"AUDITORIA360 {resource_name} resource",
                    "uri": resource_uri,
                    "server": "auditoria360-main",
                }

        return copilot_config


# Global configuration instance
_config_manager = None


def get_config_manager(config_dir: str = None) -> MCPConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = MCPConfigManager(config_dir)
    return _config_manager
