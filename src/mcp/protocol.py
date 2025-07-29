"""
MCP Protocol Implementation for AUDITORIA360
Defines core protocol messages and types according to MCP specification
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class MCPVersion(str, Enum):
    """Supported MCP protocol versions"""

    V1_0 = "1.0"


class ErrorCode(int, Enum):
    """Standard MCP error codes"""

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


class MCPError(BaseModel):
    """MCP error response format"""

    code: ErrorCode
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPRequest(BaseModel):
    """Base MCP request message"""

    jsonrpc: Literal["2.0"] = "2.0"
    id: Union[str, int, None] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """Base MCP response message"""

    jsonrpc: Literal["2.0"] = "2.0"
    id: Union[str, int, None] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[MCPError] = None


class MCPNotification(BaseModel):
    """MCP notification message (no response expected)"""

    jsonrpc: Literal["2.0"] = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None


# Core MCP Types


class ResourceType(str, Enum):
    """Types of resources available via MCP"""

    PAYROLL_DATA = "payroll_data"
    EMPLOYEE_INFO = "employee_info"
    CCT_DOCUMENT = "cct_document"
    AUDIT_REPORT = "audit_report"
    COMPLIANCE_RULE = "compliance_rule"
    KNOWLEDGE_BASE = "knowledge_base"


class ToolType(str, Enum):
    """Types of tools available via MCP"""

    PAYROLL_CALCULATOR = "payroll_calculator"
    COMPLIANCE_CHECKER = "compliance_checker"
    DOCUMENT_ANALYZER = "document_analyzer"
    AUDIT_EXECUTOR = "audit_executor"
    CCT_COMPARATOR = "cct_comparator"


class ResourceInfo(BaseModel):
    """Information about an available resource"""

    uri: str
    name: str
    description: str
    mimeType: Optional[str] = None
    annotations: Optional[Dict[str, Any]] = None


class ToolInfo(BaseModel):
    """Information about an available tool"""

    name: str
    description: str
    inputSchema: Dict[str, Any]
    outputSchema: Optional[Dict[str, Any]] = None


class ServerInfo(BaseModel):
    """MCP server information"""

    name: str
    version: str
    protocolVersion: MCPVersion = MCPVersion.V1_0
    capabilities: Dict[str, Any] = Field(default_factory=dict)


class ClientInfo(BaseModel):
    """MCP client information"""

    name: str
    version: str
    protocolVersion: MCPVersion = MCPVersion.V1_0


# Request/Response Types


class InitializeRequest(MCPRequest):
    """Initialize MCP connection"""

    method: Literal["initialize"] = "initialize"
    params: ClientInfo


class InitializeResponse(MCPResponse):
    """Initialize response with server info"""

    result: ServerInfo


class ListResourcesRequest(MCPRequest):
    """List available resources"""

    method: Literal["resources/list"] = "resources/list"


class ListResourcesResponse(MCPResponse):
    """Resources list response"""

    result: Dict[Literal["resources"], List[ResourceInfo]]


class ReadResourceRequest(MCPRequest):
    """Read a specific resource"""

    method: Literal["resources/read"] = "resources/read"
    params: Dict[Literal["uri"], str]


class ReadResourceResponse(MCPResponse):
    """Resource content response"""

    result: Dict[Literal["contents"], List[Dict[str, Any]]]


class ListToolsRequest(MCPRequest):
    """List available tools"""

    method: Literal["tools/list"] = "tools/list"


class ListToolsResponse(MCPResponse):
    """Tools list response"""

    result: Dict[Literal["tools"], List[ToolInfo]]


class CallToolRequest(MCPRequest):
    """Call a specific tool"""

    method: Literal["tools/call"] = "tools/call"
    params: Dict[str, Any]


class CallToolResponse(MCPResponse):
    """Tool call result"""

    result: Dict[str, Any]


# Notification Types


class ResourceUpdateNotification(MCPNotification):
    """Notify about resource updates"""

    method: Literal["notifications/resources/updated"] = (
        "notifications/resources/updated"
    )
    params: Dict[Literal["uri"], str]


class ToolUpdateNotification(MCPNotification):
    """Notify about tool updates"""

    method: Literal["notifications/tools/list_changed"] = (
        "notifications/tools/list_changed"
    )
