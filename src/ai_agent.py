"""
Enhanced AI Agent with Model Context Protocol (MCP) Integration
Extends Copilot coding agent capabilities with AUDITORIA360 specific tools and resources
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from .mcp.config import MCPConfiguration, get_config_manager
from .mcp.server import AuditoriaResourceProvider, MCPServer
from .mcp.tools import AuditoriaToolProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedAIAgent:
    """Enhanced AI Agent with MCP integration for AUDITORIA360"""

    def __init__(self, db_session_factory=None):
        self.status = "initializing"
        self.db_session_factory = db_session_factory

        # MCP Components
        self.mcp_server: Optional[MCPServer] = None
        self.mcp_client_manager: Optional[MCPClientManager] = None
        self.resource_provider: Optional[AuditoriaResourceProvider] = None
        self.tool_provider: Optional[AuditoriaToolProvider] = None

        # Configuration
        self.config_manager = get_config_manager()
        self.config: Optional[MCPConfiguration] = None

        # Initialize MCP components
        asyncio.create_task(self._initialize_mcp())

        logger.info("Enhanced AI Agent with MCP integration initialized")

    async def _initialize_mcp(self):
        """Initialize MCP server and client components"""
        try:
            # Load configuration
            self.config = self.config_manager.load_config()

            # Initialize MCP server
            self.mcp_server = MCPServer(
                name="AUDITORIA360-MCP-Server",
                version="1.0.0"
            )

            # Initialize resource and tool providers
            self.resource_provider = AuditoriaResourceProvider(
                self.mcp_server,
                self.db_session_factory
            )
            self.tool_provider = AuditoriaToolProvider(
                self.mcp_server,
                self.db_session_factory
            )

            # Initialize client manager
            self.mcp_client_manager = MCPClientManager()

            self.status = "ready"
            logger.info("MCP components initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing MCP components: {e}")
            self.status = "error"

    async def executar_acao(self, acao: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute an action using MCP capabilities"""
        try:
            if self.status != "ready":
                return {
                    "success": False,
                    "error": "AI Agent not ready",
                    "status": self.status
                }

            logger.info(f"Executing enhanced action: {acao}")

            # Try to interpret the action and map to MCP tools
            result = await self._process_action_with_mcp(acao, context or {})

            return {
                "success": True,
                "action": acao,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "processed_via": "MCP"
            }

        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": acao,
                "timestamp": datetime.now().isoformat()
            }

    async def _process_action_with_mcp(self, action: str, context: Dict[str, Any]) -> Any:
        """Process action using MCP tools and resources"""
        action_lower = action.lower()

        # Map actions to MCP tools
        if "calcular" in action_lower and "folha" in action_lower:
            return await self._execute_payroll_calculation(context)

        elif "verificar" in action_lower and ("compliance" in action_lower or "conformidade" in action_lower):
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

    async def _execute_payroll_calculation(self, context: Dict[str, Any]) -> Dict[str, Any]:
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
                "calculation_type": "normal"
            }
        )

        return result

    async def _execute_compliance_check(self, context: Dict[str, Any]) -> Dict[str, Any]:
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
                "payroll_data": payroll_data
            }
        )

        return result

    async def _execute_document_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
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
                "analysis_type": analysis_type
            }
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
                "period_end": period_end
            }
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
                "include_recommendations": True
            }
        )

        return result

    async def _general_ai_processing(self, action: str, context: Dict[str, Any]) -> str:
        """General AI processing for actions not mapped to specific MCP tools"""
        # This could integrate with OpenAI, Gemini, or other LLM services
        logger.info(f"Processing general action: {action}")

        return f"Processed action '{action}' with AI. Context: {json.dumps(context, indent=2)}"

    async def integrar_gemini(self, comando: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enhanced Gemini/LLM integration with MCP context"""
        logger.info(f"Integrating with Gemini/LLM: {comando}")

        # Get available MCP resources and tools for context
        mcp_context = await self._get_mcp_context()

        # Combine with provided context
        full_context = {
            "comando": comando,
            "mcp_context": mcp_context,
            "user_context": context or {},
            "timestamp": datetime.now().isoformat()
        }

        # Here you would integrate with actual Gemini/OpenAI API
        # For now, return enhanced mock response

        return {
            "response": f"Enhanced Gemini response for: {comando}",
            "context_used": full_context,
            "mcp_tools_available": len(mcp_context.get("tools", [])),
            "mcp_resources_available": len(mcp_context.get("resources", []))
        }

    async def _get_mcp_context(self) -> Dict[str, Any]:
        """Get current MCP context (available tools and resources)"""
        if not self.mcp_server:
            return {"tools": [], "resources": []}

        tools = list(self.mcp_server._tools.keys())
        resources = list(self.mcp_server._resources.keys())

        return {
            "tools": tools,
            "resources": resources,
            "server_status": "ready" if self.status == "ready" else self.status
        }

    async def get_mcp_capabilities(self) -> Dict[str, Any]:
        """Get MCP server capabilities for Copilot integration"""
        if not self.mcp_server:
            return {"error": "MCP server not initialized"}

        tools = [tool.model_dump() for tool in self.mcp_server._tools.values()]
        resources = [resource.model_dump() for resource in self.mcp_server._resources.values()]

        return {
            "server_info": {
                "name": self.mcp_server.name,
                "version": self.mcp_server.version,
                "status": self.status
            },
            "tools": tools,
            "resources": resources,
            "capabilities": {
                "payroll_calculation": True,
                "compliance_checking": True,
                "document_analysis": True,
                "audit_execution": True,
                "cct_comparison": True
            }
        }

    async def handle_mcp_request(self, request_data: str) -> str:
        """Handle incoming MCP requests"""
        if not self.mcp_server:
            raise Exception("MCP server not initialized")

        return await self.mcp_server.handle_request(request_data)


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
                {
                    "employee_id": "EMP001",
                    "base_salary": 5000.00,
                    "overtime_hours": 10
                }
            )
            logger.info(f"Payroll calculation result: {result}")

            # Test compliance check
            result = await agente.executar_acao(
                "verificar compliance",
                {
                    "employee_id": "EMP001",
                    "check_type": "salary"
                }
            )
            logger.info(f"Compliance check result: {result}")

            # Test MCP capabilities
            capabilities = await agente.get_mcp_capabilities()
            logger.info(f"MCP capabilities: {capabilities}")
        else:
            logger.error(f"Agent initialization failed: {agente.status}")

    # Run the example
    asyncio.run(main())
