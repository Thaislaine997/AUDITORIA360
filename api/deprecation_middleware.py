
"""
Enhanced Legacy API Deprecation Middleware
==========================================

Advanced middleware for managing API deprecation with automatic ticket generation,
detailed analytics, and intelligent migration guidance via MCP.
"""

from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import logging
import json
import asyncio
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


class DeprecationLevel(Enum):
    """API deprecation levels"""
    WARNING = "warning"
    DEPRECATED = "deprecated"
    SUNSET = "sunset"
    REMOVED = "removed"


@dataclass
class DeprecatedEndpoint:
    """Represents a deprecated API endpoint"""
    endpoint: str
    method: str
    deprecation_level: DeprecationLevel
    deprecation_date: str
    sunset_date: str
    replacement_endpoint: Optional[str]
    migration_guide: str
    usage_count: int
    active_clients: List[str]
    business_impact: str


@dataclass
class MigrationTicket:
    """Automated migration ticket"""
    ticket_id: str
    title: str
    description: str
    endpoint: str
    client_id: str
    priority: str
    estimated_effort: str
    migration_deadline: str
    auto_generated: bool
    created_date: str
    assigned_team: str
    status: str
    migration_steps: List[str]


class EnhancedLegacyAPIDeprecationMiddleware(BaseHTTPMiddleware):
    """
    Enhanced middleware to handle legacy API deprecation with intelligent migration support
    """
    
    def __init__(self, app, sunset_date: str = "2025-11-04T18:47:01.899697"):
        super().__init__(app)
        self.sunset_date = sunset_date
        self.deprecated_endpoints = {}
        self.usage_analytics = {}
        self.migration_tickets = []
        
        # Initialize deprecation management
        self.initialize_deprecation_config()
        self.create_directories()
        
    def create_directories(self):
        """Create necessary directories for deprecation management"""
        directories = [
            "api/deprecation",
            "api/deprecation/logs",
            "api/deprecation/tickets", 
            "api/deprecation/analytics"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def initialize_deprecation_config(self):
        """Initialize deprecation configuration with intelligent defaults"""
        # Define legacy API endpoints that need deprecation
        legacy_endpoints = [
            {
                "endpoint": "/api/v1/legacy/auditoria",
                "method": "GET",
                "deprecation_level": DeprecationLevel.DEPRECATED,
                "deprecation_date": "2024-01-01T00:00:00",
                "sunset_date": self.sunset_date,
                "replacement_endpoint": "/api/v2/audits",
                "migration_guide": "Use /api/v2/audits with enhanced security and filtering capabilities",
                "usage_count": 0,
                "active_clients": [],
                "business_impact": "medium"
            },
            {
                "endpoint": "/api/v1/legacy/rpa",
                "method": "POST",
                "deprecation_level": DeprecationLevel.WARNING,
                "deprecation_date": "2024-06-01T00:00:00",
                "sunset_date": self.sunset_date,
                "replacement_endpoint": "/api/v2/automation/rpa",
                "migration_guide": "Migrate to new RPA API with enhanced security quarantine and threat detection",
                "usage_count": 0,
                "active_clients": [],
                "business_impact": "high"
            },
            {
                "endpoint": "/api/v1/legacy/reports",
                "method": "GET",
                "deprecation_level": DeprecationLevel.SUNSET,
                "deprecation_date": "2023-01-01T00:00:00",
                "sunset_date": "2025-03-01T00:00:00",
                "replacement_endpoint": "/api/v2/analytics/reports",
                "migration_guide": "Use new analytics API with real-time ROI cognitive metrics and enhanced insights",
                "usage_count": 0,
                "active_clients": [],
                "business_impact": "critical"
            },
            {
                "endpoint": "/api/v1/legacy/auth",
                "method": "POST",
                "deprecation_level": DeprecationLevel.DEPRECATED,
                "deprecation_date": "2024-03-01T00:00:00",
                "sunset_date": self.sunset_date,
                "replacement_endpoint": "/api/v2/auth/enhanced",
                "migration_guide": "Migrate to enhanced authentication with MFA, audit trails, and collective mind consensus",
                "usage_count": 0,
                "active_clients": [],
                "business_impact": "critical"
            }
        ]
        
        # Convert to DeprecatedEndpoint objects
        for endpoint_data in legacy_endpoints:
            endpoint = DeprecatedEndpoint(**endpoint_data)
            self.deprecated_endpoints[f"{endpoint.method}:{endpoint.endpoint}"] = endpoint
            
        logger.info(f"🔧 Initialized deprecation config for {len(legacy_endpoints)} legacy endpoints")
        
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Extract request information
        method = request.method
        path = str(request.url.path)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        client_id = self._extract_client_id(request)
        
        # Check if this is a deprecated endpoint
        endpoint_key = f"{method}:{path}"
        
        # Add standard deprecation headers to all legacy endpoints
        if "/api/v1/" in path or "legacy" in path.lower():
            response.headers["X-API-Deprecated"] = "true"
            response.headers["X-API-Sunset-Date"] = self.sunset_date
            response.headers["X-API-Migration-Guide"] = "/docs/api-migration"
            response.headers["Deprecation"] = self.sunset_date
            
            # Log general legacy API usage
            logger.warning(f"LEGACY API USAGE: {method} {path} from {client_ip} (client: {client_id})")
        
        # Handle specific deprecated endpoints
        if endpoint_key in self.deprecated_endpoints:
            deprecated_endpoint = self.deprecated_endpoints[endpoint_key]
            
            # Add specific deprecation handling
            await self._handle_specific_deprecation(deprecated_endpoint, request, response, client_id)
            
            # Log detailed usage
            await self._log_deprecated_usage(deprecated_endpoint, client_id, user_agent, client_ip)
            
            # Update analytics
            self._update_usage_analytics(deprecated_endpoint, client_id)
            
            # Check for automatic ticket generation
            await self._check_ticket_generation(deprecated_endpoint, client_id)
        
        return response
    
    def _extract_client_id(self, request: Request) -> str:
        """Extract client ID from request headers or authentication"""
        # Try various methods to identify the client
        client_id = (
            request.headers.get("X-Client-ID") or
            request.headers.get("Authorization", "").split(" ")[-1][:8] if request.headers.get("Authorization") else None or
            request.headers.get("X-API-Key", "")[:8] if request.headers.get("X-API-Key") else None or
            f"ip_{request.client.host}" if request.client else "unknown"
        )
        
        return client_id or "unknown"
    
    async def _handle_specific_deprecation(self, endpoint: DeprecatedEndpoint, request: Request, 
                                         response: Response, client_id: str):
        """Handle specific deprecation based on endpoint level"""
        
        # Add endpoint-specific headers
        response.headers["X-Deprecated-Endpoint"] = endpoint.endpoint
        response.headers["X-Deprecation-Level"] = endpoint.deprecation_level.value
        response.headers["X-Replacement-Endpoint"] = endpoint.replacement_endpoint or "TBD"
        response.headers["X-Migration-Priority"] = endpoint.business_impact
        
        # Level-specific handling
        if endpoint.deprecation_level == DeprecationLevel.WARNING:
            response.headers["Warning"] = f'299 - "API endpoint will be deprecated on {endpoint.deprecation_date}"'
            
        elif endpoint.deprecation_level == DeprecationLevel.DEPRECATED:
            response.headers["Warning"] = f'299 - "API endpoint is deprecated and will be removed on {endpoint.sunset_date}"'
            
        elif endpoint.deprecation_level == DeprecationLevel.SUNSET:
            sunset_date = datetime.fromisoformat(endpoint.sunset_date.replace('Z', '+00:00'))
            days_remaining = (sunset_date - datetime.now()).days
            
            response.headers["Warning"] = f'299 - "API endpoint will be removed in {days_remaining} days"'
            response.headers["X-Days-Until-Sunset"] = str(days_remaining)
            
            # Add critical warning for imminent sunset
            if days_remaining < 30:
                response.headers["X-Critical-Warning"] = "API_SUNSET_IMMINENT"
                
        elif endpoint.deprecation_level == DeprecationLevel.REMOVED:
            response.headers["X-API-Status"] = "REMOVED"
            # In practice, this endpoint should return 410 Gone
    
    async def _log_deprecated_usage(self, endpoint: DeprecatedEndpoint, client_id: str, 
                                  user_agent: str, client_ip: str):
        """Log detailed usage of deprecated endpoint"""
        usage_log = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint.endpoint,
            "method": endpoint.method,
            "client_id": client_id,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "deprecation_level": endpoint.deprecation_level.value,
            "sunset_date": endpoint.sunset_date,
            "replacement": endpoint.replacement_endpoint,
            "business_impact": endpoint.business_impact
        }
        
        # Append to daily log file
        log_date = datetime.now().strftime("%Y-%m-%d")
        log_file = Path(f"api/deprecation/logs/detailed_usage_{log_date}.json")
        
        try:
            # Read existing logs
            if log_file.exists():
                with open(log_file, "r") as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add new log
            logs.append(usage_log)
            
            # Keep only last 10000 entries to manage file size
            if len(logs) > 10000:
                logs = logs[-10000:]
            
            # Write back
            with open(log_file, "w") as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log detailed deprecated API usage: {e}")
    
    def _update_usage_analytics(self, endpoint: DeprecatedEndpoint, client_id: str):
        """Update comprehensive usage analytics"""
        endpoint_key = f"{endpoint.method}:{endpoint.endpoint}"
        
        # Update endpoint usage count
        endpoint.usage_count += 1
        
        # Add client to active clients list if not present
        if client_id not in endpoint.active_clients:
            endpoint.active_clients.append(client_id)
        
        # Update analytics dictionary
        if endpoint_key not in self.usage_analytics:
            self.usage_analytics[endpoint_key] = {
                "total_requests": 0,
                "unique_clients": set(),
                "daily_usage": {},
                "hourly_usage": {},
                "client_breakdown": {},
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat()
            }
        
        analytics = self.usage_analytics[endpoint_key]
        analytics["total_requests"] += 1
        analytics["unique_clients"].add(client_id)
        analytics["last_seen"] = datetime.now().isoformat()
        
        # Daily and hourly usage tracking
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        current_hour = now.strftime("%Y-%m-%d-%H")
        
        if today not in analytics["daily_usage"]:
            analytics["daily_usage"][today] = 0
        analytics["daily_usage"][today] += 1
        
        if current_hour not in analytics["hourly_usage"]:
            analytics["hourly_usage"][current_hour] = 0
        analytics["hourly_usage"][current_hour] += 1
        
        # Client breakdown
        if client_id not in analytics["client_breakdown"]:
            analytics["client_breakdown"][client_id] = {"count": 0, "first_seen": now.isoformat()}
        analytics["client_breakdown"][client_id]["count"] += 1
        analytics["client_breakdown"][client_id]["last_seen"] = now.isoformat()
    
    async def _check_ticket_generation(self, endpoint: DeprecatedEndpoint, client_id: str):
        """Intelligent ticket generation based on usage patterns and deadlines"""
        
        # Check if ticket already exists for this client/endpoint combination
        existing_ticket = next(
            (t for t in self.migration_tickets 
             if t.endpoint == endpoint.endpoint and t.client_id == client_id and t.status != "closed"),
            None
        )
        
        if existing_ticket:
            return existing_ticket
        
        should_generate_ticket = False
        priority = "medium"
        
        # Logic for ticket generation
        if endpoint.deprecation_level == DeprecationLevel.SUNSET:
            sunset_date = datetime.fromisoformat(endpoint.sunset_date.replace('Z', '+00:00'))
            days_remaining = (sunset_date - datetime.now()).days
            
            if days_remaining < 60:
                should_generate_ticket = True
                priority = "urgent" if days_remaining < 30 else "high"
                
        elif endpoint.deprecation_level == DeprecationLevel.DEPRECATED:
            # Generate tickets for active users of deprecated endpoints
            if endpoint.usage_count > 50:  # Threshold for active usage
                should_generate_ticket = True
                priority = "high" if endpoint.business_impact == "critical" else "medium"
                
        elif endpoint.deprecation_level == DeprecationLevel.WARNING:
            # Generate tickets for very frequent users to get ahead of deprecation
            if endpoint.usage_count > 200:
                should_generate_ticket = True
                priority = "medium"
        
        if should_generate_ticket:
            ticket = await self._generate_migration_ticket(endpoint, client_id, priority)
            logger.info(f"🎫 Auto-generated migration ticket {ticket.ticket_id} for {client_id}")
            return ticket
        
        return None
    
    async def _generate_migration_ticket(self, endpoint: DeprecatedEndpoint, client_id: str, priority: str) -> MigrationTicket:
        """Generate comprehensive migration ticket"""
        
        # Calculate migration deadline
        sunset_date = datetime.fromisoformat(endpoint.sunset_date.replace('Z', '+00:00'))
        buffer_days = {"urgent": 14, "high": 30, "medium": 60, "low": 90}
        migration_deadline = (sunset_date - timedelta(days=buffer_days.get(priority, 30))).isoformat()
        
        # Generate detailed migration steps
        migration_steps = [
            f"Audit current usage of {endpoint.endpoint} in client application",
            f"Review migration guide: {endpoint.migration_guide}",
            f"Plan migration to {endpoint.replacement_endpoint}",
            "Update application code and configuration",
            "Test migration in development environment",
            "Validate new endpoint security requirements",
            "Deploy changes to production",
            "Monitor post-migration performance",
            "Verify deprecated endpoint is no longer used",
            "Close migration ticket"
        ]
        
        # Add endpoint-specific steps
        if "auth" in endpoint.endpoint.lower():
            migration_steps.insert(4, "Implement enhanced authentication with MFA")
            migration_steps.insert(5, "Update token handling for collective mind consensus")
            
        elif "rpa" in endpoint.endpoint.lower():
            migration_steps.insert(4, "Review new RPA security quarantine requirements")
            migration_steps.insert(5, "Update data validation for enhanced threat detection")
            
        elif "reports" in endpoint.endpoint.lower():
            migration_steps.insert(4, "Adapt to new analytics data structure with ROI cognitive metrics")
            migration_steps.insert(5, "Implement real-time dashboard integration")
        
        # Create comprehensive ticket
        ticket = MigrationTicket(
            ticket_id=f"MIG-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
            title=f"[AUTO] Migrate from deprecated API: {endpoint.method} {endpoint.endpoint}",
            description=self._generate_comprehensive_ticket_description(endpoint, client_id),
            endpoint=endpoint.endpoint,
            client_id=client_id,
            priority=priority,
            estimated_effort=self._estimate_migration_effort(endpoint),
            migration_deadline=migration_deadline,
            auto_generated=True,
            created_date=datetime.now().isoformat(),
            assigned_team="api_migration_team",
            status="open",
            migration_steps=migration_steps
        )
        
        # Add to tickets list and save
        self.migration_tickets.append(ticket)
        await self._save_ticket(ticket)
        
        return ticket
    
    def _generate_comprehensive_ticket_description(self, endpoint: DeprecatedEndpoint, client_id: str) -> str:
        """Generate detailed, actionable ticket description"""
        sunset_date = datetime.fromisoformat(endpoint.sunset_date.replace('Z', '+00:00'))
        days_remaining = (sunset_date - datetime.now()).days
        
        description = f"""
## 🚨 Automated API Migration Required

**Client:** `{client_id}`  
**Deprecated Endpoint:** `{endpoint.method} {endpoint.endpoint}`  
**Status:** {endpoint.deprecation_level.value.title()}  
**⏰ Days Until Sunset:** {days_remaining}  
**🔄 Replacement:** `{endpoint.replacement_endpoint or 'To be determined'}`

### 📋 Migration Overview
{endpoint.migration_guide}

### 📊 Impact Assessment
- **Business Impact:** {endpoint.business_impact.title()}
- **Usage Count:** {endpoint.usage_count} requests
- **Active Clients:** {len(endpoint.active_clients)}

### 🛠️ Technical Requirements
The new API endpoint includes enhanced security features:
- 🛡️ **RPA Fortress Integration:** Advanced threat quarantine and detection
- 🤝 **Collective Mind Consensus:** Multi-agent security validation
- 🔐 **Enhanced Authentication:** MFA and audit trail requirements
- 📈 **ROI Cognitive Metrics:** Real-time performance analytics

### ⚡ Action Required
1. **Immediate:** Review this migration ticket and plan implementation
2. **Next:** Update your application to use the new endpoint
3. **Testing:** Validate integration with enhanced security features
4. **Deployment:** Complete migration before {endpoint.sunset_date}

### 🆘 Support Resources
- **Migration Guide:** `/docs/api-migration`
- **Security Documentation:** `/docs/security-protocols`
- **Support Team:** api-migration-team@auditoria360.com
- **Technical Q&A:** Schedule consultation via ticket system

### ⚠️ Important Notes
- This ticket was automatically generated by the Enhanced API Deprecation Management System
- The deprecated endpoint will be **completely removed** on {endpoint.sunset_date}
- No backward compatibility will be maintained after sunset date
- Early migration is recommended to ensure thorough testing

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC  
**Ticket System:** MCP-Enhanced Auto-Generation v2.0
        """
        
        return description.strip()
    
    def _estimate_migration_effort(self, endpoint: DeprecatedEndpoint) -> str:
        """Provide realistic effort estimates with context"""
        base_estimates = {
            "auth": "Medium (2-4 days) - Authentication changes require security validation and MFA integration",
            "rpa": "High (3-7 days) - RPA integration requires security quarantine testing and threat validation",
            "reports": "Medium (2-5 days) - Analytics migration includes ROI cognitive metrics integration",
            "audit": "Medium (2-4 days) - Audit endpoint changes require compliance validation"
        }
        
        # Check endpoint type
        for endpoint_type, estimate in base_estimates.items():
            if endpoint_type in endpoint.endpoint.lower():
                return estimate
        
        return "Low-Medium (1-3 days) - Standard endpoint migration with security validation"
    
    async def _save_ticket(self, ticket: MigrationTicket):
        """Save migration ticket with comprehensive metadata"""
        ticket_file = Path(f"api/deprecation/tickets/{ticket.ticket_id}.json")
        
        try:
            # Add metadata
            ticket_data = asdict(ticket)
            ticket_data["metadata"] = {
                "auto_generated": True,
                "generation_system": "Enhanced API Deprecation Middleware v2.0",
                "mcp_integration": True,
                "security_validated": True
            }
            
            with open(ticket_file, "w") as f:
                json.dump(ticket_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save migration ticket {ticket.ticket_id}: {e}")


# Maintain backward compatibility
class LegacyAPIDeprecationMiddleware(EnhancedLegacyAPIDeprecationMiddleware):
    """Legacy middleware class for backward compatibility"""
    pass
