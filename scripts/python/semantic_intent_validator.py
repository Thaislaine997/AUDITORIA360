#!/usr/bin/env python3
"""
IAI-C: Semantic Intent Validator
===============================
Part of the Manifesto da Singularidade Serverless

This validator goes beyond syntax checking to analyze the semantic intent
of code changes. It's the first layer of the Intrinsic Artificial Intelligence
in Code (IAI-C) system.
"""

import ast
import sys
import os
import re
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass


@dataclass
class SemanticViolation:
    """Represents a semantic violation detected by IAI-C"""
    file: str
    line: int
    column: int
    violation_type: str
    message: str
    severity: str  # 'critical', 'warning', 'info'
    business_rule: str = ""


class SemanticIntentAnalyzer(ast.NodeVisitor):
    """
    AST visitor that analyzes semantic intent of Python code.
    Implements the IAI-C consciousness layer.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: List[SemanticViolation] = []
        self.current_class = None
        self.current_function = None
        
        # Business rules database - This would normally be loaded from a configuration
        self.business_rules = {
            'payroll': {
                'negative_vacation_days': "Vacation days calculation cannot result in negative values",
                'salary_bounds': "Salary calculations must respect minimum wage and maximum bounds",
                'deduction_limits': "Deductions cannot exceed legal limits",
                'date_consistency': "Payroll dates must be consistent within competency period"
            },
            'financial': {
                'balance_validation': "Financial balances must always reconcile",
                'audit_trail': "All financial operations must maintain audit trail"
            },
            'security': {
                'data_exposure': "Sensitive data must never be logged or exposed",
                'access_control': "Access control must be enforced at all levels"
            }
        }

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Analyze function definitions for semantic intent violations"""
        previous_function = self.current_function
        self.current_function = node.name
        
        # Check for semantic violations in payroll functions
        if 'payroll' in self.file_path.lower() or 'payroll' in node.name.lower():
            self._analyze_payroll_function(node)
        
        # Check for potential security violations
        self._analyze_security_violations(node)
        
        # Check for business logic violations
        self._analyze_business_logic_violations(node)
        
        self.generic_visit(node)
        self.current_function = previous_function

    def _analyze_payroll_function(self, node: ast.FunctionDef):
        """Analyze payroll-specific functions for business rule violations"""
        
        # Check for functions that might allow negative vacation calculations
        if any(keyword in node.name.lower() for keyword in ['vacation', 'ferias', 'holiday']):
            # Look for potential negative value returns
            for child in ast.walk(node):
                if isinstance(child, ast.Return) and child.value:
                    if self._could_return_negative(child.value):
                        self.violations.append(SemanticViolation(
                            file=self.file_path,
                            line=child.lineno,
                            column=child.col_offset,
                            violation_type="semantic_intent",
                            message="Function may return negative vacation days - violates business logic",
                            severity="critical",
                            business_rule=self.business_rules['payroll']['negative_vacation_days']
                        ))

        # Check for salary calculation functions
        if any(keyword in node.name.lower() for keyword in ['salary', 'salario', 'calculate', 'calcular']):
            # Look for missing validation
            has_validation = False
            for child in ast.walk(node):
                if isinstance(child, ast.If):
                    # Check if there's validation for minimum values
                    if self._contains_minimum_validation(child):
                        has_validation = True
                        break
            
            if not has_validation and len([n for n in ast.walk(node) if isinstance(n, ast.Return)]) > 0:
                self.violations.append(SemanticViolation(
                    file=self.file_path,
                    line=node.lineno,
                    column=node.col_offset,
                    violation_type="missing_validation",
                    message="Salary calculation function lacks minimum wage validation",
                    severity="warning",
                    business_rule=self.business_rules['payroll']['salary_bounds']
                ))

    def _analyze_security_violations(self, node: ast.FunctionDef):
        """Analyze functions for potential security violations"""
        
        # Check for potential data exposure in logging
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                func_name = self._get_function_name(child)
                if func_name and any(log_func in func_name.lower() for log_func in ['log', 'print', 'debug']):
                    # Check if sensitive data might be logged
                    if self._contains_sensitive_data_reference(child):
                        self.violations.append(SemanticViolation(
                            file=self.file_path,
                            line=child.lineno,
                            column=child.col_offset,
                            violation_type="security_violation",
                            message="Potential sensitive data exposure in logging statement",
                            severity="critical",
                            business_rule=self.business_rules['security']['data_exposure']
                        ))

    def _analyze_business_logic_violations(self, node: ast.FunctionDef):
        """Analyze for general business logic violations"""
        
        # Check for hardcoded values that should be configurable
        for child in ast.walk(node):
            if isinstance(child, ast.Num) and hasattr(child, 'n'):
                if isinstance(child.n, (int, float)) and child.n > 1000:
                    # Large hardcoded numbers might be business constants
                    self.violations.append(SemanticViolation(
                        file=self.file_path,
                        line=child.lineno,
                        column=child.col_offset,
                        violation_type="configuration_violation",
                        message=f"Large hardcoded value {child.n} should be configurable",
                        severity="info",
                        business_rule="Business constants should be externally configurable"
                    ))

    def _could_return_negative(self, node: ast.AST) -> bool:
        """Check if an expression could potentially return a negative value"""
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            return True
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return True
        return False

    def _contains_minimum_validation(self, if_node: ast.If) -> bool:
        """Check if an if statement contains minimum value validation"""
        for child in ast.walk(if_node.test):
            if isinstance(child, ast.Compare):
                for op in child.ops:
                    if isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)):
                        return True
        return False

    def _get_function_name(self, call_node: ast.Call) -> str:
        """Extract function name from a call node"""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return ""

    def _contains_sensitive_data_reference(self, call_node: ast.Call) -> bool:
        """Check if a call contains references to sensitive data"""
        sensitive_keywords = ['password', 'token', 'secret', 'key', 'cpf', 'cnpj', 'salary']
        
        for arg in call_node.args:
            if isinstance(arg, ast.Str) and arg.s:
                if any(keyword in arg.s.lower() for keyword in sensitive_keywords):
                    return True
            elif isinstance(arg, ast.Name):
                if any(keyword in arg.id.lower() for keyword in sensitive_keywords):
                    return True
        return False


def analyze_file(file_path: str) -> List[SemanticViolation]:
    """Analyze a single Python file for semantic violations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=file_path)
        analyzer = SemanticIntentAnalyzer(file_path)
        analyzer.visit(tree)
        
        return analyzer.violations
    except SyntaxError as e:
        return [SemanticViolation(
            file=file_path,
            line=e.lineno or 0,
            column=e.offset or 0,
            violation_type="syntax_error",
            message=f"Syntax error prevents semantic analysis: {e.msg}",
            severity="critical"
        )]
    except Exception as e:
        return [SemanticViolation(
            file=file_path,
            line=0,
            column=0,
            violation_type="analysis_error",
            message=f"Error during semantic analysis: {str(e)}",
            severity="warning"
        )]


def main():
    """Main entry point for the semantic intent validator"""
    if len(sys.argv) < 2:
        print("Usage: semantic_intent_validator.py <file1> [file2] ...")
        sys.exit(1)
    
    all_violations = []
    
    for file_path in sys.argv[1:]:
        if not file_path.endswith('.py'):
            continue
            
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        violations = analyze_file(file_path)
        all_violations.extend(violations)
    
    # Report violations
    critical_count = 0
    warning_count = 0
    
    for violation in all_violations:
        icon = "🔴" if violation.severity == "critical" else "🟡" if violation.severity == "warning" else "🔵"
        print(f"{icon} {violation.file}:{violation.line}:{violation.column}")
        print(f"   Type: {violation.violation_type}")
        print(f"   Message: {violation.message}")
        if violation.business_rule:
            print(f"   Business Rule: {violation.business_rule}")
        print()
        
        if violation.severity == "critical":
            critical_count += 1
        elif violation.severity == "warning":
            warning_count += 1
    
    # Summary
    if all_violations:
        print(f"🧠 IAI-C Semantic Analysis Summary:")
        print(f"   Critical violations: {critical_count}")
        print(f"   Warnings: {warning_count}")
        print(f"   Total: {len(all_violations)}")
        
        if critical_count > 0:
            print("\n❌ Critical semantic violations detected. Code does not fulfill its philosophical purpose.")
            sys.exit(1)
        elif warning_count > 0:
            print("\n⚠️  Semantic warnings detected. Consider reviewing business logic alignment.")
            sys.exit(0)
    else:
        print("✅ No semantic violations detected. Code aligns with its intended purpose.")
    
    sys.exit(0)


if __name__ == "__main__":
    main()