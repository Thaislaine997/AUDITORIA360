"""
Test MCP Integration for AUDITORIA360
Validates that the MCP components are working correctly
"""

import asyncio
import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_agent import EnhancedAIAgent
from src.mcp.config import get_config_manager
from src.mcp.protocol import ClientInfo, InitializeRequest, MCPResponse
from src.mcp.server import AuditoriaResourceProvider, MCPServer
from src.mcp.tools import AuditoriaToolProvider


class TestMCPIntegration:
    """Test suite for MCP integration"""

    @pytest.fixture
    async def mcp_server(self):
        """Create a test MCP server"""
        server = MCPServer("TestServer", "1.0.0")
        AuditoriaResourceProvider(server, None)
        AuditoriaToolProvider(server, None)
        return server

    @pytest.fixture
    def config_manager(self):
        """Create a test config manager"""
        return get_config_manager()

    def test_protocol_models(self):
        """Test MCP protocol models"""
        # Test request creation
        client_info = ClientInfo(name="TestClient", version="1.0.0")
        request = InitializeRequest(id="test-1", params=client_info.model_dump())

        assert request.method == "initialize"
        assert request.params["name"] == "TestClient"

        # Test JSON serialization
        request_json = request.model_dump_json()
        assert "initialize" in request_json
        assert "TestClient" in request_json

    async def test_server_initialization(self, mcp_server):
        """Test MCP server initialization"""
        assert mcp_server.name == "TestServer"
        assert mcp_server.version == "1.0.0"
        assert not mcp_server.initialized

        # Test initialization request
        client_info = ClientInfo(name="TestClient", version="1.0.0")
        request = InitializeRequest(id="test-1", params=client_info.model_dump())

        response_json = await mcp_server.handle_request(request.model_dump_json())
        response = MCPResponse.model_validate_json(response_json)

        assert response.error is None
        assert response.result is not None
        assert mcp_server.initialized

    async def test_tool_registration(self, mcp_server):
        """Test that tools are properly registered"""
        # Server should have tools registered by AuditoriaToolProvider
        assert len(mcp_server._tools) > 0

        tool_names = list(mcp_server._tools.keys())
        expected_tools = [
            "payroll_calculator",
            "compliance_checker",
            "document_analyzer",
            "audit_executor",
            "cct_comparator",
        ]

        for tool in expected_tools:
            assert tool in tool_names

    async def test_resource_registration(self, mcp_server):
        """Test that resources are properly registered"""
        # Server should have resources registered by AuditoriaResourceProvider
        assert len(mcp_server._resources) > 0

        resource_uris = list(mcp_server._resources.keys())
        expected_resources = [
            "auditoria://payroll/data",
            "auditoria://employees/info",
            "auditoria://cct/documents",
            "auditoria://compliance/rules",
            "auditoria://knowledge/base",
        ]

        for resource in expected_resources:
            assert resource in resource_uris

    async def test_payroll_calculator_tool(self, mcp_server):
        """Test payroll calculator tool execution"""
        tool_provider = AuditoriaToolProvider(mcp_server, None)

        result = await tool_provider._execute_payroll_calculator(
            "payroll_calculator",
            {
                "employee_id": "TEST001",
                "month": 1,
                "year": 2024,
                "base_salary": 5000.00,
                "overtime_hours": 10,
            },
        )

        assert "employee_id" in result
        assert "gross_salary" in result
        assert "net_salary" in result
        assert result["employee_id"] == "TEST001"
        assert result["gross_salary"] > 0
        assert result["net_salary"] > 0

    async def test_compliance_checker_tool(self, mcp_server):
        """Test compliance checker tool execution"""
        tool_provider = AuditoriaToolProvider(mcp_server, None)

        result = await tool_provider._execute_compliance_checker(
            "compliance_checker",
            {
                "employee_id": "TEST001",
                "check_type": "salary",
                "payroll_data": {"base_salary": 1000.00},  # Below minimum wage
            },
        )

        assert "employee_id" in result
        assert "compliant" in result
        assert "violations" in result
        assert result["employee_id"] == "TEST001"
        # Should have violations for low salary
        assert len(result["violations"]) > 0

    def test_config_loading(self, config_manager):
        """Test configuration loading"""
        config = config_manager.load_config()

        assert config.version == "1.0.0"
        assert "auditoria360-main" in config.servers
        assert config.copilot.enabled is True
        assert len(config.copilot.tools_enabled) > 0

    def test_config_validation(self, config_manager):
        """Test configuration validation"""
        config_manager.load_config()
        errors = config_manager.validate_config()

        # Should have no validation errors
        assert len(errors) == 0

    async def test_enhanced_ai_agent_initialization(self):
        """Test enhanced AI agent initialization"""
        agent = EnhancedAIAgent()

        # Wait for initialization (with timeout)
        max_wait = 10
        waited = 0
        while agent.status == "initializing" and waited < max_wait:
            await asyncio.sleep(0.1)
            waited += 1

        assert agent.status in ["ready", "error"]  # Should be one of these

        if agent.status == "ready":
            # Test MCP capabilities
            capabilities = await agent.get_mcp_capabilities()
            assert "tools" in capabilities
            assert "resources" in capabilities
            assert len(capabilities["tools"]) > 0
            assert len(capabilities["resources"]) > 0


# Standalone test functions for pytest compatibility


def test_mcp_protocol_models():
    """Test MCP protocol models"""
    test_instance = TestMCPIntegration()
    test_instance.test_protocol_models()


@pytest.mark.asyncio
async def test_mcp_server_basic():
    """Test basic MCP server functionality"""
    server = MCPServer("TestServer", "1.0.0")
    AuditoriaResourceProvider(server, None)
    AuditoriaToolProvider(server, None)

    # Test initialization
    client_info = ClientInfo(name="TestClient", version="1.0.0")
    request = InitializeRequest(id="test-1", params=client_info.model_dump())

    response_json = await server.handle_request(request.model_dump_json())
    response = MCPResponse.model_validate_json(response_json)

    assert response.error is None
    assert server.initialized


@pytest.mark.asyncio
async def test_payroll_calculation():
    """Test payroll calculation via MCP"""
    server = MCPServer("TestServer", "1.0.0")
    tool_provider = AuditoriaToolProvider(server, None)

    result = await tool_provider._execute_payroll_calculator(
        "payroll_calculator",
        {"employee_id": "TEST001", "month": 1, "year": 2024, "base_salary": 3000.00},
    )

    assert result["employee_id"] == "TEST001"
    assert result["gross_salary"] == 3000.00
    assert result["net_salary"] > 0


if __name__ == "__main__":
    """Run tests directly"""
    print("🧪 Running MCP Integration Tests...")

    # Run async tests
    async def run_async_tests():
        print("Testing server initialization...")
        await test_mcp_server_basic()
        print("✅ Server initialization test passed")

        print("Testing payroll calculation...")
        await test_payroll_calculation()
        print("✅ Payroll calculation test passed")

        print("Testing enhanced AI agent...")
        test_instance = TestMCPIntegration()
        await test_instance.test_enhanced_ai_agent_initialization()
        print("✅ Enhanced AI agent test passed")

    # Run sync tests
    print("Testing protocol models...")
    test_mcp_protocol_models()
    print("✅ Protocol models test passed")

    # Run async tests
    asyncio.run(run_async_tests())

    print("🎉 All MCP integration tests passed!")
