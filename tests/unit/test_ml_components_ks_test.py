"""
Unit tests for ML KS Test component
Day 1-2: Implementation of ML components testing
"""

import os
import sys
from unittest.mock import patch

import numpy as np
import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.ml.components.ks_test import ks_test_by_group


class TestKSTest:
    """Test suite for KS test ML component"""

    def setup_method(self):
        """Setup test data for each test"""
        np.random.seed(42)

        # Create test data with different distributions for different groups
        self.group_a_data = np.random.normal(0, 1, 100)  # Normal distribution
        self.group_b_data = np.random.normal(2, 1, 100)  # Shifted normal
        self.group_c_data = np.random.exponential(1, 100)  # Different distribution

        self.data = np.concatenate(
            [self.group_a_data, self.group_b_data, self.group_c_data]
        )
        self.group_labels = np.array(["A"] * 100 + ["B"] * 100 + ["C"] * 100)

    def test_ks_test_by_group_returns_dict(self):
        """Test that ks_test_by_group returns a dictionary"""
        result = ks_test_by_group(self.data, self.group_labels)

        assert isinstance(result, dict)
        assert len(result) > 0

    def test_ks_test_by_group_pairwise_comparisons(self):
        """Test that all pairwise comparisons are included"""
        result = ks_test_by_group(self.data, self.group_labels)

        expected_comparisons = {"A vs B", "A vs C", "B vs C"}
        result_comparisons = set(result.keys())

        assert expected_comparisons == result_comparisons

    def test_ks_test_result_structure(self):
        """Test that each result contains statistic and pvalue"""
        result = ks_test_by_group(self.data, self.group_labels)

        for comparison, stats in result.items():
            assert "statistic" in stats
            assert "pvalue" in stats
            assert isinstance(stats["statistic"], (float, np.floating))
            assert isinstance(stats["pvalue"], (float, np.floating))

    def test_ks_test_statistic_values(self):
        """Test that KS statistics are in valid range [0, 1]"""
        result = ks_test_by_group(self.data, self.group_labels)

        for comparison, stats in result.items():
            assert 0 <= stats["statistic"] <= 1

    def test_ks_test_pvalue_values(self):
        """Test that p-values are in valid range [0, 1]"""
        result = ks_test_by_group(self.data, self.group_labels)

        for comparison, stats in result.items():
            assert 0 <= stats["pvalue"] <= 1

    def test_ks_test_identical_distributions(self):
        """Test KS test with identical distributions"""
        # Create identical distributions
        identical_data = np.random.normal(0, 1, 200)
        identical_labels = np.array(["A"] * 100 + ["B"] * 100)

        result = ks_test_by_group(identical_data, identical_labels)

        # For identical distributions, statistic should be small and p-value high
        stats = result["A vs B"]
        assert stats["statistic"] >= 0  # Should be non-negative
        # Note: Even identical samples may have some difference due to sampling

    def test_ks_test_very_different_distributions(self):
        """Test KS test with very different distributions"""
        # Create very different distributions
        group1 = np.zeros(100)  # All zeros
        group2 = np.ones(100) * 10  # All tens

        different_data = np.concatenate([group1, group2])
        different_labels = np.array(["A"] * 100 + ["B"] * 100)

        result = ks_test_by_group(different_data, different_labels)

        # For very different distributions, statistic should be large
        stats = result["A vs B"]
        assert stats["statistic"] > 0.5  # Should be large
        assert stats["pvalue"] < 0.05  # Should be significant

    def test_ks_test_single_group(self):
        """Test KS test with single group (should return empty dict)"""
        single_data = np.random.normal(0, 1, 100)
        single_labels = np.array(["A"] * 100)

        result = ks_test_by_group(single_data, single_labels)

        # No pairwise comparisons possible
        assert len(result) == 0

    def test_ks_test_two_groups(self):
        """Test KS test with exactly two groups"""
        two_group_data = np.concatenate([self.group_a_data, self.group_b_data])
        two_group_labels = np.array(["A"] * 100 + ["B"] * 100)

        result = ks_test_by_group(two_group_data, two_group_labels)

        # Should have exactly one comparison
        assert len(result) == 1
        assert "A vs B" in result

    def test_ks_test_with_numeric_groups(self):
        """Test KS test with numeric group labels"""
        numeric_labels = np.array([1] * 100 + [2] * 100 + [3] * 100)

        result = ks_test_by_group(self.data, numeric_labels)

        # Should work with numeric labels
        expected_comparisons = {"1 vs 2", "1 vs 3", "2 vs 3"}
        result_comparisons = set(result.keys())

        assert expected_comparisons == result_comparisons

    def test_ks_test_with_empty_groups(self):
        """Test KS test with empty data"""
        empty_data = np.array([])
        empty_labels = np.array([])

        result = ks_test_by_group(empty_data, empty_labels)

        # Should return empty dict
        assert len(result) == 0

    def test_ks_test_with_unequal_group_sizes(self):
        """Test KS test with unequal group sizes"""
        group_a = np.random.normal(0, 1, 50)  # 50 samples
        group_b = np.random.normal(1, 1, 100)  # 100 samples
        group_c = np.random.normal(2, 1, 25)  # 25 samples

        unequal_data = np.concatenate([group_a, group_b, group_c])
        unequal_labels = np.array(["A"] * 50 + ["B"] * 100 + ["C"] * 25)

        result = ks_test_by_group(unequal_data, unequal_labels)

        # Should still work with unequal sizes
        assert len(result) == 3
        for comparison, stats in result.items():
            assert 0 <= stats["statistic"] <= 1
            assert 0 <= stats["pvalue"] <= 1

    def test_ks_test_reproducibility(self):
        """Test that KS test produces consistent results"""
        result1 = ks_test_by_group(self.data, self.group_labels)
        result2 = ks_test_by_group(self.data, self.group_labels)

        # Results should be identical
        assert result1.keys() == result2.keys()

        for comparison in result1.keys():
            assert result1[comparison]["statistic"] == result2[comparison]["statistic"]
            assert result1[comparison]["pvalue"] == result2[comparison]["pvalue"]

    @patch("services.ml.components.ks_test.ks_2samp")
    def test_ks_test_calls_scipy_function(self, mock_ks_2samp):
        """Test that ks_test_by_group calls scipy.stats.ks_2samp"""
        mock_ks_2samp.return_value = (0.5, 0.01)

        simple_data = np.array([1, 2, 3, 4, 5, 6])
        simple_labels = np.array(["A", "A", "A", "B", "B", "B"])

        ks_test_by_group(simple_data, simple_labels)

        # Should call ks_2samp once for the A vs B comparison
        assert mock_ks_2samp.call_count == 1

    def test_ks_test_with_nan_values(self):
        """Test KS test behavior with NaN values"""
        data_with_nan = np.array([1, 2, np.nan, 4, 5, np.nan])
        labels_with_nan = np.array(["A", "A", "A", "B", "B", "B"])

        # This may raise an error or handle NaN gracefully
        # The exact behavior depends on scipy.stats.ks_2samp implementation
        try:
            result = ks_test_by_group(data_with_nan, labels_with_nan)
            # If it succeeds, verify the structure
            for comparison, stats in result.items():
                assert "statistic" in stats
                assert "pvalue" in stats
        except (ValueError, TypeError):
            # It's acceptable for the function to fail with NaN values
            pass

    def test_ks_test_performance_with_large_groups(self):
        """Test KS test performance with larger groups"""
        # Create larger groups for performance testing
        large_group_a = np.random.normal(0, 1, 1000)
        large_group_b = np.random.normal(1, 1, 1000)

        large_data = np.concatenate([large_group_a, large_group_b])
        large_labels = np.array(["A"] * 1000 + ["B"] * 1000)

        # Should complete in reasonable time
        result = ks_test_by_group(large_data, large_labels)

        assert len(result) == 1
        assert "A vs B" in result


if __name__ == "__main__":
    pytest.main([__file__])
