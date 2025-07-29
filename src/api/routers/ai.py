"""
Enhanced AI and Chatbot API Router with MCP Integration
Módulo 7: IA, Chatbot e Bots Inteligentes - Extended with Model Context Protocol
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import logging

from src.models import get_db, User
from src.services.auth_service import get_current_user
from src.ai_agent import EnhancedAIAgent

logger = logging.getLogger(__name__)

router = APIRouter()

# Global AI agent instance
ai_agent: Optional[EnhancedAIAgent] = None

def get_ai_agent():
    """Get or create AI agent instance"""
    global ai_agent
    if ai_agent is None:
        ai_agent = EnhancedAIAgent()
    return ai_agent


# Pydantic models for requests/responses

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class MCPRequest(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = None


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = {}


class AIActionRequest(BaseModel):
    action: str
    context: Optional[Dict[str, Any]] = None


# Original AI endpoints (enhanced)

@router.post("/chat")
async def chat_with_bot(
    chat_request: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced chatbot interaction with MCP integration"""
    try:
        agent = get_ai_agent()
        
        # Process message using enhanced AI agent
        result = await agent.executar_acao(
            f"chat: {chat_request.message}",
            chat_request.context
        )
        
        if result.get("success"):
            return {
                "response": result.get("result", "Processed successfully"),
                "session_id": chat_request.session_id,
                "timestamp": result.get("timestamp"),
                "processed_via": result.get("processed_via", "Enhanced AI")
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Chat processing failed: {result.get('error')}"
            )
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/conversations")
async def list_conversations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user conversations"""
    # TODO: Implement actual conversation retrieval from database
    return {
        "conversations": [],
        "total": 0,
        "skip": skip,
        "limit": limit,
        "message": "Conversations list endpoint - enhanced implementation pending"
    }


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation with messages"""
    # TODO: Implement actual conversation retrieval
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "message": "Conversation get endpoint - enhanced implementation pending"
    }


@router.post("/recommendations")
async def get_ai_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI recommendations for user using MCP tools"""
    try:
        agent = get_ai_agent()
        
        # Use compliance checker and audit tools for recommendations
        compliance_result = await agent.executar_acao(
            "verificar compliance",
            {"employee_id": str(current_user.id), "check_type": "full"}
        )
        
        recommendations = []
        if compliance_result.get("success"):
            result_data = compliance_result.get("result", {})
            if not result_data.get("compliant", True):
                recommendations.extend(result_data.get("recommendations", []))
        
        return {
            "recommendations": recommendations,
            "user_id": current_user.id,
            "generated_via": "MCP Tools",
            "timestamp": compliance_result.get("timestamp")
        }
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/knowledge-base/search")
async def search_knowledge_base(
    query: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search knowledge base using MCP resources"""
    try:
        agent = get_ai_agent()
        
        # Use MCP resource to search knowledge base
        if agent.mcp_server and agent.resource_provider:
            kb_content = await agent.resource_provider._read_knowledge_base(
                "auditoria://knowledge/base"
            )
            
            # Simple search implementation (could be enhanced with vector search)
            search_results = []
            if "text" in kb_content:
                kb_data = json.loads(kb_content["text"])
                search_results.append({
                    "title": f"Search results for: {query}",
                    "content": kb_data.get("summary", ""),
                    "relevance": 0.8,
                    "source": "MCP Knowledge Base"
                })
            
            return {
                "query": query,
                "results": search_results[:limit],
                "total_found": len(search_results),
                "searched_via": "MCP Resources"
            }
        else:
            return {
                "query": query,
                "results": [],
                "message": "MCP knowledge base not available"
            }
            
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/knowledge-base")
async def create_knowledge_base_entry(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create knowledge base entry (admin only)"""
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return {"message": "Knowledge base creation endpoint - enhanced implementation pending"}


# New MCP-specific endpoints

@router.get("/mcp/capabilities")
async def get_mcp_capabilities(
    current_user: User = Depends(get_current_user)
):
    """Get MCP server capabilities for Copilot integration"""
    try:
        agent = get_ai_agent()
        capabilities = await agent.get_mcp_capabilities()
        return capabilities
        
    except Exception as e:
        logger.error(f"Error getting MCP capabilities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/mcp/request")
async def handle_mcp_request(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Handle raw MCP protocol requests"""
    try:
        agent = get_ai_agent()
        
        # Get raw request body
        request_data = await request.body()
        request_str = request_data.decode('utf-8')
        
        # Process MCP request
        response_str = await agent.handle_mcp_request(request_str)
        
        # Return raw MCP response
        return json.loads(response_str)
        
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/mcp/resources")
async def list_mcp_resources(
    current_user: User = Depends(get_current_user)
):
    """List available MCP resources"""
    try:
        agent = get_ai_agent()
        
        if agent.mcp_server:
            resources = list(agent.mcp_server._resources.values())
            return {
                "resources": [r.model_dump() for r in resources],
                "count": len(resources)
            }
        else:
            return {"resources": [], "count": 0}
            
    except Exception as e:
        logger.error(f"Error listing MCP resources: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/mcp/tools")
async def list_mcp_tools(
    current_user: User = Depends(get_current_user)
):
    """List available MCP tools"""
    try:
        agent = get_ai_agent()
        
        if agent.mcp_server:
            tools = list(agent.mcp_server._tools.values())
            return {
                "tools": [t.model_dump() for t in tools],
                "count": len(tools)
            }
        else:
            return {"tools": [], "count": 0}
            
    except Exception as e:
        logger.error(f"Error listing MCP tools: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/mcp/tools/call")
async def call_mcp_tool(
    tool_request: ToolCallRequest,
    current_user: User = Depends(get_current_user)
):
    """Call a specific MCP tool"""
    try:
        agent = get_ai_agent()
        
        if not agent.mcp_server or not agent.tool_provider:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MCP server not available"
            )
        
        # Map tool names to executor methods
        tool_executors = {
            "payroll_calculator": agent.tool_provider._execute_payroll_calculator,
            "compliance_checker": agent.tool_provider._execute_compliance_checker,
            "document_analyzer": agent.tool_provider._execute_document_analyzer,
            "audit_executor": agent.tool_provider._execute_audit_executor,
            "cct_comparator": agent.tool_provider._execute_cct_comparator
        }
        
        if tool_request.tool_name not in tool_executors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_request.tool_name} not found"
            )
        
        executor = tool_executors[tool_request.tool_name]
        result = await executor(tool_request.tool_name, tool_request.arguments)
        
        return {
            "tool_name": tool_request.tool_name,
            "result": result,
            "executed_by": current_user.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calling MCP tool {tool_request.tool_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/actions/execute")
async def execute_ai_action(
    action_request: AIActionRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute AI action using enhanced agent with MCP integration"""
    try:
        agent = get_ai_agent()
        
        result = await agent.executar_acao(
            action_request.action,
            action_request.context
        )
        
        return {
            "action": action_request.action,
            "result": result,
            "executed_by": current_user.username
        }
        
    except Exception as e:
        logger.error(f"Error executing AI action: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status")
async def get_ai_status(
    current_user: User = Depends(get_current_user)
):
    """Get AI agent and MCP status"""
    try:
        agent = get_ai_agent()
        
        return {
            "ai_agent_status": agent.status,
            "mcp_server_available": agent.mcp_server is not None,
            "mcp_tools_count": len(agent.mcp_server._tools) if agent.mcp_server else 0,
            "mcp_resources_count": len(agent.mcp_server._resources) if agent.mcp_server else 0,
            "version": "1.0.0-mcp-enhanced"
        }
        
    except Exception as e:
        logger.error(f"Error getting AI status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )