"""
RPA Automation for Payroll Processing - Serverless Implementation
Migrated from traditional RPA to serverless GitHub Actions compatible version
"""
import asyncio
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PayrollRPAServerless:
    """Serverless RPA for payroll processing automation"""
    
    def __init__(self):
        self.api_base_url = os.getenv("API_BASE_URL", "https://auditoria360.vercel.app/api")
        self.auth_token = os.getenv("API_AUTH_TOKEN")
        self.environment = os.getenv("ENVIRONMENT", "production")
        
    async def authenticate(self) -> str:
        """Authenticate with the API and get access token"""
        if self.auth_token:
            return self.auth_token
            
        # Fallback authentication if needed
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_base_url}/v1/auth/token",
                    json={
                        "username": os.getenv("API_USERNAME"),
                        "password": os.getenv("API_PASSWORD")
                    }
                )
                response.raise_for_status()
                return response.json()["access_token"]
            except Exception as e:
                logger.error(f"Authentication failed: {e}")
                raise
    
    async def process_pending_payrolls(self) -> Dict:
        """Process all pending payroll items"""
        token = await self.authenticate()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                # Get pending payroll items
                response = await client.get(
                    f"{self.api_base_url}/v1/payroll/pending",
                    headers=headers
                )
                response.raise_for_status()
                pending_items = response.json()
                
                results = {
                    "processed": 0,
                    "failed": 0,
                    "errors": [],
                    "timestamp": datetime.now().isoformat()
                }
                
                for item in pending_items:
                    try:
                        await self._process_single_payroll(client, headers, item)
                        results["processed"] += 1
                        logger.info(f"Processed payroll item: {item.get('id')}")
                    except Exception as e:
                        results["failed"] += 1
                        results["errors"].append({
                            "item_id": item.get("id"),
                            "error": str(e)
                        })
                        logger.error(f"Failed to process payroll item {item.get('id')}: {e}")
                
                return results
                
            except Exception as e:
                logger.error(f"Failed to get pending payrolls: {e}")
                raise
    
    async def _process_single_payroll(self, client: httpx.AsyncClient, headers: Dict, item: Dict):
        """Process a single payroll item"""
        item_id = item.get("id")
        
        # Update status to processing
        await client.patch(
            f"{self.api_base_url}/v1/payroll/{item_id}/status",
            headers=headers,
            json={"status": "processing"}
        )
        
        # Perform payroll calculations
        calculations = await self._calculate_payroll(item)
        
        # Update with results
        response = await client.patch(
            f"{self.api_base_url}/v1/payroll/{item_id}",
            headers=headers,
            json={
                "calculations": calculations,
                "status": "completed",
                "processed_at": datetime.now().isoformat()
            }
        )
        response.raise_for_status()
    
    async def _calculate_payroll(self, item: Dict) -> Dict:
        """Perform payroll calculations"""
        # Simulate payroll calculation logic
        base_salary = item.get("base_salary", 0)
        overtime_hours = item.get("overtime_hours", 0)
        deductions = item.get("deductions", 0)
        
        overtime_pay = overtime_hours * (base_salary / 220 * 1.5)  # 50% overtime
        gross_pay = base_salary + overtime_pay
        net_pay = gross_pay - deductions
        
        return {
            "base_salary": base_salary,
            "overtime_pay": overtime_pay,
            "gross_pay": gross_pay,
            "deductions": deductions,
            "net_pay": net_pay,
            "calculation_date": datetime.now().isoformat()
        }
    
    async def generate_payroll_reports(self) -> Dict:
        """Generate automated payroll reports"""
        token = await self.authenticate()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                # Get completed payrolls from last 30 days
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                
                response = await client.get(
                    f"{self.api_base_url}/v1/payroll/completed",
                    headers=headers,
                    params={
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                )
                response.raise_for_status()
                payrolls = response.json()
                
                # Generate summary report
                report = {
                    "period": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "summary": {
                        "total_payrolls": len(payrolls),
                        "total_gross_pay": sum(p.get("calculations", {}).get("gross_pay", 0) for p in payrolls),
                        "total_net_pay": sum(p.get("calculations", {}).get("net_pay", 0) for p in payrolls),
                        "total_deductions": sum(p.get("calculations", {}).get("deductions", 0) for p in payrolls),
                    },
                    "generated_at": datetime.now().isoformat()
                }
                
                # Save report
                await client.post(
                    f"{self.api_base_url}/v1/reports/payroll",
                    headers=headers,
                    json=report
                )
                
                logger.info(f"Generated payroll report for {len(payrolls)} records")
                return report
                
            except Exception as e:
                logger.error(f"Failed to generate payroll reports: {e}")
                raise

async def run_payroll_automation():
    """Main entry point for payroll automation"""
    logger.info("Starting serverless payroll automation...")
    
    try:
        rpa = PayrollRPAServerless()
        
        # Process pending payrolls
        processing_results = await rpa.process_pending_payrolls()
        logger.info(f"Payroll processing results: {processing_results}")
        
        # Generate reports
        report_results = await rpa.generate_payroll_reports()
        logger.info(f"Report generation completed")
        
        # Output results for GitHub Actions
        if os.getenv("GITHUB_ACTIONS"):
            results = {
                "success": True,
                "processing": processing_results,
                "reports": report_results
            }
            print(f"::set-output name=results::{json.dumps(results)}")
        
        return {
            "status": "success",
            "processing": processing_results,
            "reports": report_results
        }
        
    except Exception as e:
        logger.error(f"Payroll automation failed: {e}")
        
        if os.getenv("GITHUB_ACTIONS"):
            error_result = {"success": False, "error": str(e)}
            print(f"::set-output name=results::{json.dumps(error_result)}")
            print(f"::error::Payroll automation failed: {e}")
        
        raise

if __name__ == "__main__":
    asyncio.run(run_payroll_automation())