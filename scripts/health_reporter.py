#!/usr/bin/env python3
"""
Automated weekly test coverage and health reporting for AUDITORIA360.
Generates comprehensive reports on code coverage, test failures, and project health.
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any
import xml.etree.ElementTree as ET

class ProjectHealthReporter:
    """Generate comprehensive project health reports."""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.report_date = datetime.datetime.now()
        self.report_data = {
            'date': self.report_date.isoformat(),
            'coverage': {},
            'tests': {},
            'dependencies': {},
            'git_stats': {},
            'issues': []
        }
    
    def run_coverage_analysis(self) -> Dict[str, Any]:
        """Run test coverage analysis and return results."""
        try:
            # Run pytest with coverage
            result = subprocess.run([
                'python', '-m', 'pytest',
                '--cov=services',
                '--cov=dashboards', 
                '--cov=scripts',
                '--cov-report=xml',
                '--cov-report=html',
                '--cov-report=json',
                '--quiet'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            # Parse coverage.json if it exists
            coverage_file = self.project_root / 'coverage.json'
            if coverage_file.exists():
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)
                
                total_coverage = coverage_data.get('totals', {}).get('percent_covered', 0)
                
                return {
                    'total_coverage': total_coverage,
                    'files': coverage_data.get('files', {}),
                    'status': 'success' if result.returncode == 0 else 'failed',
                    'missing_lines': coverage_data.get('totals', {}).get('missing_lines', 0)
                }
            else:
                return {'status': 'no_coverage_data', 'total_coverage': 0}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'total_coverage': 0}
    
    def run_test_analysis(self) -> Dict[str, Any]:
        """Run test suite and analyze results."""
        try:
            # Run tests with JUnit XML output
            result = subprocess.run([
                'python', '-m', 'pytest',
                '--junitxml=test-results.xml',
                '--tb=short',
                '-v'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            # Parse test results
            xml_file = self.project_root / 'test-results.xml'
            if xml_file.exists():
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                total_tests = int(root.get('tests', 0))
                failures = int(root.get('failures', 0))
                errors = int(root.get('errors', 0))
                skipped = int(root.get('skipped', 0))
                
                return {
                    'total_tests': total_tests,
                    'passed': total_tests - failures - errors - skipped,
                    'failed': failures,
                    'errors': errors,
                    'skipped': skipped,
                    'success_rate': ((total_tests - failures - errors) / total_tests * 100) if total_tests > 0 else 0,
                    'status': 'success' if result.returncode == 0 else 'failed'
                }
            else:
                return {'status': 'no_test_results', 'total_tests': 0}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'total_tests': 0}
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies for security and updates."""
        try:
            # Check for outdated packages
            result_outdated = subprocess.run([
                'pip', 'list', '--outdated', '--format=json'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            outdated = []
            if result_outdated.returncode == 0:
                outdated = json.loads(result_outdated.stdout)
            
            # Check for security vulnerabilities with safety
            result_safety = subprocess.run([
                'safety', 'check', '--json'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            vulnerabilities = []
            if result_safety.returncode != 0 and result_safety.stdout:
                try:
                    safety_data = json.loads(result_safety.stdout)
                    vulnerabilities = safety_data
                except json.JSONDecodeError:
                    pass
            
            return {
                'outdated_packages': len(outdated),
                'outdated_list': outdated[:10],  # Top 10 outdated
                'vulnerabilities': len(vulnerabilities),
                'vulnerability_list': vulnerabilities[:5],  # Top 5 vulnerabilities
                'status': 'clean' if len(vulnerabilities) == 0 else 'issues_found'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def analyze_git_stats(self) -> Dict[str, Any]:
        """Analyze git repository statistics."""
        try:
            # Get recent commits
            result_commits = subprocess.run([
                'git', 'log', '--oneline', '--since=1.week.ago'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            recent_commits = len(result_commits.stdout.strip().split('\n')) if result_commits.stdout.strip() else 0
            
            # Get contributors this week
            result_contributors = subprocess.run([
                'git', 'shortlog', '-sn', '--since=1.week.ago'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            contributors = len(result_contributors.stdout.strip().split('\n')) if result_contributors.stdout.strip() else 0
            
            # Get file changes
            result_changes = subprocess.run([
                'git', 'diff', '--stat', 'HEAD~7', 'HEAD'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            return {
                'recent_commits': recent_commits,
                'active_contributors': contributors,
                'has_recent_activity': recent_commits > 0,
                'changes_summary': result_changes.stdout[:500] if result_changes.stdout else 'No changes'
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def identify_issues(self) -> List[Dict[str, Any]]:
        """Identify potential issues in the codebase."""
        issues = []
        
        # Check for missing tests
        python_files = list(self.project_root.rglob('*.py'))
        test_files = list(self.project_root.rglob('test_*.py'))
        
        if len(test_files) / len(python_files) < 0.3:
            issues.append({
                'type': 'low_test_coverage',
                'severity': 'medium',
                'description': f'Test coverage ratio is low: {len(test_files)}/{len(python_files)} = {len(test_files)/len(python_files):.2%}'
            })
        
        # Check for large files
        for py_file in python_files:
            if py_file.stat().st_size > 50000:  # Files larger than 50KB
                issues.append({
                    'type': 'large_file',
                    'severity': 'low',
                    'description': f'Large file detected: {py_file.name} ({py_file.stat().st_size} bytes)'
                })
        
        # Check for TODO/FIXME comments
        todo_count = 0
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    todo_count += content.count('TODO') + content.count('FIXME')
            except Exception:
                pass
        
        if todo_count > 10:
            issues.append({
                'type': 'many_todos',
                'severity': 'low',
                'description': f'High number of TODO/FIXME comments: {todo_count}'
            })
        
        return issues
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive project health report."""
        print("Analyzing test coverage...")
        self.report_data['coverage'] = self.run_coverage_analysis()
        
        print("Analyzing test results...")
        self.report_data['tests'] = self.run_test_analysis()
        
        print("Analyzing dependencies...")
        self.report_data['dependencies'] = self.analyze_dependencies()
        
        print("Analyzing git statistics...")
        self.report_data['git_stats'] = self.analyze_git_stats()
        
        print("Identifying issues...")
        self.report_data['issues'] = self.identify_issues()
        
        return self.report_data
    
    def save_report(self, output_file: str = None) -> str:
        """Save report to file."""
        if not output_file:
            output_file = f"health_report_{self.report_date.strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = self.project_root / output_file
        with open(output_path, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        
        return str(output_path)
    
    def generate_markdown_summary(self) -> str:
        """Generate a markdown summary of the report."""
        coverage = self.report_data['coverage']
        tests = self.report_data['tests']
        deps = self.report_data['dependencies']
        git_stats = self.report_data['git_stats']
        issues = self.report_data['issues']
        
        md = f"""# AUDITORIA360 Weekly Health Report
**Generated:** {self.report_date.strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Test Coverage
- **Total Coverage:** {coverage.get('total_coverage', 0):.1f}%
- **Status:** {coverage.get('status', 'unknown')}

## 🧪 Test Results
- **Total Tests:** {tests.get('total_tests', 0)}
- **Passed:** {tests.get('passed', 0)}
- **Failed:** {tests.get('failed', 0)}
- **Success Rate:** {tests.get('success_rate', 0):.1f}%

## 📦 Dependencies
- **Outdated Packages:** {deps.get('outdated_packages', 0)}
- **Security Vulnerabilities:** {deps.get('vulnerabilities', 0)}
- **Status:** {deps.get('status', 'unknown')}

## 🔄 Git Activity (Last Week)
- **Recent Commits:** {git_stats.get('recent_commits', 0)}
- **Active Contributors:** {git_stats.get('active_contributors', 0)}
- **Has Activity:** {'✅' if git_stats.get('has_recent_activity') else '❌'}

## ⚠️ Issues Identified
"""
        
        if issues:
            for issue in issues:
                severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(issue['severity'], '⚪')
                md += f"- {severity_icon} **{issue['type']}:** {issue['description']}\n"
        else:
            md += "- ✅ No issues identified\n"
        
        md += f"""
## 📈 Health Score
"""
        
        # Calculate health score
        score = 0
        if coverage.get('total_coverage', 0) > 80:
            score += 25
        elif coverage.get('total_coverage', 0) > 60:
            score += 15
        elif coverage.get('total_coverage', 0) > 40:
            score += 10
        
        if tests.get('success_rate', 0) > 90:
            score += 25
        elif tests.get('success_rate', 0) > 80:
            score += 20
        elif tests.get('success_rate', 0) > 70:
            score += 15
        
        if deps.get('vulnerabilities', 1) == 0:
            score += 25
        elif deps.get('vulnerabilities', 1) < 3:
            score += 15
        
        if len([i for i in issues if i['severity'] == 'high']) == 0:
            score += 25
        elif len([i for i in issues if i['severity'] == 'high']) < 2:
            score += 15
        
        health_emoji = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
        md += f"**Overall Health Score:** {health_emoji} {score}/100\n"
        
        return md

def main():
    """Main function to run the health reporter."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    reporter = ProjectHealthReporter(project_root)
    
    print("Generating AUDITORIA360 health report...")
    report_data = reporter.generate_report()
    
    # Save JSON report
    json_file = reporter.save_report()
    print(f"JSON report saved to: {json_file}")
    
    # Generate and save markdown summary
    md_summary = reporter.generate_markdown_summary()
    md_file = os.path.join(project_root, f"health_summary_{reporter.report_date.strftime('%Y%m%d')}.md")
    with open(md_file, 'w') as f:
        f.write(md_summary)
    print(f"Markdown summary saved to: {md_file}")
    
    # Print summary to console
    print("\n" + "="*50)
    print(md_summary)
    
    return 0 if report_data['coverage'].get('total_coverage', 0) > 60 and report_data['tests'].get('success_rate', 0) > 80 else 1

if __name__ == '__main__':
    sys.exit(main())