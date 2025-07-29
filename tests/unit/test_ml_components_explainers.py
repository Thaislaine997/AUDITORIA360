"""
Unit tests for ML Explainers component
Day 1-2: Implementation of ML components testing
"""

import os
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mock shap if not available
try:
    pass
except ImportError:
    sys.modules["shap"] = MagicMock()

from services.ml.components.explainers import explain_model


class TestExplainers:
    """Test suite for explainers ML component"""

    def setup_method(self):
        """Setup test data for each test"""
        np.random.seed(42)
        self.data = pd.DataFrame(
            {
                "feature1": np.random.rand(100),
                "feature2": np.random.rand(100),
                "feature3": np.random.rand(100),
                "target": np.random.choice([0, 1], 100),
            }
        )

        self.model = MagicMock()
        self.model.predict.return_value = np.random.choice([0, 1], 100)

    @patch("services.ml.components.explainers.shap.Explainer")
    @patch("services.ml.components.explainers.logging")
    def test_explain_model_creates_explainer(self, mock_logging, mock_explainer_class):
        """Test that explain_model creates a SHAP explainer"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()  # Mock SHAP values

        explain_model(self.model, self.data, nsamples=10)

        # Check that explainer was created with correct arguments
        mock_explainer_class.assert_called_once_with(self.model, self.data)

    @patch("services.ml.components.explainers.shap.Explainer")
    @patch("services.ml.components.explainers.logging")
    def test_explain_model_calls_explainer(self, mock_logging, mock_explainer_class):
        """Test that explain_model calls the explainer with correct data"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_shap_values = MagicMock()
        mock_explainer.return_value = mock_shap_values

        nsamples = 50
        result = explain_model(self.model, self.data, nsamples=nsamples)

        # Check that explainer was called with correct subset of data
        mock_explainer.assert_called_once_with(self.data.iloc[:nsamples])
        assert result == mock_shap_values

    @patch("services.ml.components.explainers.shap.Explainer")
    @patch("services.ml.components.explainers.logging")
    def test_explain_model_default_nsamples(self, mock_logging, mock_explainer_class):
        """Test explain_model with default nsamples parameter"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_model(self.model, self.data)

        # Should use default nsamples=100
        expected_data = self.data.iloc[:100]
        mock_explainer.assert_called_once_with(expected_data)

    @patch("services.ml.components.explainers.shap.Explainer")
    @patch("services.ml.components.explainers.logging")
    def test_explain_model_logging_messages(self, mock_logging, mock_explainer_class):
        """Test that explain_model logs appropriate messages"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        nsamples = 25
        explain_model(self.model, self.data, nsamples=nsamples)

        # Check logging calls
        assert mock_logging.info.call_count == 2

        # Check log messages
        log_calls = mock_logging.info.call_args_list
        assert f"Gerando explicações SHAP para {nsamples} amostras..." in str(
            log_calls[0]
        )
        assert "Explicações SHAP geradas." in str(log_calls[1])

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_returns_shap_values(self, mock_explainer_class):
        """Test that explain_model returns SHAP values"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_shap_values = MagicMock()
        mock_explainer.return_value = mock_shap_values

        result = explain_model(self.model, self.data, nsamples=10)

        assert result == mock_shap_values

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_with_small_dataset(self, mock_explainer_class):
        """Test explain_model with small dataset"""
        small_data = self.data.iloc[:5]  # Only 5 samples

        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_model(self.model, small_data, nsamples=10)

        # Should use all available data (5 samples) since nsamples > data size
        mock_explainer.assert_called_once_with(small_data.iloc[:10])

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_with_zero_nsamples(self, mock_explainer_class):
        """Test explain_model with zero nsamples"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_model(self.model, self.data, nsamples=0)

        # Should use empty dataframe
        expected_data = self.data.iloc[:0]
        mock_explainer.assert_called_once_with(expected_data)

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_with_single_feature(self, mock_explainer_class):
        """Test explain_model with single feature data"""
        single_feature_data = pd.DataFrame({"feature1": np.random.rand(50)})

        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_model(self.model, single_feature_data, nsamples=20)

        # Should work with single feature
        mock_explainer_class.assert_called_once_with(self.model, single_feature_data)
        mock_explainer.assert_called_once_with(single_feature_data.iloc[:20])

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_handles_explainer_exception(self, mock_explainer_class):
        """Test that explain_model handles explainer exceptions"""
        mock_explainer_class.side_effect = Exception("SHAP explainer failed")

        with pytest.raises(Exception):
            explain_model(self.model, self.data, nsamples=10)

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_handles_explanation_exception(self, mock_explainer_class):
        """Test that explain_model handles explanation generation exceptions"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.side_effect = Exception("Explanation generation failed")

        with pytest.raises(Exception):
            explain_model(self.model, self.data, nsamples=10)

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_different_data_types(self, mock_explainer_class):
        """Test explain_model with different data types"""
        mixed_data = pd.DataFrame(
            {
                "int_col": [1, 2, 3, 4, 5],
                "float_col": [1.1, 2.2, 3.3, 4.4, 5.5],
                "bool_col": [True, False, True, False, True],
            }
        )

        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        explain_model(self.model, mixed_data, nsamples=3)

        # Should handle mixed data types
        mock_explainer_class.assert_called_once_with(self.model, mixed_data)

    @patch("services.ml.components.explainers.shap.Explainer")
    def test_explain_model_large_nsamples(self, mock_explainer_class):
        """Test explain_model with nsamples larger than dataset"""
        mock_explainer = MagicMock()
        mock_explainer_class.return_value = mock_explainer
        mock_explainer.return_value = MagicMock()

        large_nsamples = len(self.data) + 50
        explain_model(self.model, self.data, nsamples=large_nsamples)

        # Should handle gracefully (pandas will return available data)
        mock_explainer.assert_called_once_with(self.data.iloc[:large_nsamples])


if __name__ == "__main__":
    pytest.main([__file__])
