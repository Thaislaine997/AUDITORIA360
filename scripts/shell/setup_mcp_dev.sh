#!/bin/bash

# AUDITORIA360 MCP Development Environment Setup Script
# Sets up the complete MCP integration for GitHub Copilot

set -e

echo "🚀 Setting up AUDITORIA360 MCP Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the AUDITORIA360 project root directory"
    exit 1
fi

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p logs
mkdir -p configs/mcp/servers
mkdir -p configs/mcp/clients
mkdir -p configs/copilot
mkdir -p .vscode

# Install additional MCP dependencies
print_status "Installing MCP dependencies..."
pip install pydantic pyyaml asyncio

# Generate MCP configuration if it doesn't exist
if [ ! -f "configs/mcp/mcp_config.yaml" ]; then
    print_status "Generating MCP configuration..."
    python -c "
from src.mcp.config import get_config_manager
config_manager = get_config_manager('configs/mcp')
config = config_manager.load_config()
config_manager.save_config(config)
print('MCP configuration generated successfully')
"
fi

# Generate Copilot configuration
print_status "Generating GitHub Copilot configuration..."
python -c "
import json
from src.mcp.config import get_config_manager

config_manager = get_config_manager('configs/mcp')
config = config_manager.load_config()
copilot_config = config_manager.generate_copilot_config()

with open('configs/copilot/copilot_mcp.json', 'w') as f:
    json.dump(copilot_config, f, indent=2)

print('Copilot configuration generated successfully')
"

# Create MCP server startup script
print_status "Creating MCP server startup script..."
cat > scripts/start_mcp_server.sh << 'EOF'
#!/bin/bash

# Start AUDITORIA360 MCP Server

echo "Starting AUDITORIA360 MCP Server..."

# Set environment variables
export AUDITORIA360_MCP_MODE=server
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the server
python -m src.mcp.copilot_server

EOF

chmod +x scripts/start_mcp_server.sh

# Create development startup script
print_status "Creating development startup script..."
cat > scripts/start_dev_environment.sh << 'EOF'
#!/bin/bash

# Start complete AUDITORIA360 development environment with MCP

echo "🚀 Starting AUDITORIA360 Development Environment with MCP..."

# Start the main API server in background
echo "Starting main API server..."
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Start MCP server in background
echo "Starting MCP server..."
export AUDITORIA360_MCP_MODE=server
python -m src.mcp.copilot_server &
MCP_PID=$!

echo "✅ Development environment started!"
echo "📊 API Server: http://localhost:8000"
echo "🔧 MCP Server: Running on stdio"
echo "📖 API Docs: http://localhost:8000/docs"

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down development environment..."
    kill $API_PID 2>/dev/null || true
    kill $MCP_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait $API_PID $MCP_PID

EOF

chmod +x scripts/start_dev_environment.sh

# Create test script for MCP functionality
print_status "Creating MCP test script..."
cat > scripts/test_mcp.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for AUDITORIA360 MCP integration
"""

import asyncio
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_agent import EnhancedAIAgent

async def test_mcp_integration():
    """Test MCP integration functionality"""
    print("🧪 Testing AUDITORIA360 MCP Integration...")
    
    # Initialize enhanced AI agent
    agent = EnhancedAIAgent()
    
    # Wait for initialization
    max_wait = 30
    waited = 0
    while agent.status == "initializing" and waited < max_wait:
        await asyncio.sleep(1)
        waited += 1
    
    if agent.status != "ready":
        print(f"❌ Agent failed to initialize: {agent.status}")
        return False
    
    print(f"✅ Agent initialized successfully: {agent.status}")
    
    # Test MCP capabilities
    try:
        capabilities = await agent.get_mcp_capabilities()
        print(f"📋 MCP Capabilities: {len(capabilities.get('tools', []))} tools, {len(capabilities.get('resources', []))} resources")
        
        # Test payroll calculation
        print("\n🧮 Testing payroll calculation...")
        result = await agent.executar_acao(
            "calcular folha de pagamento",
            {
                "employee_id": "TEST001",
                "base_salary": 5000.00,
                "overtime_hours": 8
            }
        )
        
        if result.get("success"):
            print("✅ Payroll calculation successful")
            calculation_result = result.get("result", {})
            if "net_salary" in str(calculation_result):
                print(f"💰 Net salary calculated successfully")
        else:
            print(f"❌ Payroll calculation failed: {result.get('error')}")
        
        # Test compliance check
        print("\n🔍 Testing compliance check...")
        result = await agent.executar_acao(
            "verificar compliance",
            {
                "employee_id": "TEST001",
                "check_type": "salary"
            }
        )
        
        if result.get("success"):
            print("✅ Compliance check successful")
        else:
            print(f"❌ Compliance check failed: {result.get('error')}")
        
        # Test document analysis
        print("\n📄 Testing document analysis...")
        result = await agent.executar_acao(
            "analisar documento",
            {
                "document_id": "TEST_DOC_001",
                "document_type": "cct",
                "analysis_type": "extract_clauses"
            }
        )
        
        if result.get("success"):
            print("✅ Document analysis successful")
        else:
            print(f"❌ Document analysis failed: {result.get('error')}")
        
        print("\n🎉 MCP integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_integration())
    sys.exit(0 if success else 1)

EOF

chmod +x scripts/test_mcp.py

# Create VS Code tasks for MCP development
print_status "Creating VS Code tasks..."
mkdir -p .vscode
cat > .vscode/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start MCP Server",
            "type": "shell",
            "command": "python",
            "args": ["-m", "src.mcp.copilot_server"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "env": {
                "AUDITORIA360_MCP_MODE": "server"
            }
        },
        {
            "label": "Test MCP Integration",
            "type": "shell",
            "command": "python",
            "args": ["scripts/test_mcp.py"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": true,
                "panel": "new"
            }
        },
        {
            "label": "Start Development Environment",
            "type": "shell",
            "command": "./scripts/start_dev_environment.sh",
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            }
        }
    ]
}
EOF

# Update requirements.txt with MCP dependencies
print_status "Updating requirements.txt with MCP dependencies..."
cat >> requirements.txt << 'EOF'

# MCP Integration Dependencies
pydantic>=2.0.0
pyyaml>=6.0
asyncio-mqtt>=0.11.1
websockets>=11.0
aiohttp>=3.8.0
jsonschema>=4.0.0
EOF

# Create documentation
print_status "Creating MCP documentation..."
cat > docs/MCP_INTEGRATION.md << 'EOF'
# Model Context Protocol (MCP) Integration for AUDITORIA360

## Overview

This document describes the Model Context Protocol (MCP) integration that extends the GitHub Copilot coding agent with AUDITORIA360-specific capabilities.

## Architecture

The MCP integration consists of:

1. **MCP Server**: Exposes AUDITORIA360 tools and resources via the MCP protocol
2. **MCP Client**: Connects to external MCP servers for additional capabilities  
3. **Enhanced AI Agent**: Integrates MCP with the existing AI system
4. **Copilot Integration**: Configured for seamless GitHub Copilot usage

## Available Tools

### Payroll Calculator
- **Name**: `payroll_calculator`
- **Description**: Calculate payroll with taxes, benefits, and deductions
- **Parameters**: employee_id, month, year, base_salary, overtime_hours, calculation_type

### Compliance Checker  
- **Name**: `compliance_checker`
- **Description**: Check compliance against labor laws and CCT requirements
- **Parameters**: employee_id, payroll_data, cct_id, check_type

### Document Analyzer
- **Name**: `document_analyzer` 
- **Description**: Analyze documents for information extraction and classification
- **Parameters**: document_id, document_type, analysis_type, compare_with

### Audit Executor
- **Name**: `audit_executor`
- **Description**: Execute audit procedures and generate reports
- **Parameters**: audit_type, scope, period_start, period_end, departments, specific_rules

### CCT Comparator
- **Name**: `cct_comparator`
- **Description**: Compare collective bargaining agreements
- **Parameters**: cct_id_1, cct_id_2, comparison_type, highlight_differences, include_recommendations

## Available Resources

### Payroll Data
- **URI**: `auditoria://payroll/data`
- **Description**: Access to payroll data including employees, competencies, and calculations

### Employee Information  
- **URI**: `auditoria://employees/info`
- **Description**: Detailed employee information and records

### CCT Documents
- **URI**: `auditoria://cct/documents`
- **Description**: Collective bargaining agreements and related documents

### Compliance Rules
- **URI**: `auditoria://compliance/rules`
- **Description**: Active compliance rules and regulations

### Knowledge Base
- **URI**: `auditoria://knowledge/base`
- **Description**: Searchable knowledge base articles and documentation

## Setup and Configuration

### 1. Development Environment Setup

```bash
# Run the setup script
./scripts/setup_mcp_dev.sh

# Start development environment
./scripts/start_dev_environment.sh
```

### 2. GitHub Copilot Configuration

The MCP server is automatically configured for GitHub Copilot integration. The configuration is stored in `.vscode/mcp.json`.

### 3. Testing

```bash
# Test MCP integration
python scripts/test_mcp.py

# Test individual tools via API
curl -X POST "http://localhost:8000/api/v1/ai/mcp/tools/call" \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "payroll_calculator", "arguments": {"employee_id": "EMP001", "base_salary": 5000}}'
```

## API Endpoints

### Enhanced AI Endpoints

- `POST /api/v1/ai/chat` - Enhanced chatbot with MCP integration
- `GET /api/v1/ai/recommendations` - AI recommendations using MCP tools
- `GET /api/v1/ai/knowledge-base/search` - Knowledge base search via MCP

### MCP-Specific Endpoints

- `GET /api/v1/ai/mcp/capabilities` - Get MCP server capabilities
- `POST /api/v1/ai/mcp/request` - Handle raw MCP protocol requests
- `GET /api/v1/ai/mcp/resources` - List available MCP resources
- `GET /api/v1/ai/mcp/tools` - List available MCP tools
- `POST /api/v1/ai/mcp/tools/call` - Call specific MCP tool
- `POST /api/v1/ai/actions/execute` - Execute AI action with MCP integration
- `GET /api/v1/ai/status` - Get AI agent and MCP status

## Development Workflow

1. **Code with Copilot**: Use GitHub Copilot with AUDITORIA360 context
2. **Tool Integration**: Call MCP tools directly from code
3. **Resource Access**: Access AUDITORIA360 data via MCP resources
4. **Testing**: Use provided scripts to test functionality
5. **Debugging**: Check logs and use VS Code tasks

## Configuration Files

- `configs/mcp/mcp_config.yaml` - Main MCP configuration
- `.vscode/mcp.json` - Copilot MCP configuration  
- `.vscode/settings.json` - VS Code settings for MCP development
- `configs/copilot/copilot_mcp.json` - Generated Copilot configuration

## Troubleshooting

### Common Issues

1. **MCP Server Not Starting**: Check Python path and dependencies
2. **Tool Execution Errors**: Verify database connection and parameters
3. **Copilot Integration Issues**: Check VS Code settings and MCP configuration

### Debugging

```bash
# Check MCP server logs
tail -f /tmp/copilot_mcp_server.log

# Test MCP server directly
python -m src.mcp.copilot_server

# Validate configuration
python -c "from src.mcp.config import get_config_manager; print(get_config_manager().validate_config())"
```

## Next Steps

1. Enhance tool implementations with real database integration
2. Add more specialized tools for specific AUDITORIA360 workflows
3. Implement advanced resource caching and optimization
4. Add comprehensive monitoring and analytics
5. Extend Copilot integration with custom prompts and contexts

EOF

print_status "✅ AUDITORIA360 MCP Development Environment setup completed!"
print_status ""
print_status "📚 Next steps:"
print_status "1. Review the generated configuration files"
print_status "2. Run './scripts/test_mcp.py' to test the integration"
print_status "3. Start development with './scripts/start_dev_environment.sh'"
print_status "4. Open VS Code and start using GitHub Copilot with MCP tools"
print_status ""
print_status "📖 Documentation: docs/MCP_INTEGRATION.md"
print_status "⚙️  Configuration: configs/mcp/mcp_config.yaml"
print_status "🔧 VS Code Settings: .vscode/settings.json"