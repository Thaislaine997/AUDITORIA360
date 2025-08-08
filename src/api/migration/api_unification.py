"""
API Unification Protocol - A Metamorfose Phase I
================================================================

This module implements the protocol for sunsetting the legacy API
and consolidating all functionality into the unified src/api structure.

Economic Consciousness: Reduce debt by consolidating API surfaces
Strategic Consciousness: Single source of truth for API development
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class APIUnificationProtocol:
    """
    The Protocol for Sunsetting Legacy API and Unifying Architecture
    """

    def __init__(self):
        self.legacy_api_path = Path("api")
        self.unified_api_path = Path("src/api")
        self.sunset_date = datetime.now() + timedelta(days=90)  # 90 days to sunset
        self.migration_tickets = []

    def analyze_legacy_api(self) -> Dict[str, Any]:
        """
        Analyze legacy API structure and identify critical functionality
        """
        logger.info("🔍 Analyzing legacy API structure...")

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "legacy_endpoints": [],
            "critical_functions": [],
            "migration_complexity": "low",
            "estimated_effort_hours": 0,
            "sunset_date": self.sunset_date.isoformat(),
            "status": "analysis_complete",
        }

        # Analyze api/index.py
        if self.legacy_api_path.exists():
            try:
                with open(self.legacy_api_path / "index.py", "r") as f:
                    content = f.read()

                # Extract endpoint patterns
                import re

                endpoints = re.findall(
                    r'@app\.(get|post|put|delete)\("([^"]+)"', content
                )

                analysis["legacy_endpoints"] = [
                    {
                        "method": method.upper(),
                        "path": path,
                        "status": "needs_migration",
                    }
                    for method, path in endpoints
                ]

                # Identify critical functions based on complexity
                if len(endpoints) > 10:
                    analysis["migration_complexity"] = "high"
                    analysis["estimated_effort_hours"] = len(endpoints) * 2
                elif len(endpoints) > 5:
                    analysis["migration_complexity"] = "medium"
                    analysis["estimated_effort_hours"] = len(endpoints) * 1.5
                else:
                    analysis["estimated_effort_hours"] = len(endpoints) * 1

                # Critical functions are those with business logic
                business_patterns = ["auditoria", "payroll", "auth", "compliance"]
                analysis["critical_functions"] = [
                    ep
                    for ep in analysis["legacy_endpoints"]
                    if any(
                        pattern in ep["path"].lower() for pattern in business_patterns
                    )
                ]

                logger.info(f"✅ Found {len(endpoints)} endpoints in legacy API")
                logger.info(
                    f"⚠️  {len(analysis['critical_functions'])} critical functions identified"
                )

            except Exception as e:
                logger.error(f"❌ Error analyzing legacy API: {e}")
                analysis["status"] = "analysis_failed"
                analysis["error"] = str(e)
        else:
            logger.warning("⚠️  Legacy API path not found")

        return analysis

    def generate_migration_tickets(
        self, analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate automated migration tickets for MCP agents
        """
        logger.info("🎫 Generating migration tickets...")

        tickets = []

        for i, endpoint in enumerate(analysis.get("legacy_endpoints", [])):
            ticket = {
                "id": f"UNIFY-{i+1:03d}",
                "title": f"Migrate {endpoint['method']} {endpoint['path']}",
                "type": "api_migration",
                "priority": (
                    "high"
                    if endpoint in analysis.get("critical_functions", [])
                    else "medium"
                ),
                "description": f"Migrate legacy endpoint {endpoint['method']} {endpoint['path']} to unified API structure",
                "acceptance_criteria": [
                    f"Endpoint functionality preserved in src/api/routers/",
                    "Legacy endpoint marked as deprecated",
                    "Tests updated to use new endpoint",
                    "Documentation updated",
                ],
                "assigned_agent": "mcp_migration_agent",
                "estimated_hours": (
                    2 if endpoint in analysis.get("critical_functions", []) else 1
                ),
                "status": "ready_for_work",
                "created_at": datetime.now().isoformat(),
                "sunset_deadline": self.sunset_date.isoformat(),
            }
            tickets.append(ticket)

        # Add infrastructure tickets
        if analysis.get("legacy_endpoints"):
            tickets.append(
                {
                    "id": "UNIFY-INFRA-001",
                    "title": "Setup API deprecation warnings",
                    "type": "infrastructure",
                    "priority": "high",
                    "description": "Add deprecation warnings to legacy API endpoints",
                    "acceptance_criteria": [
                        "All legacy endpoints return deprecation headers",
                        "Deprecation notices logged",
                        "Sunset date communicated to clients",
                    ],
                    "assigned_agent": "mcp_infrastructure_agent",
                    "estimated_hours": 4,
                    "status": "ready_for_work",
                    "created_at": datetime.now().isoformat(),
                }
            )

        self.migration_tickets = tickets
        logger.info(f"✅ Generated {len(tickets)} migration tickets")

        return tickets

    def create_sunset_timeline(self) -> Dict[str, Any]:
        """
        Create timeline for sunsetting legacy API
        """
        now = datetime.now()

        timeline = {
            "phase_1_migration": {
                "start": now.isoformat(),
                "end": (now + timedelta(days=30)).isoformat(),
                "description": "Migrate critical endpoints and add deprecation warnings",
                "deliverables": [
                    "Critical endpoints migrated",
                    "Deprecation warnings active",
                ],
            },
            "phase_2_validation": {
                "start": (now + timedelta(days=30)).isoformat(),
                "end": (now + timedelta(days=60)).isoformat(),
                "description": "Validate all migrations and update documentation",
                "deliverables": [
                    "All endpoints tested",
                    "Documentation updated",
                    "Client migration guide",
                ],
            },
            "phase_3_sunset": {
                "start": (now + timedelta(days=60)).isoformat(),
                "end": self.sunset_date.isoformat(),
                "description": "Legacy API marked as deprecated, final cleanup",
                "deliverables": ["Legacy API returns 410 Gone", "Clean codebase"],
            },
        }

        return timeline

    def implement_deprecation_warnings(self):
        """
        Add deprecation warnings to legacy API endpoints
        """
        logger.info("⚠️  Implementing deprecation warnings...")

        # Create middleware for legacy API deprecation
        deprecation_middleware = '''
"""
Legacy API Deprecation Middleware
Added by API Unification Protocol
"""

from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LegacyAPIDeprecationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add deprecation warnings to legacy API endpoints
    """
    
    def __init__(self, app, sunset_date: str = "{sunset_date}"):
        super().__init__(app)
        self.sunset_date = sunset_date
        
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add deprecation headers to all responses
        response.headers["X-API-Deprecated"] = "true"
        response.headers["X-API-Sunset-Date"] = self.sunset_date
        response.headers["X-API-Migration-Guide"] = "/docs/api-migration"
        response.headers["Deprecation"] = self.sunset_date
        
        # Log deprecation usage
        logger.warning(f"DEPRECATED API USAGE: {{request.method}} {{request.url.path}} from {{request.client.host}}")
        
        return response
'''.format(
            sunset_date=self.sunset_date.isoformat()
        )

        # Write deprecation middleware
        middleware_path = Path("api/deprecation_middleware.py")
        try:
            with open(middleware_path, "w") as f:
                f.write(deprecation_middleware)
            logger.info(f"✅ Created deprecation middleware at {middleware_path}")
        except Exception as e:
            logger.error(f"❌ Failed to create deprecation middleware: {e}")

    def execute_unification_protocol(self) -> Dict[str, Any]:
        """
        Execute the complete API unification protocol
        """
        logger.info("🚀 Executing API Unification Protocol...")

        # Step 1: Analyze legacy API
        analysis = self.analyze_legacy_api()

        # Step 2: Generate migration tickets
        tickets = self.generate_migration_tickets(analysis)

        # Step 3: Create sunset timeline
        timeline = self.create_sunset_timeline()

        # Step 4: Implement deprecation warnings
        self.implement_deprecation_warnings()

        # Compile protocol execution report
        report = {
            "protocol": "API_UNIFICATION",
            "status": "INITIATED",
            "execution_timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "migration_tickets": tickets,
            "sunset_timeline": timeline,
            "economic_impact": {
                "debt_reduction_target": "50%",
                "knowledge_consolidation": "single_api_surface",
                "maintenance_overhead": "reduced",
                "developer_cognitive_load": "decreased",
            },
            "next_actions": [
                "Assign MCP agents to migration tickets",
                "Begin Phase 1 migration",
                "Monitor legacy API usage",
                "Communicate sunset timeline to stakeholders",
            ],
        }

        # Save report
        report_path = Path("src/api/migration/unification_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
            logger.info(f"✅ Unification protocol report saved to {report_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")

        logger.info("🎯 API Unification Protocol execution complete")
        return report


def execute_api_unification():
    """
    Main function to execute API unification protocol
    """
    protocol = APIUnificationProtocol()
    return protocol.execute_unification_protocol()


if __name__ == "__main__":
    execute_api_unification()
