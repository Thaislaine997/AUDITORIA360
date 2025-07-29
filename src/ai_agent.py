"""
Enhanced AI Agent with Model Context Protocol (MCP) Integration and OpenAI GPT
Extends Copilot coding agent capabilities with AUDITORIA360 specific tools and resources
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

try:
    from .mcp.client import MCPClientManager
    from .mcp.config import MCPConfiguration, get_config_manager
    from .mcp.server import AuditoriaResourceProvider, MCPServer
    from .mcp.tools import AuditoriaToolProvider
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("MCP modules not available, using basic AI functionality")

try:
    from .services.openai_service import get_openai_service
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("OpenAI service not available")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedAIAgent:
    """Enhanced AI Agent with MCP integration and OpenAI GPT for AUDITORIA360"""

    def __init__(self, db_session_factory=None):
        self.status = "initializing"
        self.db_session_factory = db_session_factory

        # MCP Components (optional)
        self.mcp_server: Optional[MCPServer] = None
        self.mcp_client_manager: Optional[MCPClientManager] = None
        self.resource_provider: Optional[AuditoriaResourceProvider] = None
        self.tool_provider: Optional[AuditoriaToolProvider] = None

        # OpenAI Service
        self.openai_service = None
        if OPENAI_AVAILABLE:
            try:
                self.openai_service = get_openai_service()
                logger.info("OpenAI service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI service: {e}")

        # Configuration
        if MCP_AVAILABLE:
            self.config_manager = get_config_manager()
            self.config: Optional[MCPConfiguration] = None
            # Initialize MCP components
            asyncio.create_task(self._initialize_mcp())
        else:
            self.config_manager = None
            self.config = None
            self.status = "ready"

        logger.info("Enhanced AI Agent with OpenAI GPT integration initialized")

    async def _initialize_mcp(self):
        """Initialize MCP server and client components"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, skipping MCP initialization")
            self.status = "ready"
            return
            
        try:
            # Load configuration
            self.config = self.config_manager.load_config()

            # Initialize MCP server
            self.mcp_server = MCPServer(name="AUDITORIA360-MCP-Server", version="1.0.0")

            # Initialize resource and tool providers
            self.resource_provider = AuditoriaResourceProvider(
                self.mcp_server, self.db_session_factory
            )
            self.tool_provider = AuditoriaToolProvider(
                self.mcp_server, self.db_session_factory
            )

            # Initialize client manager
            self.mcp_client_manager = MCPClientManager()

            self.status = "ready"
            logger.info("MCP components initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing MCP components: {e}")
            self.status = "ready"  # Continue without MCP

    async def executar_acao(
        self, acao: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute an action using MCP capabilities"""
        try:
            if self.status != "ready":
                return {
                    "success": False,
                    "error": "AI Agent not ready",
                    "status": self.status,
                }

            logger.info(f"Executing enhanced action: {acao}")

            # Try to interpret the action and map to MCP tools
            result = await self._process_action_with_mcp(acao, context or {})

            return {
                "success": True,
                "action": acao,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "processed_via": "MCP",
            }

        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": acao,
                "timestamp": datetime.now().isoformat(),
            }

    async def _process_action_with_mcp(
        self, action: str, context: Dict[str, Any]
    ) -> Any:
        """Process action using MCP tools and resources"""
        action_lower = action.lower()

        # Map actions to MCP tools
        if "calcular" in action_lower and "folha" in action_lower:
            return await self._execute_payroll_calculation(context)

        elif "verificar" in action_lower and (
            "compliance" in action_lower or "conformidade" in action_lower
        ):
            return await self._execute_compliance_check(context)

        elif "analisar" in action_lower and "documento" in action_lower:
            return await self._execute_document_analysis(context)

        elif "auditoria" in action_lower or "audit" in action_lower:
            return await self._execute_audit(context)

        elif "comparar" in action_lower and "cct" in action_lower:
            return await self._execute_cct_comparison(context)

        else:
            # Default: use general AI processing
            return await self._general_ai_processing(action, context)

    async def _execute_payroll_calculation(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute payroll calculation using MCP tools"""
        if not self.mcp_server:
            raise Exception("MCP server not initialized")

        # Extract parameters from context
        employee_id = context.get("employee_id", "EMP001")
        month = context.get("month", datetime.now().month)
        year = context.get("year", datetime.now().year)
        base_salary = context.get("base_salary", 3000.00)
        overtime_hours = context.get("overtime_hours", 0)

        # Use MCP tool
        tool_executor = self.tool_provider._execute_payroll_calculator
        result = await tool_executor(
            "payroll_calculator",
            {
                "employee_id": employee_id,
                "month": month,
                "year": year,
                "base_salary": base_salary,
                "overtime_hours": overtime_hours,
                "calculation_type": "normal",
            },
        )

        return result

    async def _execute_compliance_check(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute compliance check using MCP tools"""
        if not self.mcp_server:
            raise Exception("MCP server not initialized")

        employee_id = context.get("employee_id", "EMP001")
        check_type = context.get("check_type", "full")
        payroll_data = context.get("payroll_data", {})

        tool_executor = self.tool_provider._execute_compliance_checker
        result = await tool_executor(
            "compliance_checker",
            {
                "employee_id": employee_id,
                "check_type": check_type,
                "payroll_data": payroll_data,
            },
        )

        return result

    async def _execute_document_analysis(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute document analysis using MCP tools"""
        if not self.mcp_server:
            raise Exception("MCP server not initialized")

        document_id = context.get("document_id", "DOC001")
        document_type = context.get("document_type", "cct")
        analysis_type = context.get("analysis_type", "extract_clauses")

        tool_executor = self.tool_provider._execute_document_analyzer
        result = await tool_executor(
            "document_analyzer",
            {
                "document_id": document_id,
                "document_type": document_type,
                "analysis_type": analysis_type,
            },
        )

        return result

    async def _execute_audit(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute audit using MCP tools"""
        if not self.mcp_server:
            raise Exception("MCP server not initialized")

        audit_type = context.get("audit_type", "payroll")
        scope = context.get("scope", "sample")
        period_start = context.get("period_start", "2024-01-01")
        period_end = context.get("period_end", "2024-12-31")

        tool_executor = self.tool_provider._execute_audit_executor
        result = await tool_executor(
            "audit_executor",
            {
                "audit_type": audit_type,
                "scope": scope,
                "period_start": period_start,
                "period_end": period_end,
            },
        )

        return result

    async def _execute_cct_comparison(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute CCT comparison using MCP tools"""
        if not self.mcp_server:
            raise Exception("MCP server not initialized")

        cct_id_1 = context.get("cct_id_1", "CCT001")
        cct_id_2 = context.get("cct_id_2", "CCT002")
        comparison_type = context.get("comparison_type", "full")

        tool_executor = self.tool_provider._execute_cct_comparator
        result = await tool_executor(
            "cct_comparator",
            {
                "cct_id_1": cct_id_1,
                "cct_id_2": cct_id_2,
                "comparison_type": comparison_type,
                "highlight_differences": True,
                "include_recommendations": True,
            },
        )

        return result

    async def _general_ai_processing(self, action: str, context: Dict[str, Any]) -> str:
        """General AI processing using OpenAI GPT for actions not mapped to specific MCP tools"""
        logger.info(f"Processing general action with OpenAI: {action}")
        
        if not OPENAI_AVAILABLE or not self.openai_service:
            return f"Processed action '{action}' with basic AI. Context: {json.dumps(context, indent=2)}"
        
        try:
            # Use OpenAI for chat-like interactions
            if action.lower().startswith("chat:"):
                message = action[5:].strip()  # Remove "chat:" prefix
                result = await self.openai_service.get_auditoria_response(message, context)
                
                if result["success"]:
                    return {
                        "response": result["response"],
                        "confidence": result.get("confidence", 0.8),
                        "suggestions": result.get("suggestions", []),
                        "source": "OpenAI GPT",
                        "usage": result.get("usage", {})
                    }
                else:
                    return f"Error processing with OpenAI: {result['error']}"
            
            # For other actions, use as general assistant
            result = await self.openai_service.get_auditoria_response(action, context)
            
            if result["success"]:
                return result["response"]
            else:
                return f"Error processing with OpenAI: {result['error']}"
                
        except Exception as e:
            logger.error(f"Error in OpenAI processing: {e}")
            return f"Error processing action with AI: {str(e)}"

    async def integrar_gemini(
        self, comando: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Enhanced Gemini/LLM integration with MCP context and OpenAI fallback"""
        logger.info(f"Integrating with LLM: {comando}")

        # Get available MCP resources and tools for context
        mcp_context = await self._get_mcp_context()

        # Combine with provided context
        full_context = {
            "comando": comando,
            "mcp_context": mcp_context,
            "user_context": context or {},
            "timestamp": datetime.now().isoformat(),
        }

        # Try OpenAI first if available
        if OPENAI_AVAILABLE and self.openai_service:
            try:
                result = await self.openai_service.get_auditoria_response(comando, full_context)
                
                if result["success"]:
                    return {
                        "response": result["response"],
                        "context_used": full_context,
                        "mcp_tools_available": len(mcp_context.get("tools", [])),
                        "mcp_resources_available": len(mcp_context.get("resources", [])),
                        "provider": "OpenAI GPT",
                        "confidence": result.get("confidence", 0.8),
                        "suggestions": result.get("suggestions", []),
                        "usage": result.get("usage", {})
                    }
                else:
                    logger.warning(f"OpenAI integration failed: {result['error']}")
            except Exception as e:
                logger.error(f"Error in OpenAI integration: {e}")

        # Fallback to mock response
        return {
            "response": f"Enhanced LLM response for: {comando}",
            "context_used": full_context,
            "mcp_tools_available": len(mcp_context.get("tools", [])),
            "mcp_resources_available": len(mcp_context.get("resources", [])),
            "provider": "Fallback",
            "note": "OpenAI integration not available"
        }

    async def _get_mcp_context(self) -> Dict[str, Any]:
        """Get current MCP context (available tools and resources)"""
        if not MCP_AVAILABLE or not self.mcp_server:
            return {"tools": [], "resources": []}

        tools = list(self.mcp_server._tools.keys())
        resources = list(self.mcp_server._resources.keys())

        return {
            "tools": tools,
            "resources": resources,
            "server_status": "ready" if self.status == "ready" else self.status,
        }

    async def get_mcp_capabilities(self) -> Dict[str, Any]:
        """Get MCP server capabilities for Copilot integration"""
        capabilities = {
            "server_info": {
                "name": "AUDITORIA360-Enhanced-Agent",
                "version": "1.0.0",
                "status": self.status,
            },
            "openai_integration": OPENAI_AVAILABLE and self.openai_service is not None,
            "mcp_integration": MCP_AVAILABLE and self.mcp_server is not None,
            "capabilities": {
                "chat_completion": OPENAI_AVAILABLE,
                "document_analysis": OPENAI_AVAILABLE,
                "personalized_recommendations": OPENAI_AVAILABLE,
                "payroll_calculation": MCP_AVAILABLE,
                "compliance_checking": MCP_AVAILABLE,
                "audit_execution": MCP_AVAILABLE,
                "cct_comparison": MCP_AVAILABLE,
            },
        }
        
        if MCP_AVAILABLE and self.mcp_server:
            tools = [tool.model_dump() for tool in self.mcp_server._tools.values()]
            resources = [
                resource.model_dump() for resource in self.mcp_server._resources.values()
            ]
            capabilities.update({
                "tools": tools,
                "resources": resources,
            })
        else:
            capabilities.update({
                "tools": [],
                "resources": [],
            })

        return capabilities

    async def handle_mcp_request(self, request_data: str) -> str:
        """Handle incoming MCP requests"""
        if not MCP_AVAILABLE or not self.mcp_server:
            raise Exception("MCP server not available")

        return await self.mcp_server.handle_request(request_data)

    # New OpenAI-specific methods
    
    async def chat_with_openai(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Direct chat with OpenAI GPT"""
        if not OPENAI_AVAILABLE or not self.openai_service:
            return {
                "success": False,
                "error": "OpenAI service not available",
                "response": None
            }
        
        return await self.openai_service.get_auditoria_response(message, context)
    
    async def analyze_document_with_ai(self, content: str, doc_type: str = "general") -> Dict[str, Any]:
        """Analyze document using OpenAI"""
        if not OPENAI_AVAILABLE or not self.openai_service:
            return {
                "success": False,
                "error": "OpenAI service not available",
                "response": None
            }
        
        return await self.openai_service.analyze_document_content(content, doc_type)
    
    async def get_ai_recommendations(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered recommendations"""
        if not OPENAI_AVAILABLE or not self.openai_service:
            return {
                "success": False,
                "error": "OpenAI service not available",
                "response": None
            }
        
        return await self.openai_service.get_recommendations(user_context)


# Backwards compatibility
class AIAgent(EnhancedAIAgent):
    """Backwards compatible AI Agent class"""

    def __init__(self, db_session_factory=None):
        super().__init__(db_session_factory)
        logger.info("AI Agent initialized with MCP support")


# Example usage and testing
if __name__ == "__main__":

    async def main():
        # Initialize enhanced agent
        agente = EnhancedAIAgent()

        # Wait for initialization
        while agente.status == "initializing":
            await asyncio.sleep(0.1)

        if agente.status == "ready":
            # Test payroll calculation
            result = await agente.executar_acao(
                "calcular folha de pagamento",
                {"employee_id": "EMP001", "base_salary": 5000.00, "overtime_hours": 10},
            )
            logger.info(f"Payroll calculation result: {result}")

            # Test compliance check
            result = await agente.executar_acao(
                "verificar compliance",
                {"employee_id": "EMP001", "check_type": "salary"},
            )
            logger.info(f"Compliance check result: {result}")

            # Test MCP capabilities
            capabilities = await agente.get_mcp_capabilities()
            logger.info(f"MCP capabilities: {capabilities}")
        else:
            logger.error(f"Agent initialization failed: {agente.status}")

    # Run the example
    asyncio.run(main())
