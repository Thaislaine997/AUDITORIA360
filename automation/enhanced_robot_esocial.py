#!/usr/bin/env python3
"""
Enhanced eSocial automation robot with core system integration
This demonstrates how automation scripts can now access real client context
"""

import asyncio
import logging
from typing import Any, Dict, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class eSocialRobotEnhanced:
    """Enhanced eSocial robot that works with client-specific context"""

    def __init__(self, core_api_base_url: str = "http://localhost:8001"):
        self.core_api_base_url = core_api_base_url
        self.client_context: Optional[Dict[str, Any]] = None

    async def get_client_context(
        self, client_id: int, user_id: int = 1
    ) -> Dict[str, Any]:
        """Get client-specific automation context from core system"""
        try:
            url = f"{self.core_api_base_url}/api/core/automation-context/{client_id}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.client_context = data["context"]
                    logger.info(
                        f"✅ Client context loaded for {self.client_context['client']['name']}"
                    )
                    return self.client_context
                else:
                    raise Exception(
                        f"API error: {data.get('message', 'Unknown error')}"
                    )
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            logger.error(f"❌ Failed to get client context: {e}")
            # Fallback to generic context
            self.client_context = self._get_fallback_context(client_id)
            return self.client_context

    def _get_fallback_context(self, client_id: int) -> Dict[str, Any]:
        """Fallback context when core system is unavailable"""
        return {
            "client": {
                "id": client_id,
                "name": "Generic Client",
                "document_number": "00.000.000/0001-00",
                "status": "active",
            },
            "automation_config": {
                "esocial_enabled": True,
                "credentials_context": f"fallback_client_{client_id}",
            },
            "session": {
                "id": f"fallback_session_{client_id}",
                "user_id": 1,
                "timestamp": "2024-01-01T00:00:00Z",
            },
        }

    async def execute_esocial_automation(
        self, client_id: int, task_type: str = "send_events"
    ) -> Dict[str, Any]:
        """Execute eSocial automation with client-specific context"""
        logger.info(f"🤖 Starting eSocial automation for client {client_id}")

        # Get client context first
        context = await self.get_client_context(client_id)

        if not context:
            raise Exception("No client context available")

        client_info = context["client"]
        automation_config = context["automation_config"]

        logger.info(
            f"📋 Client: {client_info['name']} (CNPJ: {client_info['document_number']})"
        )
        logger.info(f"⚙️  eSocial enabled: {automation_config['esocial_enabled']}")

        # Simulate eSocial authentication with client-specific credentials
        auth_result = await self._authenticate_esocial(client_info, automation_config)
        if not auth_result["success"]:
            return {
                "success": False,
                "error": "eSocial authentication failed",
                "context": context,
            }

        # Simulate event processing
        events_result = await self._process_esocial_events(client_info, task_type)

        # Return comprehensive result
        result = {
            "success": True,
            "client": client_info["name"],
            "client_id": client_id,
            "task_type": task_type,
            "events_processed": events_result["events_count"],
            "processing_time": events_result["processing_time"],
            "context_session": context["session"]["id"],
            "automation_details": {
                "esocial_login": auth_result["login_time"],
                "events_sent": events_result["events_sent"],
                "events_confirmed": events_result["events_confirmed"],
                "warnings": events_result["warnings"],
            },
        }

        logger.info(f"✅ eSocial automation completed successfully")
        logger.info(f"📊 Events processed: {result['events_processed']}")

        return result

    async def _authenticate_esocial(
        self, client_info: Dict[str, Any], config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate eSocial authentication with client-specific credentials"""
        logger.info(f"🔐 Authenticating with eSocial for {client_info['name']}")

        # Simulate authentication delay
        await asyncio.sleep(1)

        # In real implementation, this would use client-specific certificates and credentials
        credentials_context = config["credentials_context"]

        return {
            "success": True,
            "login_time": "2024-01-01T10:00:00Z",
            "credentials_used": credentials_context,
            "session_token": f"esocial_token_{client_info['id']}",
        }

    async def _process_esocial_events(
        self, client_info: Dict[str, Any], task_type: str
    ) -> Dict[str, Any]:
        """Simulate eSocial event processing"""
        logger.info(f"📤 Processing eSocial events for {client_info['name']}")

        # Simulate event processing delay
        await asyncio.sleep(2)

        # Different processing based on task type
        if task_type == "send_events":
            events_count = 15
            events_sent = 15
            events_confirmed = 14
            warnings = ["Event S-1200 partially processed"]
        elif task_type == "query_status":
            events_count = 5
            events_sent = 0
            events_confirmed = 5
            warnings = []
        else:
            events_count = 10
            events_sent = 10
            events_confirmed = 10
            warnings = []

        return {
            "events_count": events_count,
            "events_sent": events_sent,
            "events_confirmed": events_confirmed,
            "processing_time": "00:02:15",
            "warnings": warnings,
        }


async def main():
    """Main function to demonstrate the enhanced eSocial robot"""
    robot = eSocialRobotEnhanced()

    print("🚀 AUDITORIA360 - Enhanced eSocial Robot")
    print("=" * 50)

    # Test with different clients
    test_clients = [1, 2]

    for client_id in test_clients:
        print(f"\n🎯 Testing with Client ID: {client_id}")
        print("-" * 30)

        try:
            result = await robot.execute_esocial_automation(client_id, "send_events")

            print(f"✅ Automation Result:")
            print(f"   Client: {result['client']}")
            print(f"   Events Processed: {result['events_processed']}")
            print(f"   Processing Time: {result['processing_time']}")
            print(f"   Session: {result['context_session']}")
            print(f"   Events Sent: {result['automation_details']['events_sent']}")
            print(
                f"   Events Confirmed: {result['automation_details']['events_confirmed']}"
            )

            if result["automation_details"]["warnings"]:
                print(
                    f"   ⚠️  Warnings: {', '.join(result['automation_details']['warnings'])}"
                )

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n🎉 Enhanced eSocial automation demonstration completed!")
    print(
        "This shows how automation scripts now work with real client context from the core system."
    )


if __name__ == "__main__":
    asyncio.run(main())
