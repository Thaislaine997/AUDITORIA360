"""
Enhanced AI and Chatbot API Router with MCP Integration
Módulo 7: IA, Chatbot e Bots Inteligentes - Extended with Model Context Protocol
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.ai_agent import EnhancedAIAgent
from src.models import User, get_db
from src.services.auth_service import get_current_user

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
    db: Session = Depends(get_db),
):
    """Enhanced chatbot interaction with OpenAI GPT integration"""
    try:
        agent = get_ai_agent()

        # Use direct OpenAI chat for better responses
        context_data = {
            "session_id": chat_request.session_id,
            "user_id": str(current_user.id),
            "user_role": getattr(current_user, "role", "user"),
        }
        if chat_request.context:
            context_data.update(chat_request.context)

        result = await agent.chat_with_openai(chat_request.message, context_data)

        if result.get("success"):
            return {
                "response": result.get("response", "Processed successfully"),
                "session_id": chat_request.session_id,
                "confidence": result.get("confidence", 0.8),
                "suggestions": result.get("suggestions", []),
                "usage": result.get("usage", {}),
                "provider": "OpenAI GPT",
                "timestamp": result.get("timestamp"),
            }
        else:
            # Fallback to MCP processing
            mcp_result = await agent.executar_acao(
                f"chat: {chat_request.message}", chat_request.context
            )

            if mcp_result.get("success"):
                return {
                    "response": mcp_result.get("result", "Processed successfully"),
                    "session_id": chat_request.session_id,
                    "timestamp": mcp_result.get("timestamp"),
                    "processed_via": "MCP Fallback",
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Chat processing failed: {result.get('error')}",
                )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/conversations")
async def list_conversations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user conversations"""
    # TODO: Implement actual conversation retrieval from database
    return {
        "conversations": [],
        "total": 0,
        "skip": skip,
        "limit": limit,
        "message": "Conversations list endpoint - enhanced implementation pending",
    }


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get conversation with messages"""
    # TODO: Implement actual conversation retrieval
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "message": "Conversation get endpoint - enhanced implementation pending",
    }


@router.post("/recommendations")
async def get_ai_recommendations(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get AI recommendations using OpenAI GPT"""
    try:
        agent = get_ai_agent()

        # Prepare user context for recommendations
        user_context = {
            "user_id": str(current_user.id),
            "user_role": getattr(current_user, "role", "user"),
            "username": getattr(current_user, "username", "unknown"),
            "timestamp": datetime.now().isoformat(),
        }

        # Try OpenAI recommendations first
        ai_result = await agent.get_ai_recommendations(user_context)

        if ai_result.get("success"):
            return {
                "recommendations": ai_result.get("response", ""),
                "user_id": current_user.id,
                "generated_via": "OpenAI GPT",
                "timestamp": datetime.now().isoformat(),
                "usage": ai_result.get("usage", {}),
            }

        # Fallback to MCP compliance checker for recommendations
        compliance_result = await agent.executar_acao(
            "verificar compliance",
            {"employee_id": str(current_user.id), "check_type": "full"},
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
            "timestamp": compliance_result.get("timestamp"),
        }

    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/knowledge-base/search")
async def search_knowledge_base(
    query: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
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
                search_results.append(
                    {
                        "title": f"Search results for: {query}",
                        "content": kb_data.get("summary", ""),
                        "relevance": 0.8,
                        "source": "MCP Knowledge Base",
                    }
                )

            return {
                "query": query,
                "results": search_results[:limit],
                "total_found": len(search_results),
                "searched_via": "MCP Resources",
            }
        else:
            return {
                "query": query,
                "results": [],
                "message": "MCP knowledge base not available",
            }

    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/knowledge-base")
async def create_knowledge_base_entry(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Create knowledge base entry (admin only)"""
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return {
        "message": "Knowledge base creation endpoint - enhanced implementation pending"
    }


# New OpenAI-specific endpoints


@router.post("/analyze-document")
async def analyze_document_with_ai(
    document_content: str,
    document_type: str = "general",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Analyze document content using OpenAI GPT"""
    try:
        agent = get_ai_agent()

        result = await agent.analyze_document_with_ai(document_content, document_type)

        if result.get("success"):
            return {
                "analysis": result.get("response", ""),
                "document_type": document_type,
                "analyzed_by": "OpenAI GPT",
                "user_id": current_user.id,
                "timestamp": datetime.now().isoformat(),
                "usage": result.get("usage", {}),
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Document analysis failed: {result.get('error')}",
            )

    except Exception as e:
        logger.error(f"Error in document analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Original MCP-specific endpoints


@router.get("/mcp/capabilities")
async def get_mcp_capabilities(current_user: User = Depends(get_current_user)):
    """Get MCP server capabilities for Copilot integration"""
    try:
        agent = get_ai_agent()
        capabilities = await agent.get_mcp_capabilities()
        return capabilities

    except Exception as e:
        logger.error(f"Error getting MCP capabilities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/mcp/request")
async def handle_mcp_request(
    request: Request, current_user: User = Depends(get_current_user)
):
    """Handle raw MCP protocol requests"""
    try:
        agent = get_ai_agent()

        # Get raw request body
        request_data = await request.body()
        request_str = request_data.decode("utf-8")

        # Process MCP request
        response_str = await agent.handle_mcp_request(request_str)

        # Return raw MCP response
        return json.loads(response_str)

    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/mcp/resources")
async def list_mcp_resources(current_user: User = Depends(get_current_user)):
    """List available MCP resources"""
    try:
        agent = get_ai_agent()

        if agent.mcp_server:
            resources = list(agent.mcp_server._resources.values())
            return {
                "resources": [r.model_dump() for r in resources],
                "count": len(resources),
            }
        else:
            return {"resources": [], "count": 0}

    except Exception as e:
        logger.error(f"Error listing MCP resources: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/mcp/tools")
async def list_mcp_tools(current_user: User = Depends(get_current_user)):
    """List available MCP tools"""
    try:
        agent = get_ai_agent()

        if agent.mcp_server:
            tools = list(agent.mcp_server._tools.values())
            return {"tools": [t.model_dump() for t in tools], "count": len(tools)}
        else:
            return {"tools": [], "count": 0}

    except Exception as e:
        logger.error(f"Error listing MCP tools: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/mcp/tools/call")
async def call_mcp_tool(
    tool_request: ToolCallRequest, current_user: User = Depends(get_current_user)
):
    """Call a specific MCP tool"""
    try:
        agent = get_ai_agent()

        if not agent.mcp_server or not agent.tool_provider:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MCP server not available",
            )

        # Map tool names to executor methods
        tool_executors = {
            "payroll_calculator": agent.tool_provider._execute_payroll_calculator,
            "compliance_checker": agent.tool_provider._execute_compliance_checker,
            "document_analyzer": agent.tool_provider._execute_document_analyzer,
            "audit_executor": agent.tool_provider._execute_audit_executor,
            "cct_comparator": agent.tool_provider._execute_cct_comparator,
        }

        if tool_request.tool_name not in tool_executors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_request.tool_name} not found",
            )

        executor = tool_executors[tool_request.tool_name]
        result = await executor(tool_request.tool_name, tool_request.arguments)

        return {
            "tool_name": tool_request.tool_name,
            "result": result,
            "executed_by": current_user.username,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calling MCP tool {tool_request.tool_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/actions/execute")
async def execute_ai_action(
    action_request: AIActionRequest, current_user: User = Depends(get_current_user)
):
    """Execute AI action using enhanced agent with MCP integration"""
    try:
        agent = get_ai_agent()

        result = await agent.executar_acao(
            action_request.action, action_request.context
        )

        return {
            "action": action_request.action,
            "result": result,
            "executed_by": current_user.username,
        }

    except Exception as e:
        logger.error(f"Error executing AI action: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/status")
async def get_ai_status(current_user: User = Depends(get_current_user)):
    """Get AI agent status including OpenAI integration"""
    try:
        agent = get_ai_agent()

        capabilities = await agent.get_mcp_capabilities()

        return {
            "ai_agent_status": agent.status,
            "openai_available": capabilities.get("openai_integration", False),
            "mcp_server_available": capabilities.get("mcp_integration", False),
            "mcp_tools_count": len(capabilities.get("tools", [])),
            "mcp_resources_count": len(capabilities.get("resources", [])),
            "capabilities": capabilities.get("capabilities", {}),
            "version": "1.0.0-openai-integrated",
        }

    except Exception as e:
        logger.error(f"Error getting AI status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
