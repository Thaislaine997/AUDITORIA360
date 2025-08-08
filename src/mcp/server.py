"""
MCP Server Implementation for AUDITORIA360
Provides MCP server functionality for exposing system resources and tools
"""

import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, List

from .protocol import (  # Swarm Intelligence imports
    AgentInfo,
    AgentJoinedNotification,
    AgentLeftNotification,
    ConsensusProposal,
    ConsensusUpdateNotification,
    EmergencyProtocolNotification,
    ErrorCode,
    MCPError,
    MCPNotification,
    MCPRequest,
    MCPResponse,
    MessageBroadcastNotification,
    ResourceInfo,
    ResourceUpdateNotification,
    ServerInfo,
    SwarmMessage,
    TaskDefinition,
    ToolInfo,
    ToolUpdateNotification,
)
from .swarm import AgentRole, BaseAgent, CollectiveMind, SpecialistAgent

logger = logging.getLogger(__name__)


class MCPServer:
    """Model Context Protocol server for AUDITORIA360 with Swarm Intelligence"""

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
            # Swarm Intelligence handlers
            "swarm/agent/register": self._handle_register_agent,
            "swarm/agents/list": self._handle_list_agents,
            "swarm/message/send": self._handle_send_message,
            "swarm/consensus/propose": self._handle_propose_consensus,
            "swarm/consensus/vote": self._handle_vote_consensus,
            "swarm/task/distribute": self._handle_distribute_task,
            "swarm/task/claim": self._handle_claim_task,
            "swarm/agent/isolate": self._handle_isolate_agent,
            "swarm/health": self._handle_swarm_health,
        }

        # Resource and tool implementations
        self._resource_readers: Dict[str, Callable] = {}
        self._tool_executors: Dict[str, Callable] = {}

        # Notification callbacks
        self._notification_callbacks: List[Callable] = []

        # Swarm Intelligence - Master Collective Protocol
        self.collective_mind = CollectiveMind()

        logger.info(
            f"MCP Server {self.name} v{self.version} initialized with Swarm Intelligence"
        )

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

    # Swarm Intelligence Method Handlers

    async def _handle_register_agent(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle agent registration"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params:
            return MCPError(code=ErrorCode.INVALID_PARAMS, message="Missing agent info")

        try:
            agent_info = AgentInfo(**request.params)

            # Create appropriate agent type based on role
            if agent_info.role == AgentRole.SPECIALIST:
                agent = SpecialistAgent(
                    agent_info.agent_id,
                    (
                        agent_info.specializations[0]
                        if agent_info.specializations
                        else "general"
                    ),
                    "default_domain",
                )
            else:
                agent = BaseAgent(agent_info.agent_id, agent_info.role, agent_info.name)
                agent.capabilities = [cap for cap in agent_info.capabilities]
                agent.specializations = agent_info.specializations
                agent.trust_score = agent_info.trust_score

            success = await self.collective_mind.register_agent(agent)

            if success:
                # Send notification
                notification = AgentJoinedNotification(params={"agent": agent_info})
                await self._send_notification(notification)

                return {"success": True, "agent_id": agent_info.agent_id}
            else:
                return MCPError(
                    code=ErrorCode.INTERNAL_ERROR, message="Failed to register agent"
                )

        except Exception as e:
            logger.error(f"Error registering agent: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR, message=f"Registration failed: {str(e)}"
            )

    async def _handle_list_agents(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle list agents request"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        agents = [agent.get_info() for agent in self.collective_mind.agents.values()]
        return {"agents": [agent.model_dump() for agent in agents]}

    async def _handle_send_message(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle send message request"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params:
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message="Missing message data"
            )

        try:
            message = SwarmMessage(**request.params)
            delivered = await self.collective_mind.send_message(message)

            # Send notification if broadcast
            if not message.recipient_id:
                notification = MessageBroadcastNotification(params=message)
                await self._send_notification(notification)

            return {"delivered": delivered}

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Message sending failed: {str(e)}",
            )

    async def _handle_propose_consensus(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle consensus proposal"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params:
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message="Missing proposal data"
            )

        try:
            proposal = ConsensusProposal(**request.params)
            proposal_id = await self.collective_mind.propose_consensus(proposal)

            # Send notification
            notification = ConsensusUpdateNotification(params=proposal)
            await self._send_notification(notification)

            return {"proposal_id": proposal_id, "status": "proposed"}

        except Exception as e:
            logger.error(f"Error proposing consensus: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Consensus proposal failed: {str(e)}",
            )

    async def _handle_vote_consensus(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle consensus voting"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if (
            not request.params
            or "proposal_id" not in request.params
            or "vote" not in request.params
        ):
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message="Missing proposal_id or vote"
            )

        try:
            proposal_id = request.params["proposal_id"]
            vote = request.params["vote"]
            agent_id = request.params.get("agent_id", "unknown")

            success = await self.collective_mind.vote_consensus(
                proposal_id, agent_id, vote
            )

            if success:
                # Get updated proposal and send notification
                proposal = self.collective_mind.consensus_proposals.get(proposal_id)
                if proposal:
                    notification = ConsensusUpdateNotification(params=proposal)
                    await self._send_notification(notification)

                return {"voted": True, "proposal_id": proposal_id}
            else:
                return MCPError(
                    code=ErrorCode.INVALID_PARAMS,
                    message="Invalid proposal or voting failed",
                )

        except Exception as e:
            logger.error(f"Error voting on consensus: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR, message=f"Voting failed: {str(e)}"
            )

    async def _handle_distribute_task(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle task distribution"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params:
            return MCPError(code=ErrorCode.INVALID_PARAMS, message="Missing task data")

        try:
            task = TaskDefinition(**request.params)
            task_id = await self.collective_mind.distribute_task(task)

            return {"task_id": task_id, "status": "distributed"}

        except Exception as e:
            logger.error(f"Error distributing task: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Task distribution failed: {str(e)}",
            )

    async def _handle_claim_task(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle task claiming by agent"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if (
            not request.params
            or "task_id" not in request.params
            or "agent_id" not in request.params
        ):
            return MCPError(
                code=ErrorCode.INVALID_PARAMS, message="Missing task_id or agent_id"
            )

        task_id = request.params["task_id"]
        agent_id = request.params["agent_id"]

        # Implementation for task claiming logic
        if task_id in self.collective_mind.tasks:
            task = self.collective_mind.tasks[task_id]
            if agent_id not in task.assigned_agents:
                task.assigned_agents.append(agent_id)
            return {"claimed": True, "task_id": task_id}
        else:
            return MCPError(code=ErrorCode.INVALID_PARAMS, message="Task not found")

    async def _handle_isolate_agent(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle agent isolation"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        if not request.params or "agent_id" not in request.params:
            return MCPError(code=ErrorCode.INVALID_PARAMS, message="Missing agent_id")

        try:
            agent_id = request.params["agent_id"]
            reason = request.params.get("reason", "manual_isolation")

            success = await self.collective_mind.isolate_agent(agent_id, reason)

            if success:
                # Send notification
                notification = AgentLeftNotification(
                    params={"agent_id": agent_id, "reason": f"isolated: {reason}"}
                )
                await self._send_notification(notification)

                return {"isolated": True, "agent_id": agent_id}
            else:
                return MCPError(
                    code=ErrorCode.INVALID_PARAMS,
                    message="Agent not found or isolation failed",
                )

        except Exception as e:
            logger.error(f"Error isolating agent: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"Agent isolation failed: {str(e)}",
            )

    async def _handle_swarm_health(self, request: MCPRequest) -> Dict[str, Any]:
        """Handle swarm health check"""
        if not self.initialized:
            return MCPError(
                code=ErrorCode.INVALID_REQUEST, message="Server not initialized"
            )

        try:
            health = self.collective_mind.get_collective_health()

            # Resolve async consciousness cost if present
            if "consciousness_cost" in health and hasattr(
                health["consciousness_cost"], "result"
            ):
                health["consciousness_cost"] = await health["consciousness_cost"]

            return health

        except Exception as e:
            logger.error(f"Error getting swarm health: {e}")
            return MCPError(
                code=ErrorCode.INTERNAL_ERROR, message=f"Health check failed: {str(e)}"
            )


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
