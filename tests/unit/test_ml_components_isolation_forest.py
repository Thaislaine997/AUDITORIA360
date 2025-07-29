"""
Unit tests for ML Isolation Forest component
Day 1-2: Implementation of ML components testing
"""

import os
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.ml.components.isolation_forest import (
    predict_anomalies,
    train_isolation_forest,
)


class TestIsolationForest:
    """Test suite for isolation forest ML component"""

    def setup_method(self):
        """Setup test data for each test"""
        np.random.seed(42)
        self.normal_data = np.random.rand(100, 5)
        self.anomaly_data = np.random.rand(10, 5) * 10  # More extreme values
        self.test_data = np.vstack([self.normal_data, self.anomaly_data])

    def test_train_isolation_forest_returns_model(self):
        """Test that train_isolation_forest returns a model object"""
        model = train_isolation_forest(self.normal_data)

        assert model is not None
        assert hasattr(model, "predict")
        assert hasattr(model, "fit")

    def test_train_isolation_forest_with_contamination(self):
        """Test isolation forest with different contamination values"""
        contamination_values = [0.01, 0.05, 0.1, 0.2]

        for contamination in contamination_values:
            model = train_isolation_forest(
                self.normal_data, contamination=contamination
            )
            assert model is not None

    def test_train_isolation_forest_default_contamination(self):
        """Test that default contamination is used correctly"""
        model = train_isolation_forest(self.normal_data)

        # Check that model was created (contamination parameter was accepted)
        assert model is not None

    @patch("services.ml.components.isolation_forest.IsolationForest")
    def test_train_isolation_forest_parameters(self, mock_isolation_forest):
        """Test that isolation forest is initialized with correct parameters"""
        mock_model = MagicMock()
        mock_isolation_forest.return_value = mock_model

        contamination = 0.1
        train_isolation_forest(self.normal_data, contamination=contamination)

        # Check that IsolationForest was called with correct parameters
        mock_isolation_forest.assert_called_once_with(
            contamination=contamination, random_state=42
        )
        mock_model.fit.assert_called_once_with(self.normal_data)

    def test_predict_anomalies_returns_predictions(self):
        """Test that predict_anomalies returns predictions"""
        model = train_isolation_forest(self.normal_data)
        predictions = predict_anomalies(model, self.test_data)

        assert predictions is not None
        assert len(predictions) == len(self.test_data)

    def test_predict_anomalies_values(self):
        """Test that predictions contain only valid values (-1 or 1)"""
        model = train_isolation_forest(self.normal_data)
        predictions = predict_anomalies(model, self.test_data)

        # All predictions should be either -1 (anomaly) or 1 (normal)
        unique_values = np.unique(predictions)
        assert all(val in [-1, 1] for val in unique_values)

    def test_predict_anomalies_normal_data(self):
        """Test predictions on normal data (should mostly be 1)"""
        model = train_isolation_forest(self.normal_data, contamination=0.05)
        predictions = predict_anomalies(model, self.normal_data)

        # Most predictions should be normal (1)
        normal_count = np.sum(predictions == 1)
        total_count = len(predictions)

        # At least 90% should be classified as normal
        assert normal_count / total_count >= 0.9

    def test_predict_anomalies_mixed_data(self):
        """Test predictions on mixed normal and anomalous data"""
        # Create clearly anomalous data
        extreme_anomalies = np.random.rand(5, 5) * 100
        mixed_data = np.vstack([self.normal_data[:20], extreme_anomalies])

        model = train_isolation_forest(self.normal_data, contamination=0.1)
        predictions = predict_anomalies(model, mixed_data)

        # Should detect some anomalies
        anomaly_count = np.sum(predictions == -1)
        assert anomaly_count > 0

    def test_isolation_forest_with_single_sample(self):
        """Test isolation forest with single sample"""
        single_sample = self.normal_data[:1]

        model = train_isolation_forest(single_sample)
        prediction = predict_anomalies(model, single_sample)

        assert len(prediction) == 1
        assert prediction[0] in [-1, 1]

    def test_isolation_forest_with_identical_data(self):
        """Test isolation forest with identical data points"""
        identical_data = np.ones((50, 3))

        model = train_isolation_forest(identical_data)
        predictions = predict_anomalies(model, identical_data)

        assert len(predictions) == len(identical_data)
        assert all(pred in [-1, 1] for pred in predictions)

    def test_isolation_forest_different_dimensions(self):
        """Test isolation forest with different data dimensions"""
        dimensions = [1, 3, 5, 10, 20]

        for dim in dimensions:
            data = np.random.rand(50, dim)
            model = train_isolation_forest(data)
            predictions = predict_anomalies(model, data)

            assert len(predictions) == len(data)
            assert all(pred in [-1, 1] for pred in predictions)

    def test_isolation_forest_pipeline_integration(self):
        """Test complete isolation forest pipeline"""
        # Train on normal data
        model = train_isolation_forest(self.normal_data, contamination=0.1)

        # Test on mixed data
        test_predictions = predict_anomalies(model, self.test_data)

        # Verify output format
        assert len(test_predictions) == len(self.test_data)
        assert all(pred in [-1, 1] for pred in test_predictions)

        # Should detect some anomalies in the extreme data
        anomaly_indices = np.where(test_predictions == -1)[0]
        assert len(anomaly_indices) > 0

    def test_isolation_forest_reproducibility(self):
        """Test that isolation forest produces consistent results"""
        model1 = train_isolation_forest(self.normal_data, contamination=0.05)
        model2 = train_isolation_forest(self.normal_data, contamination=0.05)

        pred1 = predict_anomalies(model1, self.test_data)
        pred2 = predict_anomalies(model2, self.test_data)

        # Results should be identical due to random_state=42
        assert np.array_equal(pred1, pred2)

    def test_isolation_forest_with_extreme_contamination(self):
        """Test isolation forest with extreme contamination values"""
        # Very low contamination
        model_low = train_isolation_forest(self.normal_data, contamination=0.001)
        pred_low = predict_anomalies(model_low, self.normal_data)

        # Very high contamination
        model_high = train_isolation_forest(self.normal_data, contamination=0.5)
        pred_high = predict_anomalies(model_high, self.normal_data)

        # Both should work
        assert len(pred_low) == len(self.normal_data)
        assert len(pred_high) == len(self.normal_data)

        # High contamination should detect more anomalies
        anomalies_low = np.sum(pred_low == -1)
        anomalies_high = np.sum(pred_high == -1)
        assert anomalies_high >= anomalies_low


if __name__ == "__main__":
    pytest.main([__file__])
