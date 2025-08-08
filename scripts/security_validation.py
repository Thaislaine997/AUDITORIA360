#!/usr/bin/env python3
"""
AUDITORIA360 - Security Validation Script
Validates that no sensitive data remains in the repository after hardening
"""

import re
from pathlib import Path

# Patterns to search for sensitive data
SENSITIVE_PATTERNS = {
    "email_real": r"[a-zA-Z0-9._%+-]+@(?!exemplo\.com|empresa-exemplo\.com|teste\.com|example\.com|auditoria360-exemplo\.com)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "password_hardcoded": r'password\s*=\s*["\'][^"\']{6,}["\']',
    "api_key": r"(sk-[a-zA-Z0-9]{32,}|AKIA[0-9A-Z]{16})",
    "secret_key": r'secret[_-]?key\s*=\s*["\'][^"\']{16,}["\']',
    "jwt_secret": r"(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})",
    "real_cpf": r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}",
    "real_cnpj": r"[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}",
}

# Files/patterns to exclude from checking
EXCLUSIONS = {
    "files": [
        ".git/",
        "__pycache__/",
        ".env.example",
        ".env.template",
        "secrets.toml.template",
    ],
    "patterns": ["example", "template", "test_", "fake", "dummy"],
}

# Safe test data patterns that should be allowed
SAFE_PATTERNS = [
    r"111\.111\.111-11",
    r"222\.222\.222-22",
    r"333\.333\.333-33",
    r"123\.456\.789-[0-9]{2}",
    r"00\.000\.000/0000-00",
    r"11\.222\.333/0001-8[12]",
    r"exemplo\.com",
    r"example\.com",
    r"teste\.com",
    r"empresa-exemplo\.com",
    r"auditoria360-exemplo\.com",
    r"SENHA_DE_EXEMPLO",
    r"SUBSTITUA",
    r"REPLACE_WITH",
    r"JWT_SECRET_KEY=.*#.*checking.*variable.*name",
    r"SECRET_KEY=.*#.*checking.*variable.*name",
]


def is_safe_pattern(text, context=""):
    """Check if text matches known safe test patterns"""
    combined_text = f"{context} {text}"

    for pattern in SAFE_PATTERNS:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return True

    # Additional context-based checks
    if any(
        keyword in context.lower()
        for keyword in [
            "exemplo",
            "example",
            "test",
            "fake",
            "dummy",
            "template",
            "placeholder",
        ]
    ):
        return True

    # Check if it's a variable name check (not actual value)
    if "SECRET_KEY=" in text and any(
        keyword in context.lower()
        for keyword in ["checking", "variable", "configured", "vars"]
    ):
        return True

    return False


def should_exclude_file(filepath):
    """Check if file should be excluded from scanning"""
    path_str = str(filepath)

    # Check file exclusions
    for exclusion in EXCLUSIONS["files"]:
        if exclusion in path_str:
            return True

    # Check pattern exclusions
    for pattern in EXCLUSIONS["patterns"]:
        if pattern in path_str.lower():
            return True

    return False


def scan_file(filepath):
    """Scan a single file for sensitive patterns"""
    issues = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        for pattern_name, pattern in SENSITIVE_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)

            for match in matches:
                matched_text = match.group()
                context = content[max(0, match.start() - 50) : match.end() + 50]

                # Skip if it's a safe test pattern
                if is_safe_pattern(matched_text, context):
                    continue

    except Exception as e:
        print(f"Error scanning {filepath}: {e}")

    return issues


def scan_repository():
    """Scan entire repository for sensitive data"""
    repo_root = Path(__file__).parent
    issues = []

    # Scan Python files
    for pattern in ["**/*.py", "**/*.json", "**/*.yaml", "**/*.yml", "**/*.toml"]:
        for filepath in repo_root.glob(pattern):
            if should_exclude_file(filepath):
                continue

            file_issues = scan_file(filepath)
            issues.extend(file_issues)

    return issues


def main():
    """Main validation function"""
    print("🔒 AUDITORIA360 Security Validation")
    print("=" * 50)

    issues = scan_repository()

    if not issues:
        print("✅ No sensitive data found!")
        print("✅ Repository hardening validation PASSED")
        return True

    print(f"❌ Found {len(issues)} potential security issues:")
    print("-" * 50)

    for issue in issues:
        print(f"File: {issue['file']}")
        print(f"Line: {issue['line']}")
        print(f"Pattern: {issue['pattern']}")
        print(f"Match: {issue['match']}")
        print(f"Context: ...{issue['context']}...")
        print("-" * 30)

    print("❌ Repository hardening validation FAILED")
    return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
