#!/usr/bin/env python3
"""
Quick Checklist - AUDITORIA360
==============================

A simplified tool for quick validation of the master execution checklist.
Provides a fast overview without detailed reporting.

Usage:
    python scripts/quick_checklist.py
    python scripts/quick_checklist.py --verbose
    python scripts/quick_checklist.py --section PARTE_1_ALICERCE_E_GOVERNANCA
"""

import argparse
import os
import sys
from typing import Dict, Tuple

# Import the main checklist validator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from master_execution_checklist import MasterExecutionChecklist


class QuickChecklistValidator:
    """Quick validation tool for master execution checklist"""

    def __init__(self, project_root: str = None):
        self.checklist = MasterExecutionChecklist(project_root)

    def quick_check_section(self, section_name: str) -> Tuple[int, int, float]:
        """Quick check of a single section"""
        if section_name not in self.checklist.checklist_data:
            return 0, 0, 0.0

        files = self.checklist.checklist_data[section_name]
        valid_count = 0

        for file_path in files:
            full_path = self.checklist.project_root / file_path
            if full_path.exists():
                try:
                    # Basic validation - just check if file is readable
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        f.read(1)  # Read just one character to test
                    valid_count += 1
                except:
                    pass

        total_files = len(files)
        percentage = (valid_count / total_files * 100) if total_files > 0 else 0

        return valid_count, total_files, percentage

    def quick_check_all(self) -> Dict[str, Tuple[int, int, float]]:
        """Quick check of all sections"""
        results = {}

        for section_name in self.checklist.checklist_data:
            results[section_name] = self.quick_check_section(section_name)

        return results

    def print_summary(self, verbose: bool = False):
        """Print a quick summary"""
        print("🔍 AUDITORIA360 - Quick Checklist Validation")
        print("=" * 50)

        results = self.quick_check_all()

        total_valid = 0
        total_files = 0

        for section_name, (valid, total, percentage) in results.items():
            total_valid += valid
            total_files += total

            # Status icon
            if percentage == 100:
                icon = "✅"
            elif percentage >= 80:
                icon = "🟡"
            else:
                icon = "❌"

            # Section name formatting
            section_display = section_name.replace("_", " ").title()
            section_display = section_display.replace("Parte ", "Parte ")

            if verbose:
                print(f"{icon} {section_display}")
                print(f"   Progress: {percentage:.1f}% ({valid}/{total} files)")
                print()
            else:
                print(f"{icon} {section_display}: {percentage:.1f}% ({valid}/{total})")

        # Overall summary
        overall_percentage = (total_valid / total_files * 100) if total_files > 0 else 0

        print("\n" + "=" * 50)
        print(f"📊 OVERALL STATUS: {overall_percentage:.1f}%")
        print(f"   Total Valid Files: {total_valid}/{total_files}")

        # Status message
        if overall_percentage == 100:
            print("🎉 ALL SYSTEMS GO! Ready for merge.")
        elif overall_percentage >= 90:
            print("✨ Almost ready! Minor adjustments needed.")
        elif overall_percentage >= 80:
            print("⚠️  Good progress, but attention required.")
        else:
            print("🚨 Significant work needed before merge.")

        return overall_percentage


def main():
    parser = argparse.ArgumentParser(
        description="Quick validation of AUDITORIA360 master execution checklist"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument("--section", "-s", help="Check only specific section")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument(
        "--threshold",
        type=float,
        default=85.0,
        help="Minimum completion threshold (default: 85.0)",
    )

    args = parser.parse_args()

    # Initialize validator
    validator = QuickChecklistValidator(args.project_root)

    if args.section:
        # Check specific section only
        valid, total, percentage = validator.quick_check_section(args.section)

        section_display = args.section.replace("_", " ").title()

        if percentage == 100:
            icon = "✅"
        elif percentage >= 80:
            icon = "🟡"
        else:
            icon = "❌"

        print(f"{icon} {section_display}: {percentage:.1f}% ({valid}/{total} files)")

        if percentage < args.threshold:
            sys.exit(1)
    else:
        # Check all sections
        overall_percentage = validator.print_summary(args.verbose)

        # Exit with error code if below threshold
        if overall_percentage < args.threshold:
            print(
                f"\n❌ Completion ({overall_percentage:.1f}%) below threshold ({args.threshold}%)"
            )
            sys.exit(1)
        else:
            print(
                f"\n✅ Completion ({overall_percentage:.1f}%) meets threshold ({args.threshold}%)"
            )


if __name__ == "__main__":
    main()
