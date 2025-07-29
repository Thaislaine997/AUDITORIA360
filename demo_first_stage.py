#!/usr/bin/env python3
"""
AUDITORIA360 - First Stage Integration Example
Demonstrates the unified reporting system with dashboard integration

This script shows how the first stage components work together:
1. Generate unified reports
2. Display dashboard with graphics
3. Export results in multiple formats
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import logging

    from services.reporting import ReportFormat, ReportType, UnifiedReportGenerator

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def demo_first_stage():
        """Demonstrate first stage implementation"""
        print("🚀 AUDITORIA360 - First Stage Implementation Demo")
        print("=" * 60)

        # Initialize report generator
        generator = UnifiedReportGenerator(output_dir="./demo_reports")

        print("\n📊 1. Generating Unified Reports...")

        # Generate different types of reports
        reports = []

        # Daily report
        print("   📅 Generating daily report...")
        daily_report = generator.generate_unified_report(
            ReportType.DAILY, include_charts=True, format_output=ReportFormat.JSON
        )
        reports.append(daily_report)

        # Weekly report
        print("   📆 Generating weekly report...")
        weekly_report = generator.generate_unified_report(
            ReportType.WEEKLY, include_charts=True, format_output=ReportFormat.JSON
        )
        reports.append(weekly_report)

        # Monthly report
        print("   📊 Generating monthly report...")
        monthly_report = generator.generate_unified_report(
            ReportType.MONTHLY, include_charts=True, format_output=ReportFormat.JSON
        )
        reports.append(monthly_report)

        print(f"\n✅ Generated {len(reports)} reports successfully!")

        # Display report summary
        print("\n📋 2. Report Summary:")
        print("-" * 40)

        for report in reports:
            print(f"   📊 {report.title}")
            print(f"      ID: {report.id}")
            print(
                f"      Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}"
            )
            print(
                f"      Metrics: {report.metrics.total_audits} audits, {report.metrics.compliance_score}% compliance"
            )
            print(f"      Charts: {len(report.charts_data)} visualizations")
            print(f"      Recommendations: {len(report.recommendations)} items")
            print()

        # Show chart data structure
        print("📈 3. Chart Data Structure Example:")
        print("-" * 40)

        sample_report = reports[0]  # Use daily report
        for chart_name, chart_data in sample_report.charts_data.items():
            print(f"   📊 {chart_name}:")
            print(f"      Type: {chart_data['config']['type']}")
            print(f"      Title: {chart_data['config']['title']}")
            if "data" in chart_data and "labels" in chart_data["data"]:
                print(f"      Data points: {len(chart_data['data']['labels'])}")
            print()

        # Show recommendations
        print("💡 4. Sample Recommendations:")
        print("-" * 40)

        for i, rec in enumerate(sample_report.recommendations[:3], 1):
            print(f"   {i}. {rec['title']} ({rec['priority']} priority)")
            print(f"      Category: {rec['category']}")
            print(f"      Description: {rec['description']}")
            print()

        print("🎯 5. First Stage Benefits Achieved:")
        print("-" * 40)
        print("   ✅ Centralized documentation structure (docs/documentos/)")
        print("   ✅ Unified reporting system with graphics")
        print("   ✅ Enhanced dashboard with interactive charts")
        print("   ✅ Modular architecture for future PRs")
        print("   ✅ Performance-optimized data structures")
        print("   ✅ Standardized report formats and APIs")
        print()

        print("🚀 6. Next PR Preparation:")
        print("-" * 40)
        print("   📝 PR #2: Complete database integration")
        print("   📈 PR #3: Advanced dashboard analytics")
        print("   ⚡ PR #4: Performance optimization & caching")
        print("   🤖 PR #5: ML/AI integration")
        print()

        print("✨ First Stage Implementation: COMPLETED")
        print("=" * 60)

        return reports

    def show_file_structure():
        """Show the file structure created in first stage"""
        print("\n📁 First Stage File Structure:")
        print("-" * 40)

        structure = {
            "docs/documentos/": [
                "README.md (Documentation index)",
                "relatorios/relatorio-unificado.md",
                "relatorios/status-implementacao.md",
                "arquitetura/visao-geral.md",
                "apis/api-documentation.md",
                "manuais/ (prepared)",
                "compliance/ (prepared)",
                "instalacao/ (prepared)",
                "templates/ (prepared)",
            ],
            "services/reporting/": [
                "__init__.py (Package definition)",
                "unified_reports.py (Main implementation)",
            ],
            "dashboards/": ["enhanced_dashboard.py (Improved Streamlit app)"],
        }

        for folder, files in structure.items():
            print(f"   📂 {folder}")
            for file in files:
                print(f"      📄 {file}")
            print()

    if __name__ == "__main__":
        try:
            # Run the demo
            reports = demo_first_stage()

            # Show file structure
            show_file_structure()

            print("🎉 Demo completed successfully!")
            print("\nTo run the enhanced dashboard:")
            print("   streamlit run dashboards/enhanced_dashboard.py")
            print("\nTo generate reports programmatically:")
            print("   python services/reporting/unified_reports.py")

        except Exception as e:
            logger.error(f"Demo failed: {e}")
            print(f"❌ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure you're in the project root directory")
            print("2. Check that all dependencies are installed")
            print("3. Verify file permissions")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\n🔧 Setup Instructions:")
    print("1. Make sure you're in the AUDITORIA360 project root")
    print("2. Install required dependencies:")
    print("   pip install streamlit plotly pandas")
    print("3. Run this demo again")
