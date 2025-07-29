"""
MCP Server for GitHub Copilot Integration
Specialized MCP server that integrates with GitHub Copilot for code assistance
"""

import asyncio
import sys
import json
import logging
from typing import Dict, Any
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.mcp.server import MCPServer, AuditoriaResourceProvider
from src.mcp.tools import AuditoriaToolProvider
from src.mcp.config import get_config_manager


logger = logging.getLogger(__name__)


class CopilotMCPServer:
    """Specialized MCP server for GitHub Copilot integration"""
    
    def __init__(self):
        self.server = MCPServer(
            name="AUDITORIA360-Copilot-MCP",
            version="1.0.0"
        )
        
        # Initialize providers (without database for Copilot mode)
        self.resource_provider = AuditoriaResourceProvider(self.server, None)
        self.tool_provider = AuditoriaToolProvider(self.server, None)
        
        logger.info("Copilot MCP Server initialized")
    
    async def run_stdio(self):
        """Run MCP server in stdio mode for Copilot integration"""
        logger.info("Starting Copilot MCP Server in stdio mode")
        
        try:
            while True:
                # Read request from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Process MCP request
                    response = await self.server.handle_request(line)
                    
                    # Write response to stdout
                    print(response, flush=True)
                    
                except Exception as e:
                    # Send error response
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("Copilot MCP Server stopped")
        except Exception as e:
            logger.error(f"Error in Copilot MCP Server: {e}")


async def main():
    """Main entry point for Copilot MCP server"""
    # Configure logging for Copilot mode
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/tmp/copilot_mcp_server.log'),
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    # Create and run server
    server = CopilotMCPServer()
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())