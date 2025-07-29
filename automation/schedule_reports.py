"""
Scheduled Reports Automation - Serverless Implementation
Compatible with Vercel Cron Jobs and GitHub Actions
"""
import asyncio
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import httpx
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScheduledReportsServerless:
    """Serverless scheduled reports automation"""
    
    def __init__(self):
        self.api_base_url = os.getenv("API_BASE_URL", "https://auditoria360.vercel.app/api")
        self.auth_token = os.getenv("API_AUTH_TOKEN")
        self.environment = os.getenv("ENVIRONMENT", "production")
        self.output_dir = Path(os.getenv("REPORTS_OUTPUT_DIR", "/tmp/reports"))
        self.output_dir.mkdir(exist_ok=True)
        
    async def authenticate(self) -> str:
        """Authenticate with the API"""
        if self.auth_token:
            return self.auth_token
            
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
    
    async def generate_daily_report(self) -> Dict:
        """Generate daily audit report"""
        token = await self.authenticate()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                today = datetime.now().date()
                yesterday = today - timedelta(days=1)
                
                # Get audit data from yesterday
                response = await client.get(
                    f"{self.api_base_url}/v1/audits/summary",
                    headers=headers,
                    params={
                        "date": yesterday.isoformat()
                    }
                )
                response.raise_for_status()
                audit_data = response.json()
                
                # Get compliance data
                response = await client.get(
                    f"{self.api_base_url}/v1/compliance/daily",
                    headers=headers,
                    params={
                        "date": yesterday.isoformat()
                    }
                )
                response.raise_for_status()
                compliance_data = response.json()
                
                # Generate report
                report = {
                    "type": "daily_report",
                    "date": yesterday.isoformat(),
                    "generated_at": datetime.now().isoformat(),
                    "summary": {
                        "total_audits": audit_data.get("total_audits", 0),
                        "completed_audits": audit_data.get("completed_audits", 0),
                        "pending_audits": audit_data.get("pending_audits", 0),
                        "compliance_score": compliance_data.get("compliance_score", 0),
                        "critical_issues": compliance_data.get("critical_issues", 0),
                        "resolved_issues": compliance_data.get("resolved_issues", 0)
                    },
                    "details": {
                        "audits": audit_data.get("details", []),
                        "compliance": compliance_data.get("details", [])
                    }
                }
                
                # Save report locally
                report_file = self.output_dir / f"daily_report_{yesterday.isoformat()}.json"
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                
                # Send report to API
                await client.post(
                    f"{self.api_base_url}/v1/reports/daily",
                    headers=headers,
                    json=report
                )
                
                logger.info(f"Generated daily report for {yesterday}")
                return report
                
            except Exception as e:
                logger.error(f"Failed to generate daily report: {e}")
                raise
    
    async def generate_weekly_report(self) -> Dict:
        """Generate weekly compliance report"""
        token = await self.authenticate()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=7)
                
                # Get weekly audit summary
                response = await client.get(
                    f"{self.api_base_url}/v1/audits/summary",
                    headers=headers,
                    params={
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                )
                response.raise_for_status()
                audit_summary = response.json()
                
                # Get compliance trends
                response = await client.get(
                    f"{self.api_base_url}/v1/compliance/trends",
                    headers=headers,
                    params={
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat()
                    }
                )
                response.raise_for_status()
                compliance_trends = response.json()
                
                # Get risk analysis
                response = await client.get(
                    f"{self.api_base_url}/v1/risks/analysis",
                    headers=headers,
                    params={
                        "period": "weekly"
                    }
                )
                response.raise_for_status()
                risk_analysis = response.json()
                
                # Generate weekly report
                report = {
                    "type": "weekly_report",
                    "period": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "generated_at": datetime.now().isoformat(),
                    "summary": {
                        "total_audits": audit_summary.get("total_audits", 0),
                        "completion_rate": audit_summary.get("completion_rate", 0),
                        "avg_compliance_score": compliance_trends.get("average_score", 0),
                        "compliance_improvement": compliance_trends.get("improvement", 0),
                        "high_risk_items": risk_analysis.get("high_risk_count", 0),
                        "risk_score": risk_analysis.get("overall_score", 0)
                    },
                    "trends": compliance_trends,
                    "risks": risk_analysis,
                    "recommendations": self._generate_recommendations(audit_summary, compliance_trends, risk_analysis)
                }
                
                # Save report locally
                report_file = self.output_dir / f"weekly_report_{start_date}_to_{end_date}.json"
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                
                # Send report to API
                await client.post(
                    f"{self.api_base_url}/v1/reports/weekly",
                    headers=headers,
                    json=report
                )
                
                logger.info(f"Generated weekly report for {start_date} to {end_date}")
                return report
                
            except Exception as e:
                logger.error(f"Failed to generate weekly report: {e}")
                raise
    
    async def generate_monthly_report(self) -> Dict:
        """Generate monthly comprehensive report"""
        token = await self.authenticate()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                end_date = datetime.now().date()
                start_date = end_date.replace(day=1)  # First day of current month
                
                # Get comprehensive monthly data
                tasks = [
                    client.get(f"{self.api_base_url}/v1/audits/monthly", headers=headers, params={"month": start_date.strftime("%Y-%m")}),
                    client.get(f"{self.api_base_url}/v1/compliance/monthly", headers=headers, params={"month": start_date.strftime("%Y-%m")}),
                    client.get(f"{self.api_base_url}/v1/payroll/monthly", headers=headers, params={"month": start_date.strftime("%Y-%m")}),
                    client.get(f"{self.api_base_url}/v1/risks/monthly", headers=headers, params={"month": start_date.strftime("%Y-%m")})
                ]
                
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    response.raise_for_status()
                
                audit_data, compliance_data, payroll_data, risk_data = [r.json() for r in responses]
                
                # Generate comprehensive monthly report
                report = {
                    "type": "monthly_report",
                    "month": start_date.strftime("%Y-%m"),
                    "generated_at": datetime.now().isoformat(),
                    "executive_summary": {
                        "total_audits": audit_data.get("total_audits", 0),
                        "audit_completion_rate": audit_data.get("completion_rate", 0),
                        "overall_compliance_score": compliance_data.get("overall_score", 0),
                        "payroll_accuracy": payroll_data.get("accuracy_rate", 0),
                        "risk_reduction": risk_data.get("risk_reduction", 0),
                        "cost_savings": payroll_data.get("cost_savings", 0)
                    },
                    "detailed_analysis": {
                        "audits": audit_data,
                        "compliance": compliance_data,
                        "payroll": payroll_data,
                        "risks": risk_data
                    },
                    "kpis": self._calculate_monthly_kpis(audit_data, compliance_data, payroll_data, risk_data),
                    "action_items": self._generate_action_items(audit_data, compliance_data, risk_data)
                }
                
                # Save report locally
                report_file = self.output_dir / f"monthly_report_{start_date.strftime('%Y-%m')}.json"
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                
                # Send report to API
                await client.post(
                    f"{self.api_base_url}/v1/reports/monthly",
                    headers=headers,
                    json=report
                )
                
                logger.info(f"Generated monthly report for {start_date.strftime('%Y-%m')}")
                return report
                
            except Exception as e:
                logger.error(f"Failed to generate monthly report: {e}")
                raise
    
    def _generate_recommendations(self, audit_summary: Dict, compliance_trends: Dict, risk_analysis: Dict) -> List[Dict]:
        """Generate recommendations based on data analysis"""
        recommendations = []
        
        if compliance_trends.get("improvement", 0) < 0:
            recommendations.append({
                "type": "compliance",
                "priority": "high",
                "recommendation": "Implement additional compliance training due to declining scores"
            })
        
        if risk_analysis.get("high_risk_count", 0) > 5:
            recommendations.append({
                "type": "risk",
                "priority": "critical",
                "recommendation": "Address high-risk items immediately to prevent compliance failures"
            })
        
        if audit_summary.get("completion_rate", 0) < 0.8:
            recommendations.append({
                "type": "process",
                "priority": "medium",
                "recommendation": "Optimize audit workflow to improve completion rates"
            })
        
        return recommendations
    
    def _calculate_monthly_kpis(self, audit_data: Dict, compliance_data: Dict, payroll_data: Dict, risk_data: Dict) -> Dict:
        """Calculate monthly KPIs"""
        return {
            "audit_efficiency": audit_data.get("completion_rate", 0) * 100,
            "compliance_score": compliance_data.get("overall_score", 0),
            "payroll_accuracy": payroll_data.get("accuracy_rate", 0) * 100,
            "risk_mitigation": (1 - risk_data.get("overall_score", 1)) * 100,
            "automation_rate": payroll_data.get("automation_rate", 0) * 100
        }
    
    def _generate_action_items(self, audit_data: Dict, compliance_data: Dict, risk_data: Dict) -> List[Dict]:
        """Generate action items for the next month"""
        action_items = []
        
        if audit_data.get("pending_audits", 0) > 10:
            action_items.append({
                "category": "audits",
                "priority": "high",
                "action": "Clear backlog of pending audits",
                "due_date": (datetime.now() + timedelta(days=7)).isoformat()
            })
        
        critical_compliance_issues = compliance_data.get("critical_issues", 0)
        if critical_compliance_issues > 0:
            action_items.append({
                "category": "compliance",
                "priority": "critical",
                "action": f"Resolve {critical_compliance_issues} critical compliance issues",
                "due_date": (datetime.now() + timedelta(days=3)).isoformat()
            })
        
        return action_items

async def run_scheduled_reports(report_type: str = "daily"):
    """Main entry point for scheduled reports"""
    logger.info(f"Starting {report_type} report generation...")
    
    try:
        scheduler = ScheduledReportsServerless()
        
        if report_type == "daily":
            result = await scheduler.generate_daily_report()
        elif report_type == "weekly":
            result = await scheduler.generate_weekly_report()
        elif report_type == "monthly":
            result = await scheduler.generate_monthly_report()
        else:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Output for GitHub Actions/Vercel
        if os.getenv("GITHUB_ACTIONS") or os.getenv("VERCEL"):
            success_result = {"success": True, "report": result}
            print(f"::set-output name=results::{json.dumps(success_result)}")
        
        logger.info(f"{report_type.title()} report generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"{report_type} report generation failed: {e}")
        
        if os.getenv("GITHUB_ACTIONS") or os.getenv("VERCEL"):
            error_result = {"success": False, "error": str(e)}
            print(f"::set-output name=results::{json.dumps(error_result)}")
            print(f"::error::{report_type} report generation failed: {e}")
        
        raise

if __name__ == "__main__":
    import sys
    report_type = sys.argv[1] if len(sys.argv) > 1 else "daily"
    asyncio.run(run_scheduled_reports(report_type))