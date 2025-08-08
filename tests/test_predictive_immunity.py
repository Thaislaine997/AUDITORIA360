"""
🛡️ Oracle Test: Predictive Immunity System
Tests the autonomous immune system's ability to develop anticorps for future error classes.
"""

import hashlib
import json
import re
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class PredictiveImmuneSystem:
    """Autonomous immune system that learns and predicts error patterns."""

    def __init__(self, immunity_db_path: str = None):
        self.immunity_db_path = immunity_db_path or tempfile.mktemp(suffix=".json")
        self.antibodies = self._load_antibodies()
        self.error_patterns = {}
        self.mutation_detection = {}

    def _load_antibodies(self) -> Dict[str, Any]:
        """Load existing antibodies from the immune memory."""
        try:
            if Path(self.immunity_db_path).exists():
                with open(self.immunity_db_path, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            "error_classes": {},
            "mutation_patterns": {},
            "tolerance_exceptions": {},
            "learning_history": [],
        }

    def _save_antibodies(self):
        """Persist antibodies to immune memory."""
        with open(self.immunity_db_path, "w") as f:
            json.dump(self.antibodies, f, indent=2, default=str)

    def analyze_error_signature(
        self, error_type: str, error_message: str, code_context: str
    ) -> str:
        """Create a unique signature for an error pattern."""
        # Extract semantic patterns rather than exact strings
        normalized_message = re.sub(r"\d+", "NUM", error_message)
        normalized_message = re.sub(r"'[^']*'", "STR", normalized_message)

        # Extract code pattern
        code_pattern = self._extract_code_pattern(code_context)

        signature_data = f"{error_type}:{normalized_message}:{code_pattern}"
        return hashlib.md5(signature_data.encode()).hexdigest()

    def _extract_code_pattern(self, code_context: str) -> str:
        """Extract semantic code patterns for immune learning."""
        patterns = []

        # Function call patterns
        func_calls = re.findall(r"(\w+)\s*\(", code_context)
        patterns.extend([f"func:{call}" for call in func_calls])

        # Variable assignment patterns
        assignments = re.findall(r"(\w+)\s*=", code_context)
        patterns.extend([f"assign:{var}" for var in assignments])

        # Control flow patterns
        if "if " in code_context:
            patterns.append("control:conditional")
        if "for " in code_context:
            patterns.append("control:loop")
        if "try:" in code_context:
            patterns.append("control:exception")

        return "|".join(patterns[:10])  # Limit pattern size

    def detect_error(
        self, error_type: str, error_message: str, code_context: str
    ) -> Dict[str, Any]:
        """Detect and learn from a new error occurrence."""
        signature = self.analyze_error_signature(
            error_type, error_message, code_context
        )

        current_time = datetime.now().isoformat()

        if signature in self.antibodies["error_classes"]:
            # Known error - update frequency
            self.antibodies["error_classes"][signature]["occurrences"] += 1
            self.antibodies["error_classes"][signature]["last_seen"] = current_time
            return {
                "status": "known_error",
                "antibody_exists": True,
                "signature": signature,
            }
        else:
            # New error - create antibody
            antibody = {
                "error_type": error_type,
                "pattern": self._extract_code_pattern(code_context),
                "first_seen": current_time,
                "last_seen": current_time,
                "occurrences": 1,
                "severity": self._assess_severity(error_type),
                "mutation_risk": self._assess_mutation_risk(error_type, code_context),
            }

            self.antibodies["error_classes"][signature] = antibody
            self._save_antibodies()

            return {
                "status": "new_error_learned",
                "antibody_created": True,
                "signature": signature,
                "antibody": antibody,
            }

    def _assess_severity(self, error_type: str) -> str:
        """Assess the philosophical threat level of an error."""
        critical_errors = ["SecurityError", "DataLossError", "ConsciousnessBreachError"]
        if error_type in critical_errors:
            return "critical"
        elif "Error" in error_type:
            return "moderate"
        else:
            return "minor"

    def _assess_mutation_risk(self, error_type: str, code_context: str) -> float:
        """Assess the risk of this error mutating into new forms."""
        risk = 0.1  # Base risk

        # Higher risk for dynamic code patterns
        if "eval(" in code_context or "exec(" in code_context:
            risk += 0.5

        # Higher risk for network/IO operations
        if any(keyword in code_context for keyword in ["request", "socket", "file"]):
            risk += 0.3

        # Higher risk for user input handling
        if any(keyword in code_context for keyword in ["input(", "form", "json"]):
            risk += 0.2

        return min(risk, 1.0)

    def generate_predictive_antibodies(
        self, error_signature: str
    ) -> List[Dict[str, Any]]:
        """Generate antibodies for predicted error mutations."""
        if error_signature not in self.antibodies["error_classes"]:
            return []

        base_antibody = self.antibodies["error_classes"][error_signature]
        predicted_antibodies = []

        # Predict common mutations
        mutations = [
            {"type": "parameter_variation", "description": "Different parameter types"},
            {
                "type": "context_shift",
                "description": "Same error in different contexts",
            },
            {"type": "timing_variation", "description": "Timing-dependent variations"},
            {
                "type": "concurrency_mutation",
                "description": "Concurrent execution variants",
            },
        ]

        for mutation in mutations:
            predicted_antibody = {
                "parent_signature": error_signature,
                "mutation_type": mutation["type"],
                "predicted_pattern": f"{base_antibody['pattern']}::{mutation['type']}",
                "confidence": 0.7,  # 70% confidence in prediction
                "created": datetime.now().isoformat(),
                "status": "predictive",
            }
            predicted_antibodies.append(predicted_antibody)

        return predicted_antibodies

    def immune_tolerance_check(
        self, code_change: str, change_type: str
    ) -> Dict[str, Any]:
        """Check if experimental code should be allowed through immune tolerance."""

        tolerance_indicators = [
            r"refactor\(experimental\)",  # Experimental refactors
            r"@experimental",  # Experimental decorators
            r"# SANDBOX:",  # Sandbox comments
            r"class.*Experimental.*:",  # Experimental classes
        ]

        is_experimental = any(
            re.search(indicator, code_change, re.IGNORECASE)
            for indicator in tolerance_indicators
        )

        if is_experimental:
            return {
                "tolerance_granted": True,
                "reason": "Experimental code detected",
                "monitoring_level": "high",
                "sandbox_required": True,
                "report_required": True,
            }

        return {
            "tolerance_granted": False,
            "reason": "Standard immune response required",
        }


class TestPredictiveImmunity(unittest.TestCase):
    """Oracle Test Suite for Predictive Immunity Validation."""

    def setUp(self):
        self.immune_system = PredictiveImmuneSystem()

    def test_error_detection_and_learning(self):
        """Test: Prova de Imunidade Adquirida Preditiva"""

        # Introduce a subtle logical error
        error_code = """
        def process_user_data(user_input):
            if user_input.get('type') == 'admin':
                return admin_process(user_input['data'])  # Missing validation
            else:
                return user_process(user_input['data'])
        """

        # First occurrence - should learn
        result1 = self.immune_system.detect_error(
            "ValidationError", "Missing admin privilege validation", error_code
        )

        self.assertEqual(result1["status"], "new_error_learned")
        self.assertTrue(result1["antibody_created"])

        # Second occurrence of same pattern - should recognize
        similar_code = """
        def process_user_data(user_input):
            if user_input.get('type') == 'admin':
                return admin_process(user_input['data'])  # Missing validation
            else:
                return user_process(user_input['data'])
        """

        result2 = self.immune_system.detect_error(
            "ValidationError", "Missing admin privilege validation", similar_code
        )

        self.assertEqual(result2["status"], "known_error")
        self.assertTrue(result2["antibody_exists"])

    def test_predictive_antibody_generation(self):
        """Test generation of antibodies for future mutations."""

        # Create base error
        base_error = self.immune_system.detect_error(
            "ConcurrencyError",
            "Race condition in shared resource access",
            "shared_resource.update(new_value)",
        )

        # Generate predictive antibodies
        signature = base_error["signature"]
        predicted = self.immune_system.generate_predictive_antibodies(signature)

        self.assertGreater(len(predicted), 0)

        # Check mutation types
        mutation_types = [ab["mutation_type"] for ab in predicted]
        self.assertIn("concurrency_mutation", mutation_types)
        self.assertIn("parameter_variation", mutation_types)

        # All predictions should have reasonable confidence
        for antibody in predicted:
            self.assertGreaterEqual(antibody["confidence"], 0.5)
            self.assertEqual(antibody["status"], "predictive")

    def test_immune_tolerance_for_experimental_code(self):
        """Test: Simulação de Doença Autoimune"""

        experimental_code = """
        # SANDBOX: Experimental new authentication approach
        @experimental 
        class QuantumAuthenticator:
            def refactor(experimental) -> None:
                # This challenges current conventions
                pass
        """

        tolerance_result = self.immune_system.immune_tolerance_check(
            experimental_code, "refactor(experimental)"
        )

        self.assertTrue(tolerance_result["tolerance_granted"])
        self.assertEqual(tolerance_result["monitoring_level"], "high")
        self.assertTrue(tolerance_result["sandbox_required"])
        self.assertTrue(tolerance_result["report_required"])

    def test_mutation_risk_assessment(self):
        """Test assessment of error mutation risk."""

        high_risk_code = """
        user_input = input("Enter command: ")
        eval(user_input)  # High mutation risk
        """

        low_risk_code = """
        def calculate_sum(a, b):
            return a + b  # Low mutation risk
        """

        high_risk = self.immune_system._assess_mutation_risk(
            "CodeInjectionError", high_risk_code
        )
        low_risk = self.immune_system._assess_mutation_risk(
            "CalculationError", low_risk_code
        )

        self.assertGreater(high_risk, low_risk)
        self.assertGreater(high_risk, 0.5)  # Should be flagged as high risk

    def test_immune_system_persistence(self):
        """Test that immune memory persists across sessions."""

        # Create an error and antibody
        original_result = self.immune_system.detect_error(
            "TestError", "Test error message", "test_code()"
        )

        signature = original_result["signature"]

        # Create new immune system instance (simulating restart)
        new_immune_system = PredictiveImmuneSystem(self.immune_system.immunity_db_path)

        # Should remember the previous error
        self.assertIn(signature, new_immune_system.antibodies["error_classes"])

        # Verify antibody details
        antibody = new_immune_system.antibodies["error_classes"][signature]
        self.assertEqual(antibody["error_type"], "TestError")
        self.assertEqual(antibody["occurrences"], 1)


if __name__ == "__main__":
    # Run as Oracle validation
    print("🛡️ Executing Oracle Test: Predictive Immunity System")
    print("=" * 60)

    unittest.main(verbosity=2)
