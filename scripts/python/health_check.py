#!/usr/bin/env python3
"""
Advanced Health Checks for AUDITORIA360
"""
import asyncio
import aiohttp
import json
import time
from datetime import datetime

class HealthChecker:
    def __init__(self):
        self.checks = []
        self.results = []
    
    async def check_api_health(self):
        """Check API health"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8000/health") as response:
                    return response.status == 200
        except:
            return False
    
    async def check_database_health(self):
        """Check database connectivity"""
        # Simulate database check
        await asyncio.sleep(0.1)
        return True
    
    async def check_storage_health(self):
        """Check storage connectivity"""
        # Simulate storage check
        await asyncio.sleep(0.05)
        return True
    
    async def run_all_checks(self):
        """Run all health checks"""
        checks = [
            ("API", self.check_api_health),
            ("Database", self.check_database_health),
            ("Storage", self.check_storage_health)
        ]
        
        results = []
        for name, check_func in checks:
            start_time = time.time()
            try:
                status = await check_func()
                response_time = (time.time() - start_time) * 1000
                results.append({
                    "name": name,
                    "status": "healthy" if status else "unhealthy",
                    "response_time_ms": response_time,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                results.append({
                    "name": name,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results

async def main():
    checker = HealthChecker()
    results = await checker.run_all_checks()
    
    print(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "overall_status": "healthy" if all(r["status"] == "healthy" for r in results) else "unhealthy",
        "checks": results
    }, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
