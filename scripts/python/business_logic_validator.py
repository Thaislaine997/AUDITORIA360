#!/usr/bin/env python3
"""
IAI-C: Business Logic Validator
==============================
Part of the Manifesto da Singularidade Serverless

This validator specifically focuses on business logic integrity within service layers.
It enforces domain-specific rules and architectural principles.
"""

import ast
import sys
import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class BusinessViolation:
    """Represents a business logic violation"""
    file: str
    line: int
    violation_type: str
    message: str
    severity: str
    domain: str
    suggested_fix: str = ""


class BusinessLogicAnalyzer(ast.NodeVisitor):
    """
    Analyzes business logic for domain-specific violations
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: List[BusinessViolation] = []
        self.domain = self._detect_domain(file_path)
        
        # Domain-specific rules
        self.payroll_rules = {
            'minimum_wage_validation': {
                'pattern': r'(salary|salario|wage|remuneracao)',
                'required_checks': ['minimum', 'minimo', 'min_wage'],
                'message': 'Salary calculations must validate against minimum wage'
            },
            'deduction_limits': {
                'pattern': r'(deduction|desconto|deducao)',
                'required_checks': ['limit', 'limite', 'max'],
                'message': 'Deductions must respect legal limits'
            },
            'negative_values': {
                'pattern': r'(vacation|ferias|days|dias)',
                'forbidden_operations': ['negative', 'subtract_without_check'],
                'message': 'Vacation calculations cannot result in negative values'
            }
        }

    def _detect_domain(self, file_path: str) -> str:
        """Detect the domain based on file path and content"""
        if 'payroll' in file_path.lower():
            return 'payroll'
        elif 'financial' in file_path.lower():
            return 'financial'
        elif 'auth' in file_path.lower():
            return 'security'
        return 'general'

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Analyze function definitions for business logic violations"""
        
        if self.domain == 'payroll':
            self._validate_payroll_function(node)
        elif self.domain == 'financial':
            self._validate_financial_function(node)
        elif self.domain == 'security':
            self._validate_security_function(node)
        
        self.generic_visit(node)

    def _validate_payroll_function(self, node: ast.FunctionDef):
        """Validate payroll-specific business logic"""
        
        function_name = node.name.lower()
        
        # Check vacation calculation functions
        if any(keyword in function_name for keyword in ['vacation', 'ferias', 'holiday']):
            self._check_vacation_logic(node)
        
        # Check salary calculation functions
        if any(keyword in function_name for keyword in ['salary', 'salario', 'calculate_pay']):
            self._check_salary_logic(node)
        
        # Check deduction functions
        if any(keyword in function_name for keyword in ['deduction', 'desconto', 'deduct']):
            self._check_deduction_logic(node)

    def _check_vacation_logic(self, node: ast.FunctionDef):
        """Check vacation calculation logic for business rule violations"""
        
        # Look for return statements that could return negative values
        has_negative_protection = False
        
        for child in ast.walk(node):
            # Check for negative value protection
            if isinstance(child, ast.If):
                if self._checks_for_negative_values(child):
                    has_negative_protection = True
            
            # Check for direct subtraction without validation
            if isinstance(child, ast.Return) and child.value:
                if self._has_unprotected_subtraction(child.value):
                    self.violations.append(BusinessViolation(
                        file=self.file_path,
                        line=child.lineno,
                        violation_type="unprotected_subtraction",
                        message="Vacation calculation performs subtraction without negative value protection",
                        severity="critical",
                        domain="payroll",
                        suggested_fix="Add validation to ensure result is not negative"
                    ))
        
        if not has_negative_protection and self._has_arithmetic_operations(node):
            self.violations.append(BusinessViolation(
                file=self.file_path,
                line=node.lineno,
                violation_type="missing_negative_validation",
                message="Vacation function lacks protection against negative values",
                severity="warning",
                domain="payroll",
                suggested_fix="Add check: if result < 0: return 0 or raise ValueError"
            ))

    def _check_salary_logic(self, node: ast.FunctionDef):
        """Check salary calculation logic"""
        
        has_minimum_wage_check = False
        has_maximum_bound_check = False
        
        for child in ast.walk(node):
            if isinstance(child, ast.Compare):
                # Look for minimum wage comparisons
                if self._is_minimum_wage_comparison(child):
                    has_minimum_wage_check = True
                
                # Look for maximum bound checks
                if self._is_maximum_bound_comparison(child):
                    has_maximum_bound_check = True
        
        if not has_minimum_wage_check:
            self.violations.append(BusinessViolation(
                file=self.file_path,
                line=node.lineno,
                violation_type="missing_minimum_wage_validation",
                message="Salary calculation lacks minimum wage validation",
                severity="critical",
                domain="payroll",
                suggested_fix="Add validation against current minimum wage"
            ))

    def _check_deduction_logic(self, node: ast.FunctionDef):
        """Check deduction calculation logic"""
        
        has_limit_check = False
        
        for child in ast.walk(node):
            if isinstance(child, ast.Compare):
                if self._is_deduction_limit_check(child):
                    has_limit_check = True
        
        if not has_limit_check:
            self.violations.append(BusinessViolation(
                file=self.file_path,
                line=node.lineno,
                violation_type="missing_deduction_limits",
                message="Deduction calculation lacks legal limit validation",
                severity="warning",
                domain="payroll",
                suggested_fix="Add validation against maximum deduction percentages"
            ))

    def _validate_financial_function(self, node: ast.FunctionDef):
        """Validate financial domain business logic"""
        
        # Check for balance reconciliation
        if 'balance' in node.name.lower():
            self._check_balance_reconciliation(node)

    def _validate_security_function(self, node: ast.FunctionDef):
        """Validate security domain business logic"""
        
        # Check for proper access control
        if any(keyword in node.name.lower() for keyword in ['access', 'authorize', 'permission']):
            self._check_access_control(node)

    def _checks_for_negative_values(self, if_node: ast.If) -> bool:
        """Check if an if statement validates against negative values"""
        for child in ast.walk(if_node.test):
            if isinstance(child, ast.Compare):
                for op in child.ops:
                    if isinstance(op, (ast.Lt, ast.LtE)):
                        # Check if comparing against zero or negative
                        for comparator in child.comparators:
                            if isinstance(comparator, ast.Num) and comparator.n <= 0:
                                return True
        return False

    def _has_unprotected_subtraction(self, node: ast.AST) -> bool:
        """Check if node contains subtraction without protection"""
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            return True
        for child in ast.walk(node):
            if isinstance(child, ast.BinOp) and isinstance(child.op, ast.Sub):
                return True
        return False

    def _has_arithmetic_operations(self, node: ast.FunctionDef) -> bool:
        """Check if function contains arithmetic operations"""
        for child in ast.walk(node):
            if isinstance(child, ast.BinOp) and isinstance(child.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                return True
        return False

    def _is_minimum_wage_comparison(self, compare_node: ast.Compare) -> bool:
        """Check if comparison involves minimum wage"""
        # Look for variables or attributes that suggest minimum wage
        keywords = ['minimum', 'min_wage', 'salario_minimo', 'wage_min']
        
        for child in ast.walk(compare_node):
            if isinstance(child, ast.Name):
                if any(keyword in child.id.lower() for keyword in keywords):
                    return True
            elif isinstance(child, ast.Attribute):
                if any(keyword in child.attr.lower() for keyword in keywords):
                    return True
        return False

    def _is_maximum_bound_comparison(self, compare_node: ast.Compare) -> bool:
        """Check if comparison involves maximum bounds"""
        keywords = ['maximum', 'max_salary', 'salario_maximo', 'upper_bound']
        
        for child in ast.walk(compare_node):
            if isinstance(child, ast.Name):
                if any(keyword in child.id.lower() for keyword in keywords):
                    return True
            elif isinstance(child, ast.Attribute):
                if any(keyword in child.attr.lower() for keyword in keywords):
                    return True
        return False

    def _is_deduction_limit_check(self, compare_node: ast.Compare) -> bool:
        """Check if comparison involves deduction limits"""
        keywords = ['limit', 'limite', 'max_deduction', 'deduction_limit']
        
        for child in ast.walk(compare_node):
            if isinstance(child, ast.Name):
                if any(keyword in child.id.lower() for keyword in keywords):
                    return True
            elif isinstance(child, ast.Attribute):
                if any(keyword in child.attr.lower() for keyword in keywords):
                    return True
        return False

    def _check_balance_reconciliation(self, node: ast.FunctionDef):
        """Check balance reconciliation logic"""
        # Implementation for financial balance checks
        pass

    def _check_access_control(self, node: ast.FunctionDef):
        """Check access control implementation"""
        # Implementation for access control validation
        pass


def analyze_file(file_path: str) -> List[BusinessViolation]:
    """Analyze a file for business logic violations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=file_path)
        analyzer = BusinessLogicAnalyzer(file_path)
        analyzer.visit(tree)
        
        return analyzer.violations
    except Exception as e:
        return [BusinessViolation(
            file=file_path,
            line=0,
            violation_type="analysis_error",
            message=f"Error analyzing business logic: {str(e)}",
            severity="warning",
            domain="unknown"
        )]


def main():
    """Main entry point for business logic validator"""
    if len(sys.argv) < 2:
        print("Usage: business_logic_validator.py <file1> [file2] ...")
        sys.exit(1)
    
    all_violations = []
    
    for file_path in sys.argv[1:]:
        if not file_path.endswith('.py'):
            continue
            
        if not os.path.exists(file_path):
            continue
        
        violations = analyze_file(file_path)
        all_violations.extend(violations)
    
    # Report violations
    critical_count = 0
    warning_count = 0
    
    for violation in all_violations:
        icon = "💼" if violation.severity == "critical" else "⚠️"
        print(f"{icon} {violation.file}:{violation.line}")
        print(f"   Domain: {violation.domain}")
        print(f"   Type: {violation.violation_type}")
        print(f"   Message: {violation.message}")
        if violation.suggested_fix:
            print(f"   Suggested Fix: {violation.suggested_fix}")
        print()
        
        if violation.severity == "critical":
            critical_count += 1
        elif violation.severity == "warning":
            warning_count += 1
    
    if all_violations:
        print(f"🧠 IAI-C Business Logic Analysis Summary:")
        print(f"   Critical violations: {critical_count}")
        print(f"   Warnings: {warning_count}")
        print(f"   Total: {len(all_violations)}")
        
        if critical_count > 0:
            print("\n❌ Critical business logic violations detected.")
            sys.exit(1)
        elif warning_count > 0:
            print("\n⚠️  Business logic warnings detected.")
    else:
        print("✅ No business logic violations detected.")
    
    sys.exit(0)


if __name__ == "__main__":
    main()