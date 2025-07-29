"""
MCP Client Implementation for AUDITORIA360
Provides client functionality for connecting to external MCP servers
"""

import json
import logging
import uuid
from typing import Any, Callable, Dict, List, Optional

from .protocol import (
    CallToolRequest,
    ClientInfo,
    InitializeRequest,
    ListResourcesRequest,
    ListToolsRequest,
    MCPResponse,
    ReadResourceRequest,
    ResourceInfo,
    ToolInfo,
)

logger = logging.getLogger(__name__)


class MCPClient:
    """Model Context Protocol client for connecting to external MCP servers"""

    def __init__(self, name: str = "AUDITORIA360-Client", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.connected = False
        self.server_info = None
        self.session_id = None

        # Connection handler
        self.connection_handler: Optional[Callable] = None

        # Cache for resources and tools
        self._cached_resources: List[ResourceInfo] = []
        self._cached_tools: List[ToolInfo] = []
        self._cache_valid = False

        logger.info(f"MCP Client {self.name} v{self.version} initialized")

    def set_connection_handler(self, handler: Callable):
        """Set the connection handler for sending messages"""
        self.connection_handler = handler

    async def connect(self) -> bool:
        """Initialize connection with MCP server"""
        if not self.connection_handler:
            logger.error("No connection handler set")
            return False

        try:
            # Create initialize request
            client_info = ClientInfo(name=self.name, version=self.version)
            request = InitializeRequest(
                id=str(uuid.uuid4()), params=client_info.model_dump()
            )

            # Send request and get response
            response_data = await self.connection_handler(request.model_dump_json())
            response = MCPResponse.model_validate(json.loads(response_data))

            if response.error:
                logger.error(f"Connection failed: {response.error.message}")
                return False

            self.server_info = response.result
            self.connected = True
            self.session_id = str(uuid.uuid4())

            logger.info(
                f"Connected to MCP server: {self.server_info.get('name', 'Unknown')}"
            )
            return True

        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False

    async def disconnect(self):
        """Disconnect from MCP server"""
        self.connected = False
        self.server_info = None
        self.session_id = None
        self._cached_resources.clear()
        self._cached_tools.clear()
        self._cache_valid = False
        logger.info("Disconnected from MCP server")

    async def list_resources(self, use_cache: bool = True) -> List[ResourceInfo]:
        """List available resources from the server"""
        if not self.connected:
            raise Exception("Not connected to MCP server")

        if use_cache and self._cache_valid and self._cached_resources:
            return self._cached_resources

        try:
            request = ListResourcesRequest(id=str(uuid.uuid4()))
            response_data = await self.connection_handler(request.model_dump_json())
            response = MCPResponse.model_validate(json.loads(response_data))

            if response.error:
                raise Exception(f"Failed to list resources: {response.error.message}")

            resources_data = response.result.get("resources", [])
            resources = [ResourceInfo.model_validate(r) for r in resources_data]

            if use_cache:
                self._cached_resources = resources
                self._cache_valid = True

            logger.info(f"Retrieved {len(resources)} resources from server")
            return resources

        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            raise

    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read content from a specific resource"""
        if not self.connected:
            raise Exception("Not connected to MCP server")

        try:
            request = ReadResourceRequest(id=str(uuid.uuid4()), params={"uri": uri})

            response_data = await self.connection_handler(request.model_dump_json())
            response = MCPResponse.model_validate(json.loads(response_data))

            if response.error:
                raise Exception(
                    f"Failed to read resource {uri}: {response.error.message}"
                )

            contents = response.result.get("contents", [])
            if not contents:
                raise Exception(f"No content returned for resource {uri}")

            logger.info(f"Successfully read resource: {uri}")
            return contents[0]

        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            raise

    async def list_tools(self, use_cache: bool = True) -> List[ToolInfo]:
        """List available tools from the server"""
        if not self.connected:
            raise Exception("Not connected to MCP server")

        if use_cache and self._cache_valid and self._cached_tools:
            return self._cached_tools

        try:
            request = ListToolsRequest(id=str(uuid.uuid4()))
            response_data = await self.connection_handler(request.model_dump_json())
            response = MCPResponse.model_validate(json.loads(response_data))

            if response.error:
                raise Exception(f"Failed to list tools: {response.error.message}")

            tools_data = response.result.get("tools", [])
            tools = [ToolInfo.model_validate(t) for t in tools_data]

            if use_cache:
                self._cached_tools = tools
                self._cache_valid = True

            logger.info(f"Retrieved {len(tools)} tools from server")
            return tools

        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            raise

    async def call_tool(
        self, name: str, arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a specific tool with given arguments"""
        if not self.connected:
            raise Exception("Not connected to MCP server")

        try:
            request = CallToolRequest(
                id=str(uuid.uuid4()),
                params={"name": name, "arguments": arguments or {}},
            )

            response_data = await self.connection_handler(request.model_dump_json())
            response = MCPResponse.model_validate(json.loads(response_data))

            if response.error:
                raise Exception(f"Failed to call tool {name}: {response.error.message}")

            logger.info(f"Successfully called tool: {name}")
            return response.result

        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            raise

    async def get_server_capabilities(self) -> Dict[str, Any]:
        """Get server capabilities"""
        if not self.connected or not self.server_info:
            raise Exception("Not connected to MCP server")

        return self.server_info.get("capabilities", {})

    def invalidate_cache(self):
        """Invalidate cached resources and tools"""
        self._cache_valid = False
        self._cached_resources.clear()
        self._cached_tools.clear()
        logger.info("Cache invalidated")


class MCPClientManager:
    """Manages multiple MCP client connections"""

    def __init__(self):
        self.clients: Dict[str, MCPClient] = {}
        self.connection_configs: Dict[str, Dict[str, Any]] = {}

    def register_client(
        self, name: str, client: MCPClient, config: Dict[str, Any] = None
    ):
        """Register a client with optional configuration"""
        self.clients[name] = client
        if config:
            self.connection_configs[name] = config
        logger.info(f"Registered MCP client: {name}")

    def get_client(self, name: str) -> Optional[MCPClient]:
        """Get a client by name"""
        return self.clients.get(name)

    async def connect_all(self) -> Dict[str, bool]:
        """Connect all registered clients"""
        results = {}
        for name, client in self.clients.items():
            try:
                result = await client.connect()
                results[name] = result
                if result:
                    logger.info(f"Successfully connected client: {name}")
                else:
                    logger.warning(f"Failed to connect client: {name}")
            except Exception as e:
                logger.error(f"Error connecting client {name}: {e}")
                results[name] = False

        return results

    async def disconnect_all(self):
        """Disconnect all clients"""
        for name, client in self.clients.items():
            try:
                await client.disconnect()
                logger.info(f"Disconnected client: {name}")
            except Exception as e:
                logger.error(f"Error disconnecting client {name}: {e}")

    async def list_all_resources(self) -> Dict[str, List[ResourceInfo]]:
        """List resources from all connected clients"""
        results = {}
        for name, client in self.clients.items():
            if client.connected:
                try:
                    resources = await client.list_resources()
                    results[name] = resources
                except Exception as e:
                    logger.error(f"Error listing resources from {name}: {e}")
                    results[name] = []
            else:
                results[name] = []

        return results

    async def list_all_tools(self) -> Dict[str, List[ToolInfo]]:
        """List tools from all connected clients"""
        results = {}
        for name, client in self.clients.items():
            if client.connected:
                try:
                    tools = await client.list_tools()
                    results[name] = tools
                except Exception as e:
                    logger.error(f"Error listing tools from {name}: {e}")
                    results[name] = []
            else:
                results[name] = []

        return results

    async def call_tool_on_client(
        self, client_name: str, tool_name: str, arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a tool on a specific client"""
        client = self.get_client(client_name)
        if not client:
            raise Exception(f"Client {client_name} not found")

        if not client.connected:
            raise Exception(f"Client {client_name} not connected")

        return await client.call_tool(tool_name, arguments)

    def get_connection_status(self) -> Dict[str, bool]:
        """Get connection status for all clients"""
        return {name: client.connected for name, client in self.clients.items()}


# Utility functions for common MCP operations


async def create_simple_mcp_client(
    server_handler: Callable, name: str = "AUDITORIA360-Client"
) -> MCPClient:
    """Create and connect a simple MCP client"""
    client = MCPClient(name=name)
    client.set_connection_handler(server_handler)

    success = await client.connect()
    if not success:
        raise Exception("Failed to connect to MCP server")

    return client


async def discover_and_cache_capabilities(client: MCPClient) -> Dict[str, Any]:
    """Discover and cache all capabilities from an MCP server"""
    if not client.connected:
        raise Exception("Client not connected")

    capabilities = {
        "server_info": client.server_info,
        "server_capabilities": await client.get_server_capabilities(),
        "resources": await client.list_resources(),
        "tools": await client.list_tools(),
    }

    logger.info(f"Discovered capabilities from {client.name}")
    return capabilities
