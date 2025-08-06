#!/usr/bin/env python3
"""
IAI-C: Dependency Entropy Scanner
=================================
Part of the Manifesto da Singularidade Serverless

This scanner identifies dependencies with high entropy (low usage, high maintenance cost)
and automatically creates issues for deprecation when the cost exceeds value.
"""

import os
import sys
import json
import re
import subprocess
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import ast


@dataclass
class DependencyAnalysis:
    """Analysis result for a dependency"""
    name: str
    version: str
    usage_count: int
    last_used_file: str
    maintenance_cost: float  # 0.0 to 1.0
    business_value: float   # 0.0 to 1.0
    entropy_score: float    # Higher = more entropy (bad)
    recommendation: str     # 'keep', 'deprecate', 'remove'
    reasoning: str


class DependencyEntropyScanner:
    """
    Scans project dependencies and calculates entropy scores
    """
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.dependencies: Dict[str, DependencyAnalysis] = {}
        
        # Critical dependencies that should never be flagged
        self.critical_deps = {
            'fastapi', 'uvicorn', 'sqlalchemy', 'psycopg2-binary',
            'pandas', 'numpy', 'pydantic', 'python-dotenv',
            'pytest', 'black', 'isort', 'flake8'
        }
        
        # Deprecated or problematic patterns
        self.problematic_patterns = {
            'outdated_ml': ['sklearn==0.24', 'tensorflow==1.'],
            'legacy_web': ['flask==1.0', 'django==2.'],
            'unused_ocr': ['pytesseract', 'opencv-python==3.'],
            'redundant_tools': ['autopep8', 'yapf']  # When black is already used
        }

    def scan_python_dependencies(self) -> List[DependencyAnalysis]:
        """Scan Python dependencies from requirements files"""
        analyses = []
        
        # Read requirements files
        req_files = ['requirements.txt', 'requirements-dev.txt', 'requirements-ml.txt']
        all_deps = {}
        
        for req_file in req_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                deps = self._parse_requirements_file(req_path)
                all_deps.update(deps)
        
        # Analyze each dependency
        for dep_name, version in all_deps.items():
            if dep_name.lower() in self.critical_deps:
                continue  # Skip critical dependencies
            
            analysis = self._analyze_python_dependency(dep_name, version)
            analyses.append(analysis)
        
        return analyses

    def scan_npm_dependencies(self) -> List[DependencyAnalysis]:
        """Scan NPM dependencies from package.json"""
        analyses = []
        
        package_json = self.project_root / 'package.json'
        if not package_json.exists():
            return analyses
        
        try:
            with open(package_json, 'r') as f:
                data = json.load(f)
            
            # Analyze dependencies and devDependencies
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in data:
                    for dep_name, version in data[dep_type].items():
                        analysis = self._analyze_npm_dependency(dep_name, version)
                        analyses.append(analysis)
        
        except Exception as e:
            print(f"Error reading package.json: {e}")
        
        return analyses

    def _parse_requirements_file(self, file_path: Path) -> Dict[str, str]:
        """Parse a requirements.txt file"""
        deps = {}
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse dependency name and version
                        match = re.match(r'^([a-zA-Z0-9_-]+)([>=<~!]+.*)?', line)
                        if match:
                            name = match.group(1)
                            version = match.group(2) or ''
                            deps[name] = version
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return deps

    def _analyze_python_dependency(self, name: str, version: str) -> DependencyAnalysis:
        """Analyze a Python dependency"""
        
        # Count usage in codebase
        usage_count = self._count_python_usage(name)
        
        # Calculate maintenance cost
        maintenance_cost = self._calculate_maintenance_cost(name, version)
        
        # Calculate business value
        business_value = self._calculate_business_value(name, usage_count)
        
        # Calculate entropy score
        entropy_score = maintenance_cost / max(business_value, 0.1)
        
        # Make recommendation
        recommendation, reasoning = self._make_recommendation(
            name, usage_count, maintenance_cost, business_value, entropy_score
        )
        
        return DependencyAnalysis(
            name=name,
            version=version,
            usage_count=usage_count,
            last_used_file=self._find_last_usage_file(name),
            maintenance_cost=maintenance_cost,
            business_value=business_value,
            entropy_score=entropy_score,
            recommendation=recommendation,
            reasoning=reasoning
        )

    def _analyze_npm_dependency(self, name: str, version: str) -> DependencyAnalysis:
        """Analyze an NPM dependency"""
        
        # Count usage in frontend code
        usage_count = self._count_npm_usage(name)
        
        # For now, use simplified analysis for NPM
        maintenance_cost = 0.3  # Default moderate cost
        business_value = min(usage_count / 10, 1.0)
        entropy_score = maintenance_cost / max(business_value, 0.1)
        
        recommendation = 'keep' if usage_count > 0 else 'deprecate'
        reasoning = f"Usage count: {usage_count}"
        
        return DependencyAnalysis(
            name=name,
            version=version,
            usage_count=usage_count,
            last_used_file="",
            maintenance_cost=maintenance_cost,
            business_value=business_value,
            entropy_score=entropy_score,
            recommendation=recommendation,
            reasoning=reasoning
        )

    def _count_python_usage(self, dep_name: str) -> int:
        """Count how many times a dependency is imported/used"""
        usage_count = 0
        
        # Search for imports
        import_patterns = [
            f"import {dep_name}",
            f"from {dep_name}",
            f"import {dep_name.replace('-', '_')}",
            f"from {dep_name.replace('-', '_')}"
        ]
        
        # Search through Python files
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in import_patterns:
                    usage_count += len(re.findall(pattern, content, re.IGNORECASE))
                    
            except Exception:
                continue
        
        return usage_count

    def _count_npm_usage(self, dep_name: str) -> int:
        """Count usage of NPM dependency"""
        usage_count = 0
        
        # Search in JS/TS files
        patterns = [
            f"require('{dep_name}')",
            f'require("{dep_name}")',
            f"import.*from '{dep_name}'",
            f'import.*from "{dep_name}"'
        ]
        
        for file_ext in ['*.js', '*.ts', '*.jsx', '*.tsx']:
            for js_file in self.project_root.rglob(file_ext):
                try:
                    with open(js_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in patterns:
                        usage_count += len(re.findall(pattern, content))
                        
                except Exception:
                    continue
        
        return usage_count

    def _calculate_maintenance_cost(self, name: str, version: str) -> float:
        """Calculate maintenance cost (0.0 to 1.0)"""
        cost = 0.2  # Base cost
        
        # Check for problematic patterns
        for category, patterns in self.problematic_patterns.items():
            for pattern in patterns:
                if name in pattern or pattern in f"{name}{version}":
                    cost += 0.3
                    break
        
        # Very specific version constraints increase maintenance cost
        if '>=' in version or '==' in version:
            cost += 0.1
        
        # Alpha/beta versions
        if any(tag in version.lower() for tag in ['alpha', 'beta', 'rc', 'dev']):
            cost += 0.2
        
        # Large, complex packages
        complex_packages = ['tensorflow', 'pytorch', 'opencv', 'scipy']
        if any(pkg in name.lower() for pkg in complex_packages):
            cost += 0.1
        
        return min(cost, 1.0)

    def _calculate_business_value(self, name: str, usage_count: int) -> float:
        """Calculate business value (0.0 to 1.0)"""
        
        # Base value from usage
        value = min(usage_count / 20, 0.6)
        
        # Core business functionality
        business_critical = [
            'fastapi', 'sqlalchemy', 'pandas', 'psycopg2',
            'pydantic', 'uvicorn', 'prefect', 'openai'
        ]
        
        if any(critical in name.lower() for critical in business_critical):
            value += 0.4
        
        # Development tools
        dev_tools = ['pytest', 'black', 'isort', 'flake8', 'pre-commit']
        if any(tool in name.lower() for tool in dev_tools):
            value += 0.3
        
        # Security tools
        security_tools = ['cryptography', 'passlib', 'python-jose']
        if any(tool in name.lower() for tool in security_tools):
            value += 0.2
        
        return min(value, 1.0)

    def _find_last_usage_file(self, dep_name: str) -> str:
        """Find the file where dependency was last used"""
        
        import_patterns = [
            f"import {dep_name}",
            f"from {dep_name}",
            f"import {dep_name.replace('-', '_')}",
            f"from {dep_name.replace('-', '_')}"
        ]
        
        last_file = ""
        
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in import_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        last_file = str(py_file.relative_to(self.project_root))
                        break
                        
            except Exception:
                continue
        
        return last_file

    def _make_recommendation(self, name: str, usage_count: int, maintenance_cost: float, 
                           business_value: float, entropy_score: float) -> Tuple[str, str]:
        """Make recommendation based on analysis"""
        
        if usage_count == 0:
            return 'remove', f"Unused dependency with {maintenance_cost:.1%} maintenance cost"
        
        if entropy_score > 2.0:
            return 'deprecate', f"High entropy score ({entropy_score:.2f}) - maintenance cost exceeds value"
        
        if entropy_score > 1.5 and usage_count < 3:
            return 'deprecate', f"Low usage ({usage_count} imports) with high maintenance overhead"
        
        if maintenance_cost > 0.7:
            return 'deprecate', f"High maintenance cost ({maintenance_cost:.1%}) - consider alternatives"
        
        return 'keep', f"Good balance of value ({business_value:.1%}) vs cost ({maintenance_cost:.1%})"


def generate_github_issue_content(high_entropy_deps: List[DependencyAnalysis]) -> str:
    """Generate GitHub issue content for high entropy dependencies"""
    
    if not high_entropy_deps:
        return ""
    
    issue_content = """# 🧬 Dependency Entropy Alert - Genetic Cleanup Required

## IAI-C Temporal Erosion Analysis

The Intrinsic Artificial Intelligence has detected dependencies with high entropy scores, indicating that their maintenance cost exceeds their functional value. These represent "genetic mutations" that should be cleaned from our digital organism.

## High Entropy Dependencies Detected

"""
    
    for dep in high_entropy_deps:
        issue_content += f"""### {dep.name} (Entropy: {dep.entropy_score:.2f})
- **Version**: {dep.version}
- **Usage Count**: {dep.usage_count}
- **Maintenance Cost**: {dep.maintenance_cost:.1%}
- **Business Value**: {dep.business_value:.1%}
- **Recommendation**: {dep.recommendation.upper()}
- **Reasoning**: {dep.reasoning}
- **Last Used**: {dep.last_used_file or 'Not found'}

"""
    
    issue_content += """
## Recommended Actions

1. **Immediate Review**: Evaluate each flagged dependency
2. **Deprecation Plan**: Create timeline for removal of unused dependencies
3. **Alternative Assessment**: Research modern alternatives for high-cost dependencies
4. **Automated Cleanup**: Implement automated removal of truly unused dependencies

## IAI-C Philosophy

> "A system that cannot clean itself of entropy will eventually collapse under the weight of its own complexity. The serverless organism must shed dead cells to remain vital."

This issue was automatically generated by the IAI-C Dependency Entropy Scanner as part of the Manifesto da Singularidade Serverless.

**Labels**: `entropy`, `dependencies`, `maintenance`, `iai-c`, `automated`
"""
    
    return issue_content


def main():
    """Main entry point for dependency entropy scanner"""
    if len(sys.argv) < 2:
        project_root = os.getcwd()
    else:
        project_root = sys.argv[1]
    
    scanner = DependencyEntropyScanner(project_root)
    
    # Scan dependencies
    python_analyses = scanner.scan_python_dependencies()
    npm_analyses = scanner.scan_npm_dependencies()
    
    all_analyses = python_analyses + npm_analyses
    
    # Filter high entropy dependencies
    high_entropy = [dep for dep in all_analyses if dep.entropy_score > 1.5 or dep.recommendation in ['deprecate', 'remove']]
    
    # Report results
    print("🧬 IAI-C Dependency Entropy Analysis")
    print("=" * 50)
    
    if high_entropy:
        print(f"\n⚠️  High Entropy Dependencies Detected: {len(high_entropy)}")
        
        for dep in high_entropy:
            icon = "🗑️" if dep.recommendation == 'remove' else "⚠️"
            print(f"\n{icon} {dep.name}")
            print(f"   Entropy Score: {dep.entropy_score:.2f}")
            print(f"   Usage: {dep.usage_count} imports")
            print(f"   Recommendation: {dep.recommendation.upper()}")
            print(f"   Reasoning: {dep.reasoning}")
        
        # Generate GitHub issue content
        issue_content = generate_github_issue_content(high_entropy)
        
        # Save issue content to file
        issue_file = Path(project_root) / "dependency_entropy_issue.md"
        with open(issue_file, 'w') as f:
            f.write(issue_content)
        
        print(f"\n📝 GitHub issue content generated: {issue_file}")
        print("\n⚡ IAI-C Recommendation: Review and clean high entropy dependencies")
        
        sys.exit(1)  # Exit with error code to flag in CI
    
    else:
        print("\n✅ No high entropy dependencies detected")
        print("🧬 Digital organism DNA is clean and optimized")
    
    # Report summary
    print(f"\nAnalyzed {len(all_analyses)} dependencies:")
    keep_count = len([d for d in all_analyses if d.recommendation == 'keep'])
    deprecate_count = len([d for d in all_analyses if d.recommendation == 'deprecate'])
    remove_count = len([d for d in all_analyses if d.recommendation == 'remove'])
    
    print(f"  ✅ Keep: {keep_count}")
    print(f"  ⚠️  Deprecate: {deprecate_count}")
    print(f"  🗑️  Remove: {remove_count}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()