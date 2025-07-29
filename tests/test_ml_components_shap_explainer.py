"""
Unit tests for ML SHAP Explainer component
Day 1-2: Implementation of ML components testing
"""

import os
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mock shap if not available
try:
    import shap
except ImportError:
    sys.modules["shap"] = MagicMock()

from services.ml.components.shap_explainer import explain_with_shap


class TestShapExplainer:
    """Test suite for SHAP explainer ML component"""

    def setup_method(self):
        """Setup test data for each test"""
        np.random.seed(42)
        self.X = np.random.rand(100, 5)
        self.model = MagicMock()
        self.model.predict.return_value = np.random.rand(100)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_creates_explainer(self, mock_explainer_class):
        """Test that explain_with_shap creates a SHAP explainer"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, self.X, nsamples=10)

        # Check that explainer was created with correct arguments
        mock_explainer_class.assert_called_once_with(self.model, self.X)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_calls_explainer(self, mock_explainer_class):
        """Test that explain_with_shap calls the explainer with correct data"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_shap_values = MagicMock()
        mock_explainer.return_value = mock_shap_values

        nsamples = 20
        result = explain_with_shap(self.model, self.X, nsamples=nsamples)

        # Check that explainer was called with correct subset of data
        mock_explainer.assert_called_once_with(self.X[:nsamples])
        assert result == mock_shap_values

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_default_nsamples(self, mock_explainer_class):
        """Test explain_with_shap with default nsamples parameter"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, self.X)

        # Should use default nsamples=100
        mock_explainer.assert_called_once_with(self.X[:100])

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_returns_shap_values(self, mock_explainer_class):
        """Test that explain_with_shap returns SHAP values"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_shap_values = MagicMock()
        mock_explainer.return_value = mock_shap_values

        result = explain_with_shap(self.model, self.X, nsamples=10)

        assert result == mock_shap_values

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_small_dataset(self, mock_explainer_class):
        """Test explain_with_shap with small dataset"""
        small_X = self.X[:5]  # Only 5 samples

        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, small_X, nsamples=10)

        # Should use all available data since nsamples > dataset size
        mock_explainer.assert_called_once_with(small_X[:10])

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_zero_nsamples(self, mock_explainer_class):
        """Test explain_with_shap with zero nsamples"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, self.X, nsamples=0)

        # Should use empty array
        mock_explainer.assert_called_once()
        call_args = mock_explainer.call_args[0][0]
        assert len(call_args) == 0

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_single_feature(self, mock_explainer_class):
        """Test explain_with_shap with single feature data"""
        single_feature_X = np.random.rand(50, 1)

        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, single_feature_X, nsamples=20)

        # Should work with single feature
        mock_explainer_class.assert_called_once_with(self.model, single_feature_X)
        mock_explainer.assert_called_once_with(single_feature_X[:20])

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_many_features(self, mock_explainer_class):
        """Test explain_with_shap with many features"""
        many_features_X = np.random.rand(100, 50)

        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, many_features_X, nsamples=30)

        # Should work with many features
        mock_explainer_class.assert_called_once_with(self.model, many_features_X)
        mock_explainer.assert_called_once_with(many_features_X[:30])

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_handles_explainer_exception(self, mock_explainer_class):
        """Test that explain_with_shap handles explainer creation exceptions"""
        mock_explainer_class.side_effect = Exception("SHAP explainer creation failed")

        with pytest.raises(Exception):
            explain_with_shap(self.model, self.X, nsamples=10)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_handles_explanation_exception(
        self, mock_explainer_class
    ):
        """Test that explain_with_shap handles explanation generation exceptions"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.side_effect = Exception("Explanation generation failed")

        with pytest.raises(Exception):
            explain_with_shap(self.model, self.X, nsamples=10)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_large_nsamples(self, mock_explainer_class):
        """Test explain_with_shap with nsamples larger than dataset"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        large_nsamples = len(self.X) + 50
        explain_with_shap(self.model, self.X, nsamples=large_nsamples)

        # Should handle gracefully (numpy will return available data)
        mock_explainer.assert_called_once_with(self.X[:large_nsamples])

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_negative_nsamples(self, mock_explainer_class):
        """Test explain_with_shap with negative nsamples"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_with_shap(self.model, self.X, nsamples=-10)

        # Negative indexing should work in numpy
        mock_explainer.assert_called_once_with(self.X[:-10])

    def test_explain_with_shap_input_validation(self):
        """Test explain_with_shap input validation"""
        # Test with None model
        with pytest.raises(AttributeError):
            explain_with_shap(None, self.X, nsamples=10)

        # Test with None data
        with pytest.raises((TypeError, AttributeError)):
            explain_with_shap(self.model, None, nsamples=10)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_different_data_types(self, mock_explainer_class):
        """Test explain_with_shap with different numpy data types"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        # Test with integer data
        int_X = np.random.randint(0, 10, (50, 3))
        explain_with_shap(self.model, int_X, nsamples=20)

        # Should handle integer data
        mock_explainer_class.assert_called_with(self.model, int_X)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_extreme_values(self, mock_explainer_class):
        """Test explain_with_shap with extreme values"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        # Test with extreme values
        extreme_X = np.array([[1e10, -1e10], [1e-10, -1e-10]])
        explain_with_shap(self.model, extreme_X, nsamples=1)

        # Should handle extreme values
        mock_explainer_class.assert_called_once_with(self.model, extreme_X)

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_reproducibility(self, mock_explainer_class):
        """Test that explain_with_shap calls are consistent"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_shap_values = MagicMock()
        mock_explainer.return_value = mock_shap_values

        # Call twice with same parameters
        result1 = explain_with_shap(self.model, self.X, nsamples=50)
        result2 = explain_with_shap(self.model, self.X, nsamples=50)

        # Both should return the same mock object
        assert result1 == result2

        # Should have been called twice with same parameters
        assert mock_explainer_class.call_count == 2
        assert mock_explainer.call_count == 2

    @patch("services.ml.components.shap_explainer.shap.Explainer")
    def test_explain_with_shap_model_interface(self, mock_explainer_class):
        """Test that model interface requirements are met"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        # Model should be passed as-is to the explainer
        explain_with_shap(self.model, self.X, nsamples=10)

        # Check that the exact model object was passed
        call_args = mock_explainer_class.call_args[0]
        assert call_args[0] is self.model
        assert np.array_equal(call_args[1], self.X)


if __name__ == "__main__":
    pytest.main([__file__])
