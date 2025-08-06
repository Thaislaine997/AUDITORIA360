"""
MCP Protocol Implementation for AUDITORIA360
Defines core protocol messages and types according to MCP specification
Enhanced with Consensus Mechanism for "Grande Síntese" - Initiative IV
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from datetime import datetime
import uuid
import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

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
    # Enhanced error codes for consensus
    CONSENSUS_FAILED = -32001
    QUORUM_NOT_REACHED = -32002
    AGENT_CONFLICT = -32003

class ConsensusLevel(str, Enum):
    """Consensus requirement levels"""
    SIMPLE = "simple"  # 51% agreement
    MAJORITY = "majority"  # 66% agreement 
    SUPERMAJORITY = "supermajority"  # 75% agreement
    UNANIMOUS = "unanimous"  # 100% agreement

class AgentRole(str, Enum):
    """Types of agents in the consensus system"""
    SECURITY_AGENT = "security"
    VALIDATION_AGENT = "validation"
    RISK_AGENT = "risk"
    COMPLIANCE_AGENT = "compliance"
    AUDIT_AGENT = "audit"
    BUSINESS_AGENT = "business"

class ConsensusVote(BaseModel):
    """Individual agent vote in consensus"""
    agent_id: str
    agent_role: AgentRole
    vote: bool  # True = approve, False = reject
    confidence: float = Field(ge=0.0, le=1.0)  # 0.0 to 1.0
    reasoning: str
    timestamp: datetime
    supporting_data: Optional[Dict[str, Any]] = None

class ConsensusResult(BaseModel):
    """Result of a consensus process"""
    consensus_id: str
    decision_approved: bool
    total_agents: int
    votes_for: int
    votes_against: int
    abstentions: int
    consensus_level_required: ConsensusLevel
    consensus_level_achieved: float
    quorum_met: bool
    individual_votes: List[ConsensusVote]
    debate_log: List[str]
    final_reasoning: str
    timestamp: datetime
    processing_time_ms: int

class MCPConsensusRequest(BaseModel):
    """Request for MCP consensus on critical insights"""
    insight_id: str
    insight_type: str  # e.g., "risk_assessment", "security_decision", "compliance_ruling"
    insight_data: Dict[str, Any]
    consensus_level_required: ConsensusLevel = ConsensusLevel.MAJORITY
    timeout_seconds: int = 300  # 5 minute default timeout
    required_agent_roles: List[AgentRole] = []
    context: Optional[Dict[str, Any]] = None
    priority: Literal["low", "medium", "high", "critical"] = "medium"

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


# Swarm Intelligence Extensions for Master Collective Protocol

class AgentRole(str, Enum):
    """Agent specialization roles in the collective"""
    
    COORDINATOR = "coordinator"
    ANALYST = "analyst"
    LEGISLATOR = "legislator"
    COMMUNICATOR = "communicator"
    DATA_PROCESSOR = "data_processor"
    AUDITOR = "auditor"
    SPECIALIST = "specialist"
    MONITOR = "monitor"


class AgentStatus(str, Enum):
    """Agent operational status"""
    
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    CORRUPTED = "corrupted"
    ISOLATED = "isolated"
    DEAD = "dead"


class AgentInfo(BaseModel):
    """Information about an agent in the collective"""
    
    agent_id: str
    name: str
    role: AgentRole
    status: AgentStatus
    capabilities: List[str]
    specializations: List[str] = Field(default_factory=list)
    trust_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: str
    last_seen: str
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)


class SwarmMessage(BaseModel):
    """Message format for inter-agent communication"""
    
    message_id: str
    sender_id: str
    recipient_id: Optional[str] = None  # None means broadcast
    message_type: str
    content: Dict[str, Any]
    timestamp: str
    priority: int = Field(default=1, ge=1, le=5)  # 1=low, 5=critical
    requires_response: bool = False
    correlation_id: Optional[str] = None


class ConsensusProposal(BaseModel):
    """Proposal for collective decision making"""
    
    proposal_id: str
    proposer_id: str
    proposal_type: str
    content: Dict[str, Any]
    voting_threshold: float = Field(default=0.6, ge=0.5, le=1.0)
    deadline: str
    votes: Dict[str, bool] = Field(default_factory=dict)  # agent_id -> vote
    status: Literal["pending", "approved", "rejected", "expired"] = "pending"


class TaskDefinition(BaseModel):
    """Definition of a task for the collective"""
    
    task_id: str
    title: str
    description: str
    requirements: List[str]
    complexity: int = Field(ge=1, le=10)
    estimated_duration: int  # minutes
    assigned_agents: List[str] = Field(default_factory=list)
    status: Literal["pending", "in_progress", "completed", "failed"] = "pending"
    created_at: str
    deadline: Optional[str] = None


# Swarm-specific MCP Messages

class RegisterAgentRequest(MCPRequest):
    """Register a new agent in the collective"""
    
    method: Literal["swarm/agent/register"] = "swarm/agent/register"
    params: AgentInfo


class RegisterAgentResponse(MCPResponse):
    """Agent registration response"""
    
    result: Dict[Literal["success", "agent_id"], Union[bool, str]]


class ListAgentsRequest(MCPRequest):
    """List all agents in the collective"""
    
    method: Literal["swarm/agents/list"] = "swarm/agents/list"
    params: Optional[Dict[str, Any]] = None


class ListAgentsResponse(MCPResponse):
    """Agents list response"""
    
    result: Dict[Literal["agents"], List[AgentInfo]]


class SendMessageRequest(MCPRequest):
    """Send message between agents"""
    
    method: Literal["swarm/message/send"] = "swarm/message/send"
    params: SwarmMessage


class SendMessageResponse(MCPResponse):
    """Message sending response"""
    
    result: Dict[Literal["delivered"], bool]


class ProposeConsensusRequest(MCPRequest):
    """Propose something for collective decision"""
    
    method: Literal["swarm/consensus/propose"] = "swarm/consensus/propose"
    params: ConsensusProposal


class VoteConsensusRequest(MCPRequest):
    """Vote on a consensus proposal"""
    
    method: Literal["swarm/consensus/vote"] = "swarm/consensus/vote"
    params: Dict[Literal["proposal_id", "vote"], Union[str, bool]]


class DistributeTaskRequest(MCPRequest):
    """Distribute a task to the collective"""
    
    method: Literal["swarm/task/distribute"] = "swarm/task/distribute"
    params: TaskDefinition


class ClaimTaskRequest(MCPRequest):
    """Agent claims a task"""
    
    method: Literal["swarm/task/claim"] = "swarm/task/claim"
    params: Dict[Literal["task_id", "agent_id"], str]


class IsolateAgentRequest(MCPRequest):
    """Isolate a corrupted agent"""
    
    method: Literal["swarm/agent/isolate"] = "swarm/agent/isolate"
    params: Dict[Literal["agent_id", "reason"], str]


class SwarmHealthRequest(MCPRequest):
    """Get collective health status"""
    
    method: Literal["swarm/health"] = "swarm/health"


class SwarmHealthResponse(MCPResponse):
    """Collective health status"""
    
    result: Dict[str, Any]  # Contains metrics, agent counts, etc.


# Swarm Notifications

class AgentJoinedNotification(MCPNotification):
    """Notify when new agent joins collective"""
    
    method: Literal["notifications/swarm/agent_joined"] = "notifications/swarm/agent_joined"
    params: Dict[Literal["agent"], AgentInfo]


class AgentLeftNotification(MCPNotification):
    """Notify when agent leaves collective"""
    
    method: Literal["notifications/swarm/agent_left"] = "notifications/swarm/agent_left"
    params: Dict[Literal["agent_id", "reason"], str]


class MessageBroadcastNotification(MCPNotification):
    """Broadcast message to all agents"""
    
    method: Literal["notifications/swarm/message_broadcast"] = "notifications/swarm/message_broadcast"
    params: SwarmMessage


class ConsensusUpdateNotification(MCPNotification):
    """Notify about consensus proposal updates"""
    
    method: Literal["notifications/swarm/consensus_update"] = "notifications/swarm/consensus_update"
    params: ConsensusProposal


class EmergencyProtocolNotification(MCPNotification):
    """Emergency protocol activation"""
    
    method: Literal["notifications/swarm/emergency"] = "notifications/swarm/emergency"
    params: Dict[str, Any]
