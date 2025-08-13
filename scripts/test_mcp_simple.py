#!/usr/bin/env python3
"""
Simple MCP Integration Test Runner for AUDITORIA360

This script has been moved to the centralized test structure.
Please use pytest to run the tests:

    pytest tests/integration/mcp/test_mcp_integration_simple.py -v

Or run all MCP integration tests:

    pytest tests/integration/mcp/ -v

For all tests:

    pytest tests/ -v
"""

import subprocess
import sys


def main():
    print("🚀 AUDITORIA360 MCP Integration Tests")
    print("=" * 50)
    print("This script has been reorganized into the centralized test structure.")
    print("\nTo run MCP integration tests, use:")
    print("  pytest tests/integration/mcp/test_mcp_integration_simple.py -v")
    print("\nTo run all tests:")
    print("  pytest tests/ -v")
    print("\nRunning MCP integration tests now...")
    print("=" * 50)

    # Run the pytest command
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/integration/mcp/test_mcp_integration_simple.py",
            "-v",
        ],
        cwd="../../..",
    )

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
