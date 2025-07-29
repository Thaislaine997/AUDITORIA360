"""
AUDITORIA360 - Centralized Reporting Service
First Stage Implementation: Unified reporting system with graphical structure

This module provides:
- UnifiedReportGenerator: Main class for generating reports
- ReportData, ReportMetrics: Data structures for reports
- ReportType, ReportFormat: Enums for configuration
- Sample report generation functions

Usage:
    from services.reporting import UnifiedReportGenerator, ReportType, ReportFormat
    
    generator = UnifiedReportGenerator()
    report = generator.generate_unified_report(
        ReportType.MONTHLY,
        include_charts=True,
        format_output=ReportFormat.JSON
    )
"""

from .unified_reports import (
    UnifiedReportGenerator,
    ReportData,
    ReportMetrics,
    ReportType,
    ReportFormat,
    generate_sample_reports
)

__version__ = "1.0.0"
__author__ = "AUDITORIA360 Team"

__all__ = [
    "UnifiedReportGenerator",
    "ReportData", 
    "ReportMetrics",
    "ReportType",
    "ReportFormat",
    "generate_sample_reports"
]