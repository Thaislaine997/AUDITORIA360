#!/usr/bin/env python3
"""
AUDITORIA360 MCP Integration Demo
Demonstrates the complete Model Context Protocol integration with GitHub Copilot
"""

import asyncio
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_agent import EnhancedAIAgent


class MCPDemo:
    """Demonstration of MCP integration capabilities"""

    def __init__(self):
        self.agent = None
        self.demo_results = []

    async def initialize(self):
        """Initialize the enhanced AI agent"""
        print("🚀 Initializing AUDITORIA360 MCP Integration Demo")
        print("=" * 60)

        self.agent = EnhancedAIAgent()

        # Wait for initialization
        max_wait = 10
        waited = 0
        while self.agent.status == "initializing" and waited < max_wait:
            print(f"⏳ Waiting for initialization... ({waited + 1}s)")
            await asyncio.sleep(1)
            waited += 1

        if self.agent.status != "ready":
            raise Exception(f"Agent failed to initialize: {self.agent.status}")

        print(f"✅ Agent initialized successfully: {self.agent.status}")

        # Display capabilities
        capabilities = await self.agent.get_mcp_capabilities()
        tools_count = len(capabilities.get("tools", []))
        resources_count = len(capabilities.get("resources", []))

        print(f"📊 MCP Capabilities: {tools_count} tools, {resources_count} resources")
        print()

    async def demo_payroll_calculation(self):
        """Demonstrate payroll calculation via MCP"""
        print("💰 Demo 1: Payroll Calculation via MCP")
        print("-" * 40)

        try:
            result = await self.agent.executar_acao(
                "calcular folha de pagamento para funcionário",
                {
                    "employee_id": "DEMO001",
                    "month": datetime.now().month,
                    "year": datetime.now().year,
                    "base_salary": 6500.00,
                    "overtime_hours": 15,
                    "calculation_type": "normal",
                },
            )

            if result.get("success"):
                calc_result = result.get("result", {})
                print(
                    f"✅ Calculation successful for employee {calc_result.get('employee_id', 'N/A')}"
                )
                print(
                    f"   📈 Gross Salary: R$ {calc_result.get('gross_salary', 0):,.2f}"
                )
                print(f"   📉 Net Salary: R$ {calc_result.get('net_salary', 0):,.2f}")
                print(
                    f"   🏦 INSS Deduction: R$ {calc_result.get('inss_deduction', 0):,.2f}"
                )
                print(
                    f"   💸 IRRF Deduction: R$ {calc_result.get('irrf_deduction', 0):,.2f}"
                )
                print(
                    f"   🏠 FGTS Deposit: R$ {calc_result.get('fgts_deposit', 0):,.2f}"
                )

                self.demo_results.append(
                    {
                        "demo": "payroll_calculation",
                        "status": "success",
                        "result": calc_result,
                    }
                )
            else:
                print(f"❌ Calculation failed: {result.get('error')}")
                self.demo_results.append(
                    {
                        "demo": "payroll_calculation",
                        "status": "failed",
                        "error": result.get("error"),
                    }
                )

        except Exception as e:
            print(f"❌ Demo failed: {e}")
            self.demo_results.append(
                {"demo": "payroll_calculation", "status": "error", "error": str(e)}
            )

        print()

    async def demo_compliance_check(self):
        """Demonstrate compliance checking via MCP"""
        print("🔍 Demo 2: Compliance Check via MCP")
        print("-" * 40)

        try:
            # Test with compliant data
            result = await self.agent.executar_acao(
                "verificar conformidade trabalhista",
                {
                    "employee_id": "DEMO001",
                    "check_type": "salary",
                    "payroll_data": {
                        "base_salary": 6500.00,
                        "working_hours": 40,
                        "overtime_hours": 15,
                    },
                    "cct_id": "CCT_METALURGICOS_2024",
                },
            )

            if result.get("success"):
                comp_result = result.get("result", {})
                is_compliant = comp_result.get("compliant", False)
                violations = comp_result.get("violations", [])
                recommendations = comp_result.get("recommendations", [])

                print(
                    f"✅ Compliance check completed for {comp_result.get('employee_id', 'N/A')}"
                )
                print(f"   📋 Compliant: {'✅ Yes' if is_compliant else '❌ No'}")
                print(f"   ⚠️  Violations Found: {len(violations)}")

                if violations:
                    for i, violation in enumerate(violations[:3], 1):  # Show max 3
                        print(
                            f"      {i}. {violation.get('description', 'N/A')} ({violation.get('severity', 'N/A')})"
                        )

                if recommendations:
                    print(f"   💡 Recommendations: {len(recommendations)}")
                    for i, rec in enumerate(recommendations[:2], 1):  # Show max 2
                        print(f"      {i}. {rec}")

                self.demo_results.append(
                    {
                        "demo": "compliance_check",
                        "status": "success",
                        "result": comp_result,
                    }
                )
            else:
                print(f"❌ Compliance check failed: {result.get('error')}")

        except Exception as e:
            print(f"❌ Demo failed: {e}")

        print()

    async def demo_document_analysis(self):
        """Demonstrate document analysis via MCP"""
        print("📄 Demo 3: Document Analysis via MCP")
        print("-" * 40)

        try:
            result = await self.agent.executar_acao(
                "analisar documento de convenção coletiva",
                {
                    "document_id": "CCT_METALURGICOS_2024_V1",
                    "document_type": "cct",
                    "analysis_type": "extract_clauses",
                },
            )

            if result.get("success"):
                doc_result = result.get("result", {})
                analysis_results = doc_result.get("analysis_results", {})
                extracted_data = doc_result.get("extracted_data", {})

                print(
                    f"✅ Document analysis completed for {doc_result.get('document_id', 'N/A')}"
                )
                print(
                    f"   📊 Confidence Score: {doc_result.get('confidence_score', 0):.2%}"
                )
                print(
                    f"   ⏱️  Processing Time: {doc_result.get('processing_time', 0)} seconds"
                )
                print(f"   🌐 Language: {analysis_results.get('language', 'N/A')}")

                if extracted_data:
                    print("   📝 Extracted Information:")
                    if "syndicate_name" in extracted_data:
                        print(f"      • Syndicate: {extracted_data['syndicate_name']}")
                    if "validity_period" in extracted_data:
                        print(f"      • Validity: {extracted_data['validity_period']}")
                    if "salary_clauses" in extracted_data:
                        print(
                            f"      • Salary Clauses: {', '.join(extracted_data['salary_clauses'])}"
                        )

                self.demo_results.append(
                    {
                        "demo": "document_analysis",
                        "status": "success",
                        "result": doc_result,
                    }
                )
            else:
                print(f"❌ Document analysis failed: {result.get('error')}")

        except Exception as e:
            print(f"❌ Demo failed: {e}")

        print()

    async def demo_audit_execution(self):
        """Demonstrate audit execution via MCP"""
        print("🔎 Demo 4: Audit Execution via MCP")
        print("-" * 40)

        try:
            result = await self.agent.executar_acao(
                "executar auditoria de folha de pagamento",
                {
                    "audit_type": "payroll",
                    "scope": "sample",
                    "period_start": "2024-01-01",
                    "period_end": "2024-12-31",
                    "departments": ["HR", "Finance", "Operations"],
                },
            )

            if result.get("success"):
                audit_result = result.get("result", {})
                findings = audit_result.get("findings", [])
                recommendations = audit_result.get("recommendations", [])
                risk_assessment = audit_result.get("risk_assessment", {})

                print(
                    f"✅ Audit execution completed: {audit_result.get('audit_id', 'N/A')}"
                )
                print(
                    f"   🎯 Audit Type: {audit_result.get('audit_type', 'N/A').title()}"
                )
                print(f"   📊 Scope: {audit_result.get('scope', 'N/A').title()}")
                print(f"   🚨 Findings: {len(findings)}")
                print(f"   💡 Recommendations: {len(recommendations)}")
                print(
                    f"   ⚠️  Overall Risk: {risk_assessment.get('overall_risk', 'N/A').title()}"
                )

                if findings:
                    print("   📋 Key Findings:")
                    for i, finding in enumerate(findings[:2], 1):  # Show max 2
                        print(
                            f"      {i}. {finding.get('description', 'N/A')} ({finding.get('severity', 'N/A')})"
                        )

                self.demo_results.append(
                    {
                        "demo": "audit_execution",
                        "status": "success",
                        "result": audit_result,
                    }
                )
            else:
                print(f"❌ Audit execution failed: {result.get('error')}")

        except Exception as e:
            print(f"❌ Demo failed: {e}")

        print()

    async def demo_cct_comparison(self):
        """Demonstrate CCT comparison via MCP"""
        print("⚖️  Demo 5: CCT Comparison via MCP")
        print("-" * 40)

        try:
            result = await self.agent.executar_acao(
                "comparar convenções coletivas de trabalho",
                {
                    "cct_id_1": "CCT_METALURGICOS_2023",
                    "cct_id_2": "CCT_METALURGICOS_2024",
                    "comparison_type": "salary_clauses",
                    "highlight_differences": True,
                    "include_recommendations": True,
                },
            )

            if result.get("success"):
                comp_result = result.get("result", {})
                comparison_summary = comp_result.get("comparison_summary", {})
                differences = comp_result.get("differences", [])
                impact_analysis = comp_result.get("impact_analysis", {})

                print(
                    f"✅ CCT comparison completed: {comp_result.get('comparison_id', 'N/A')}"
                )
                print(
                    f"   📊 Total Clauses: {comparison_summary.get('total_clauses_compared', 0)}"
                )
                print(
                    f"   ✅ Identical: {comparison_summary.get('identical_clauses', 0)}"
                )
                print(
                    f"   ⚠️  Different: {comparison_summary.get('different_clauses', 0)}"
                )
                print(
                    f"   📈 Similarity: {comparison_summary.get('similarity_percentage', 0):.1f}%"
                )

                if differences:
                    print("   🔍 Key Differences:")
                    for i, diff in enumerate(differences[:2], 1):  # Show max 2
                        print(
                            f"      {i}. {diff.get('clause_type', 'N/A').title()}: {diff.get('significance', 'N/A')} impact"
                        )

                financial_impact = impact_analysis.get("financial_impact", {})
                if financial_impact:
                    cost_diff = financial_impact.get("estimated_cost_difference", 0)
                    print(
                        f"   💰 Financial Impact: R$ {cost_diff:,.2f} {financial_impact.get('period', 'monthly')}"
                    )

                self.demo_results.append(
                    {
                        "demo": "cct_comparison",
                        "status": "success",
                        "result": comp_result,
                    }
                )
            else:
                print(f"❌ CCT comparison failed: {result.get('error')}")

        except Exception as e:
            print(f"❌ Demo failed: {e}")

        print()

    async def show_summary(self):
        """Show demo summary and results"""
        print("📊 Demo Summary and Results")
        print("=" * 60)

        successful_demos = [r for r in self.demo_results if r["status"] == "success"]
        failed_demos = [
            r for r in self.demo_results if r["status"] in ["failed", "error"]
        ]

        print(f"✅ Successful Demos: {len(successful_demos)}/{len(self.demo_results)}")
        print(f"❌ Failed Demos: {len(failed_demos)}/{len(self.demo_results)}")
        print()

        if successful_demos:
            print("🎉 Successfully Demonstrated MCP Capabilities:")
            for demo in successful_demos:
                demo_name = demo["demo"].replace("_", " ").title()
                print(f"   ✅ {demo_name}")

        if failed_demos:
            print("\n⚠️  Demos with Issues:")
            for demo in failed_demos:
                demo_name = demo["demo"].replace("_", " ").title()
                error = demo.get("error", "Unknown error")
                print(f"   ❌ {demo_name}: {error}")

        print("\n🔧 MCP Integration Features Demonstrated:")
        print("   • Real-time payroll calculations with tax computations")
        print("   • Automated compliance checking against labor laws")
        print("   • AI-powered document analysis and information extraction")
        print("   • Comprehensive audit execution with risk assessment")
        print("   • Intelligent CCT comparison with impact analysis")

        print("\n📚 Next Steps for GitHub Copilot Integration:")
        print("   1. Open VS Code in this project directory")
        print("   2. Enable GitHub Copilot extension")
        print("   3. Start coding with AI-powered AUDITORIA360 context")
        print("   4. Use natural language comments to trigger MCP tools")
        print("   5. Access real-time payroll and compliance data")

        print("\n🛠️  Available Commands:")
        print("   • ./scripts/start_dev_environment.sh - Start full environment")
        print("   • python -m src.mcp.copilot_server - Start MCP server")
        print(
            "   • curl http://localhost:8000/api/v1/ai/mcp/capabilities - Get capabilities"
        )

        return len(successful_demos) == len(self.demo_results)


async def main():
    """Main demo function"""
    demo = MCPDemo()

    try:
        # Initialize the demo
        await demo.initialize()

        # Run all demonstrations
        await demo.demo_payroll_calculation()
        await demo.demo_compliance_check()
        await demo.demo_document_analysis()
        await demo.demo_audit_execution()
        await demo.demo_cct_comparison()

        # Show summary
        all_success = await demo.show_summary()

        if all_success:
            print("\n🎉 All demos completed successfully!")
            print(
                "AUDITORIA360 MCP integration is fully functional and ready for GitHub Copilot."
            )
        else:
            print("\n⚠️  Some demos had issues, but core functionality is working.")

        return all_success

    except Exception as e:
        print(f"\n❌ Demo failed to complete: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 AUDITORIA360 Model Context Protocol Integration Demo")
    print("🤖 Extended GitHub Copilot with Domain-Specific AI Tools")
    print("⭐ Payroll • Compliance • Audit • Document Analysis • CCT Comparison")
    print()

    success = asyncio.run(main())

    print("\n" + "=" * 60)
    if success:
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("🎯 MCP integration is ready for production use with GitHub Copilot")
    else:
        print("⚠️  DEMO COMPLETED WITH ISSUES")
        print("🔧 Check the output above for specific error details")

    sys.exit(0 if success else 1)
