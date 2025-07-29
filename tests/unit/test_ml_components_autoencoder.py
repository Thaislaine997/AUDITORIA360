"""
Unit tests for ML Autoencoder component
Day 1-2: Implementation of ML components testing
"""

import os
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mock tensorflow if not available
try:
    pass
except ImportError:
    sys.modules["tensorflow"] = MagicMock()
    sys.modules["tensorflow.keras"] = MagicMock()
    sys.modules["tensorflow.keras.layers"] = MagicMock()
    sys.modules["tensorflow.keras.Model"] = MagicMock()

from services.ml.components.autoencoder import (
    build_autoencoder,
    predict_reconstruction_error,
    train_autoencoder,
)


class TestAutoencoder:
    """Test suite for autoencoder ML component"""

    def test_build_autoencoder_creates_model(self):
        """Test that build_autoencoder creates a valid model"""
        input_dim = 10
        model = build_autoencoder(input_dim)

        assert model is not None
        assert hasattr(model, "fit")
        assert hasattr(model, "predict")

    def test_build_autoencoder_input_shape(self):
        """Test that model has correct input shape"""
        input_dim = 5
        model = build_autoencoder(input_dim)

        # Check input shape
        assert model.input_shape == (None, input_dim)

    def test_build_autoencoder_different_dimensions(self):
        """Test autoencoder with different input dimensions"""
        dimensions = [1, 5, 10, 20, 50]

        for dim in dimensions:
            model = build_autoencoder(dim)
            assert model.input_shape == (None, dim)
            assert model.output_shape == (None, dim)

    @patch("services.ml.components.autoencoder.keras.Model.fit")
    def test_train_autoencoder_calls_fit(self, mock_fit):
        """Test that train_autoencoder calls the fit method"""
        input_dim = 10
        model = build_autoencoder(input_dim)
        X = np.random.rand(100, input_dim)

        train_autoencoder(model, X, epochs=5, batch_size=16)

        mock_fit.assert_called_once()
        call_args = mock_fit.call_args

        # Check that X is passed as both input and target
        assert np.array_equal(call_args[0][0], X)  # input
        assert np.array_equal(call_args[0][1], X)  # target

    def test_train_autoencoder_returns_model(self):
        """Test that train_autoencoder returns the model"""
        input_dim = 5
        model = build_autoencoder(input_dim)
        X = np.random.rand(50, input_dim)

        trained_model = train_autoencoder(model, X, epochs=1)

        assert trained_model is model

    @patch("services.ml.components.autoencoder.keras.Model.predict")
    def test_predict_reconstruction_error_shape(self, mock_predict):
        """Test reconstruction error prediction shape"""
        input_dim = 8
        n_samples = 20
        X = np.random.rand(n_samples, input_dim)

        # Mock prediction to return slightly different values
        mock_predict.return_value = X + np.random.rand(*X.shape) * 0.1

        model = build_autoencoder(input_dim)
        errors = predict_reconstruction_error(model, X)

        assert errors.shape == (n_samples,)
        assert len(errors) == n_samples

    def test_predict_reconstruction_error_values(self):
        """Test that reconstruction error values are reasonable"""
        input_dim = 4
        X = np.random.rand(10, input_dim)

        model = build_autoencoder(input_dim)

        # Train very briefly to get some prediction capability
        train_autoencoder(model, X, epochs=1)

        errors = predict_reconstruction_error(model, X)

        # Errors should be non-negative
        assert np.all(errors >= 0)

    def test_autoencoder_pipeline_integration(self):
        """Test complete autoencoder pipeline"""
        input_dim = 6
        n_samples = 30
        X = np.random.rand(n_samples, input_dim)

        # Build model
        model = build_autoencoder(input_dim)

        # Train model
        trained_model = train_autoencoder(model, X, epochs=2, batch_size=10)

        # Predict errors
        errors = predict_reconstruction_error(trained_model, X)

        assert len(errors) == n_samples
        assert np.all(errors >= 0)
        assert np.all(np.isfinite(errors))

    def test_autoencoder_with_zeros(self):
        """Test autoencoder handles zero input"""
        input_dim = 5
        X = np.zeros((10, input_dim))

        model = build_autoencoder(input_dim)
        train_autoencoder(model, X, epochs=1)
        errors = predict_reconstruction_error(model, X)

        assert len(errors) == 10
        assert np.all(errors >= 0)

    def test_autoencoder_with_extreme_values(self):
        """Test autoencoder handles extreme values"""
        input_dim = 3
        X = np.array([[1000, -1000, 0], [0.001, -0.001, 999]])

        model = build_autoencoder(input_dim)
        train_autoencoder(model, X, epochs=1)
        errors = predict_reconstruction_error(model, X)

        assert len(errors) == 2
        assert np.all(errors >= 0)
        assert np.all(np.isfinite(errors))


if __name__ == "__main__":
    pytest.main([__file__])
