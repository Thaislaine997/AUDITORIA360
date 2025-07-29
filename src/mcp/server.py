"""
MCP Server Implementation for AUDITORIA360
Provides MCP server functionality for exposing system resources and tools
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .protocol import (
    CallToolRequest,
    CallToolResponse,
    ErrorCode,
    InitializeRequest,
    InitializeResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    ListToolsRequest,
    ListToolsResponse,
    MCPError,
    MCPNotification,
    MCPRequest,
    MCPResponse,
    ReadResourceRequest,
    ReadResourceResponse,
    ResourceInfo,
    ResourceUpdateNotification,
    ServerInfo,
    ToolInfo,
    ToolUpdateNotification,
)

logger = logging.getLogger(__name__)


class MCPServer:
    """Model Context Protocol server for AUDITORIA360"""

    def __init__(self, name: str = "AUDITORIA360-MCP", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.initialized = False
        self.client_info = None

        # Registry for resources and tools
        self._resources: Dict[str, ResourceInfo] = {}
        self._tools: Dict[str, ToolInfo] = {}

        # Handlers for different methods
        self._method_handlers: Dict[str, Callable] = {
            "initialize": self._handle_initialize,
            "resources/list": self._handle_list_resources,
            "resources/read": self._handle_read_resource,
            "tools/list": self._handle_list_tools,
            "tools/call": self._handle_call_tool,
        }

        # Resource and tool implementations
        self._resource_readers: Dict[str, Callable] = {}
        self._tool_executors: Dict[str, Callable] = {}

        # Notification callbacks
        self._notification_callbacks: List[Callable] = []

        logger.info(f"MCP Server {self.name} v{self.version} initialized")

    async def handle_request(self, request_data: str) -> str:
        """Handle incoming MCP request"""
        try:
            request_dict = json.loads(request_data)
            request = MCPRequest(**request_dict)

            if request.method not in self._method_handlers:
                error = MCPError(
                    code=ErrorCode.METHOD_NOT_FOUND,
                    message=f"Method {request.method} not found",
                )
                response = MCPResponse(id=request.id, error=error)
                return response.model_dump_json()

            handler = self._method_handlers[request.method]
            result = await handler(request)

            if isinstance(result, MCPError):
                response = MCPResponse(id=request.id, error=result)
            else:
                response = MCPResponse(id=request.id, result=result)

            return response.model_dump_json()

        except json.JSONDecodeError:
            error = MCPError(code=ErrorCode.PARSE_ERROR, message="Invalid JSON")
            response = MCPResponse(error=error)
            return response.model_dump_json()

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            error = MCPError(code=ErrorCode.INTERNAL_ERROR, message=str(e))
            response = MCPResponse(id=getattr(request, "id", None), error=error)
            return response.model_dump_json()

    async def _handle_initialize(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle initialize request"""
        if not request.params:
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message="Missing client info"
            )

        self.client_info = request.params
        self.initialized = True

        server_info = ServerInfo(
            name=self.name,
            version=self.version,
            capabilities={
                "resources": {"subscribe": True, "listChanged": True},
                "tools": {"listChanged": True},
                "logging": {},
            },
        )

        logger.info(f"MCP connection initialized with client: {self.client_info}")
        return server_info.model_dump()

    async def _handle_list_resources(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle list resources request"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        resources = list(self._resources.values())
        return {"resources": [r.model_dump() for r in resources]}

    async def _handle_read_resource(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle read resource request"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params or "uri" not in request.params:
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message="Missing resource URI"
            )

        uri = request.params["uri"]
        if uri not in self._resource_readers:
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message=f"Resource {uri} not found"
            )

        try:
            reader = self._resource_readers[uri]
            content = await reader(uri)
            return {"contents": [content]}
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Failed to read resource: {str(e)}",
            )

    async def _handle_list_tools(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle list tools request"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        tools = list(self._tools.values())
        return {"tools": [t.model_dump() for t in tools]}

    async def _handle_call_tool(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle call tool request"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params or "name" not in request.params:
            return MCPError(code=ErrorCode.INVALID_PARAMS, message="Missing tool name")

        tool_name = request.params["name"]
        if tool_name not in self._tool_executors:
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message=f"Tool {tool_name} not found"
            )

        try:
            executor = self._tool_executors[tool_name]
            arguments = request.params.get("arguments", {})
            result = await executor(tool_name, arguments)
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Failed to execute tool: {str(e)}",
            )

    def register_resource(self, uri: str, info: ResourceInfo, reader: Callable):
        """Register a resource with its reader function"""
        self._resources[uri] = info
        self._resource_readers[uri] = reader
        logger.info(f"Registered resource: {uri}")

    def register_tool(self, name: str, info: ToolInfo, executor: Callable):
        """Register a tool with its executor function"""
        self._tools[name] = info
        self._tool_executors[name] = executor
        logger.info(f"Registered tool: {name}")

    async def notify_resource_updated(self, uri: str):
        """Send notification about resource update"""
        if not self.initialized:
            return

        notification = ResourceUpdateNotification(params={"uri": uri})
        await self._send_notification(notification)

    async def notify_tools_changed(self):
        """Send notification about tools list change"""
        if not self.initialized:
            return

        notification = ToolUpdateNotification()
        await self._send_notification(notification)

    async def _send_notification(self, notification: MCPNotification):
        """Send notification to client"""
        for callback in self._notification_callbacks:
            try:
                await callback(notification.model_dump_json())
            except Exception as e:
                logger.error(f"Error sending notification: {e}")

    def add_notification_callback(self, callback: Callable):
        """Add callback for sending notifications"""
        self._notification_callbacks.append(callback)


class AuditoriaResourceProvider:
    """Provides AUDITORIA360-specific resources via MCP"""

    def __init__(self, server: MCPServer, db_session_factory):
        self.server = server
        self.db_session_factory = db_session_factory
        self._register_resources()

    def _register_resources(self):
        """Register all AUDITORIA360 resources"""

        # Payroll data resource
        payroll_resource = ResourceInfo(
            uri="auditoria://payroll/data",
            name="Payroll Data",
            description="Access to payroll data including employees, competencies, and calculations",
            mimeType="application/json",
        )
        self.server.register_resource(
            payroll_resource.uri, payroll_resource, self._read_payroll_data
        )

        # Employee information resource
        employee_resource = ResourceInfo(
            uri="auditoria://employees/info",
            name="Employee Information",
            description="Detailed employee information and records",
            mimeType="application/json",
        )
        self.server.register_resource(
            employee_resource.uri, employee_resource, self._read_employee_info
        )

        # CCT documents resource
        cct_resource = ResourceInfo(
            uri="auditoria://cct/documents",
            name="CCT Documents",
            description="Collective bargaining agreements and related documents",
            mimeType="application/json",
        )
        self.server.register_resource(
            cct_resource.uri, cct_resource, self._read_cct_documents
        )

        # Compliance rules resource
        compliance_resource = ResourceInfo(
            uri="auditoria://compliance/rules",
            name="Compliance Rules",
            description="Active compliance rules and regulations",
            mimeType="application/json",
        )
        self.server.register_resource(
            compliance_resource.uri, compliance_resource, self._read_compliance_rules
        )

        # Knowledge base resource
        kb_resource = ResourceInfo(
            uri="auditoria://knowledge/base",
            name="Knowledge Base",
            description="Searchable knowledge base articles and documentation",
            mimeType="application/json",
        )
        self.server.register_resource(
            kb_resource.uri, kb_resource, self._read_knowledge_base
        )

    async def _read_payroll_data(self, uri: str) -> Dict[str, Any]:
        """Read payroll data"""
        # Implementation would access database through db_session_factory
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(
                {
                    "type": "payroll_data",
                    "timestamp": datetime.now().isoformat(),
                    "summary": "Payroll data access via MCP",
                    "available_endpoints": [
                        "employees/list",
                        "competencies/current",
                        "calculations/recent",
                    ],
                }
            ),
        }

    async def _read_employee_info(self, uri: str) -> Dict[str, Any]:
        """Read employee information"""
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(
                {
                    "type": "employee_info",
                    "timestamp": datetime.now().isoformat(),
                    "summary": "Employee information access via MCP",
                }
            ),
        }

    async def _read_cct_documents(self, uri: str) -> Dict[str, Any]:
        """Read CCT documents"""
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(
                {
                    "type": "cct_documents",
                    "timestamp": datetime.now().isoformat(),
                    "summary": "CCT documents access via MCP",
                }
            ),
        }

    async def _read_compliance_rules(self, uri: str) -> Dict[str, Any]:
        """Read compliance rules"""
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(
                {
                    "type": "compliance_rules",
                    "timestamp": datetime.now().isoformat(),
                    "summary": "Compliance rules access via MCP",
                }
            ),
        }

    async def _read_knowledge_base(self, uri: str) -> Dict[str, Any]:
        """Read knowledge base"""
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(
                {
                    "type": "knowledge_base",
                    "timestamp": datetime.now().isoformat(),
                    "summary": "Knowledge base access via MCP",
                }
            ),
        }
