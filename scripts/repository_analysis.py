#!/usr/bin/env python3
"""
Comprehensive Repository Analysis Script for AUDITORIA360
Performs file-by-file validation, integrity checks, and improvement recommendations
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


class AuditoriaAnalyzer:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.issues = defaultdict(list)
        self.recommendations = defaultdict(list)
        self.file_stats = {}

    def analyze_repository(self):
        """Main analysis function"""
        print("🔍 Starting comprehensive repository analysis...")

        # File system analysis
        self.analyze_file_structure()
        self.find_obsolete_files()
        self.check_duplicate_files()

        # Code quality analysis
        self.analyze_python_files()
        self.analyze_config_files()
        self.analyze_documentation()

        # Security and best practices
        self.security_scan()
        self.check_best_practices()

        # Generate final report
        self.generate_report()

    def analyze_file_structure(self):
        """Analyze overall file structure and organization"""
        print("📁 Analyzing file structure...")

        # Count files by type
        file_types = Counter()
        total_size = 0

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                file_types[suffix] += 1
                total_size += file_path.stat().st_size

        self.file_stats = {
            "total_files": sum(file_types.values()),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_types": dict(file_types.most_common()),
        }

        print(
            f"   ✅ Found {self.file_stats['total_files']} files ({self.file_stats['total_size_mb']} MB)"
        )

    def find_obsolete_files(self):
        """Find potentially obsolete or unwanted files"""
        print("🧹 Checking for obsolete files...")

        obsolete_patterns = [
            "*.pyc",
            "**/__pycache__/**",
            "*.pyo",
            "*.pyd",
            ".DS_Store",
            "Thumbs.db",
            "*.tmp",
            "*.temp",
            "*.log",
            "*.bak",
            "*.swp",
            "*.swo",
            "node_modules/**",
            ".pytest_cache/**",
            "*.db",
            "*.sqlite",
            "*.sqlite3",  # Should not be in repo
        ]

        obsolete_files = []
        for pattern in obsolete_patterns:
            obsolete_files.extend(self.root_path.glob(pattern))

        if obsolete_files:
            self.issues["obsolete_files"] = [
                str(f.relative_to(self.root_path)) for f in obsolete_files
            ]
            print(f"   ⚠️  Found {len(obsolete_files)} potentially obsolete files")
        else:
            print("   ✅ No obsolete files found")

    def check_duplicate_files(self):
        """Check for potential duplicate files"""
        print("🔍 Checking for duplicate files...")

        # Simple name-based duplicate detection
        file_names = defaultdict(list)

        for file_path in self.root_path.rglob("*.py"):
            if not any(part.startswith(".") for part in file_path.parts):
                file_names[file_path.name].append(
                    str(file_path.relative_to(self.root_path))
                )

        duplicates = {
            name: paths for name, paths in file_names.items() if len(paths) > 1
        }

        if duplicates:
            self.issues["potential_duplicates"] = duplicates
            print(f"   ⚠️  Found {len(duplicates)} potential duplicate file names")
        else:
            print("   ✅ No obvious duplicate files found")

    def analyze_python_files(self):
        """Analyze Python files for issues"""
        print("🐍 Analyzing Python files...")

        python_files = list(self.root_path.rglob("*.py"))
        issues_found = 0

        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for common issues
                relative_path = str(py_file.relative_to(self.root_path))

                # Check imports
                if (
                    "from tensorflow import" in content
                    and "requirements-ml.txt" not in str(py_file)
                ):
                    self.issues["missing_ml_dependencies"].append(relative_path)

                # Check for hardcoded credentials
                if any(
                    keyword in content.lower()
                    for keyword in ["password =", "secret =", "api_key ="]
                ):
                    self.issues["potential_hardcoded_secrets"].append(relative_path)

                # Check for old Pydantic syntax
                if "@validator(" in content:
                    self.issues["deprecated_pydantic"].append(relative_path)

                # Check for TODO/FIXME
                if "TODO" in content or "FIXME" in content:
                    self.issues["todos_fixmes"].append(relative_path)

            except Exception as e:
                self.issues["file_read_errors"].append(f"{relative_path}: {str(e)}")
                issues_found += 1

        print(f"   ✅ Analyzed {len(python_files)} Python files")
        if issues_found:
            print(f"   ⚠️  Found issues in {issues_found} files")

    def analyze_config_files(self):
        """Analyze configuration files"""
        print("⚙️  Analyzing configuration files...")

        config_files = []
        config_files.extend(self.root_path.glob("*.json"))
        config_files.extend(self.root_path.glob("*.yaml"))
        config_files.extend(self.root_path.glob("*.yml"))
        config_files.extend(self.root_path.glob("*.toml"))
        config_files.extend(self.root_path.glob("*.env*"))

        for config_file in config_files:
            try:
                relative_path = str(config_file.relative_to(self.root_path))

                # Check if .env files contain actual secrets (shouldn't be in repo)
                if (
                    config_file.name.startswith(".env")
                    and config_file.name != ".env.template"
                ):
                    with open(config_file, "r") as f:
                        content = f.read()
                        if "=" in content and not all(
                            line.strip().startswith("#") or not line.strip()
                            for line in content.split("\n")
                        ):
                            self.issues["env_files_with_secrets"].append(relative_path)

            except Exception as e:
                self.issues["config_read_errors"].append(f"{relative_path}: {str(e)}")

        print(f"   ✅ Analyzed {len(config_files)} configuration files")

    def analyze_documentation(self):
        """Analyze documentation completeness"""
        print("📚 Analyzing documentation...")

        # Check for essential documentation files
        essential_docs = ["README.md", "docs/relatorios/CHANGELOG.md"]
        missing_docs = []

        for doc in essential_docs:
            if not (self.root_path / doc).exists():
                missing_docs.append(doc)

        if missing_docs:
            self.issues["missing_essential_docs"] = missing_docs

        # Check documentation structure
        docs_dir = self.root_path / "docs"
        if docs_dir.exists():
            md_files = list(docs_dir.rglob("*.md"))
            print(f"   ✅ Found {len(md_files)} documentation files")
        else:
            self.issues["missing_docs_directory"] = ["docs/ directory not found"]

    def security_scan(self):
        """Basic security scan"""
        print("🔒 Running security scan...")

        # Check .gitignore
        gitignore = self.root_path / ".gitignore"
        if gitignore.exists():
            with open(gitignore, "r") as f:
                gitignore_content = f.read()

            required_ignores = [".env", "*.db", "__pycache__", "*.pyc", "node_modules"]
            missing_ignores = [
                item for item in required_ignores if item not in gitignore_content
            ]

            if missing_ignores:
                self.issues["gitignore_missing_entries"] = missing_ignores
        else:
            self.issues["missing_gitignore"] = [".gitignore file not found"]

        print("   ✅ Security scan completed")

    def check_best_practices(self):
        """Check for best practices"""
        print("✨ Checking best practices...")

        # Check for proper requirements files
        req_files = ["requirements.txt", "requirements-dev.txt"]
        for req_file in req_files:
            if not (self.root_path / req_file).exists():
                self.recommendations["missing_requirements"].append(req_file)

        # Check for proper project structure
        expected_dirs = ["src", "tests", "docs"]
        for exp_dir in expected_dirs:
            if not (self.root_path / exp_dir).exists():
                self.recommendations["missing_directories"].append(exp_dir)

        print("   ✅ Best practices check completed")

    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE REPOSITORY ANALYSIS REPORT")
        print("=" * 80)

        print(f"\n📊 REPOSITORY STATISTICS:")
        print(f"   Total files: {self.file_stats['total_files']}")
        print(f"   Total size: {self.file_stats['total_size_mb']} MB")
        print(f"   File types: {len(self.file_stats['file_types'])}")

        print(f"\n🔍 ISSUES FOUND: {len(self.issues)}")
        for category, items in self.issues.items():
            print(f"\n   ⚠️  {category.upper().replace('_', ' ')}:")
            if isinstance(items, dict):
                for key, value in list(items.items())[:5]:  # Show first 5 items
                    print(f"      - {key}: {value}")
                if len(items) > 5:
                    print(f"      ... and {len(items) - 5} more")
            elif isinstance(items, list):
                for item in items[:5]:  # Show first 5 items
                    print(f"      - {item}")
                if len(items) > 5:
                    print(f"      ... and {len(items) - 5} more")
            else:
                print(f"      - {items}")

        print(f"\n💡 RECOMMENDATIONS: {len(self.recommendations)}")
        for category, items in self.recommendations.items():
            print(f"\n   💡 {category.upper().replace('_', ' ')}:")
            for item in items:
                print(f"      - {item}")

        # Save detailed report to file
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "file_stats": self.file_stats,
            "issues": dict(self.issues),
            "recommendations": dict(self.recommendations),
        }

        report_file = self.root_path / "repository_analysis_report.json"
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"\n📄 Detailed report saved to: {report_file}")
        print("=" * 80)


if __name__ == "__main__":
    analyzer = AuditoriaAnalyzer()
    analyzer.analyze_repository()
