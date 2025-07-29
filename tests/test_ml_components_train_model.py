"""
Unit tests for ML Train Model component
Day 1-2: Implementation of ML components testing
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.ml.components.train_model import train_model


class TestTrainModel:
    """Test suite for train model ML component"""
    
    def setup_method(self):
        """Setup test data for each test"""
        np.random.seed(42)
        
        # Create sample training data
        self.data = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'feature3': np.random.rand(100),
            'target': np.random.choice([0, 1], 100)
        })
    
    @patch('services.ml.components.train_model.RandomForestClassifier')
    @patch('services.ml.components.train_model.logging')
    def test_train_model_creates_classifier(self, mock_logging, mock_rf_class):
        """Test that train_model creates a RandomForestClassifier"""
        mock_model = MagicMock()
        mock_rf_class.return_value = mock_model
        
        result = train_model(self.data, target_col='target')
        
        # Check that RandomForestClassifier was created with correct parameters
        mock_rf_class.assert_called_once_with(n_estimators=100, random_state=42)
        assert result == mock_model
    
    @patch('services.ml.components.train_model.RandomForestClassifier')
    @patch('services.ml.components.train_model.logging')
    def test_train_model_fits_with_correct_data(self, mock_logging, mock_rf_class):
        """Test that train_model fits the model with correct X and y"""
        mock_model = MagicMock()
        mock_rf_class.return_value = mock_model
        
        train_model(self.data, target_col='target')
        
        # Check that fit was called
        mock_model.fit.assert_called_once()
        
        # Check the arguments passed to fit
        call_args = mock_model.fit.call_args[0]
        X, y = call_args
        
        # X should be features (excluding target)
        expected_features = ['feature1', 'feature2', 'feature3']
        assert list(X.columns) == expected_features
        
        # y should be the target column
        assert np.array_equal(y.values, self.data['target'].values)
    
    @patch('services.ml.components.train_model.RandomForestClassifier')
    @patch('services.ml.components.train_model.logging')
    def test_train_model_logging_messages(self, mock_logging, mock_rf_class):
        """Test that train_model logs appropriate messages"""
        mock_model = MagicMock()
        mock_rf_class.return_value = mock_model
        
        train_model(self.data, target_col='target')
        
        # Check logging calls
        assert mock_logging.info.call_count == 2
        
        # Check log messages
        log_calls = mock_logging.info.call_args_list
        assert f"Iniciando treinamento com {len(self.data)} amostras..." in str(log_calls[0])
        assert "Treinamento concluído." in str(log_calls[1])
    
    def test_train_model_returns_model_object(self):
        """Test that train_model returns a model with required methods"""
        model = train_model(self.data, target_col='target')
        
        assert model is not None
        assert hasattr(model, 'fit')
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')
    
    def test_train_model_with_custom_target_col(self):
        """Test train_model with custom target column name"""
        custom_data = self.data.copy()
        custom_data.rename(columns={'target': 'custom_target'}, inplace=True)
        
        model = train_model(custom_data, target_col='custom_target')
        
        assert model is not None
        assert hasattr(model, 'predict')
    
    def test_train_model_prediction_capability(self):
        """Test that trained model can make predictions"""
        model = train_model(self.data, target_col='target')
        
        # Test prediction on training data
        X_test = self.data.drop(columns=['target'])
        predictions = model.predict(X_test)
        
        assert len(predictions) == len(X_test)
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_train_model_with_small_dataset(self):
        """Test train_model with small dataset"""
        small_data = self.data.iloc[:5]
        
        model = train_model(small_data, target_col='target')
        
        assert model is not None
        assert hasattr(model, 'predict')
    
    def test_train_model_with_single_feature(self):
        """Test train_model with single feature"""
        single_feature_data = pd.DataFrame({
            'feature1': np.random.rand(50),
            'target': np.random.choice([0, 1], 50)
        })
        
        model = train_model(single_feature_data, target_col='target')
        
        assert model is not None
        
        # Test prediction
        X_test = single_feature_data.drop(columns=['target'])
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
    
    def test_train_model_with_many_features(self):
        """Test train_model with many features"""
        many_features_data = pd.DataFrame(
            np.random.rand(100, 20),
            columns=[f'feature_{i}' for i in range(20)]
        )
        many_features_data['target'] = np.random.choice([0, 1], 100)
        
        model = train_model(many_features_data, target_col='target')
        
        assert model is not None
        
        # Test prediction
        X_test = many_features_data.drop(columns=['target'])
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
    
    def test_train_model_with_multiclass_target(self):
        """Test train_model with multiclass target"""
        multiclass_data = self.data.copy()
        multiclass_data['target'] = np.random.choice([0, 1, 2, 3], 100)
        
        model = train_model(multiclass_data, target_col='target')
        
        assert model is not None
        
        # Test prediction
        X_test = multiclass_data.drop(columns=['target'])
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
        assert all(pred in [0, 1, 2, 3] for pred in predictions)
    
    def test_train_model_handles_missing_target_column(self):
        """Test that train_model handles missing target column"""
        data_no_target = self.data.drop(columns=['target'])
        
        with pytest.raises(KeyError):
            train_model(data_no_target, target_col='target')
    
    def test_train_model_reproducibility(self):
        """Test that train_model produces consistent results with random_state"""
        model1 = train_model(self.data, target_col='target')
        model2 = train_model(self.data, target_col='target')
        
        X_test = self.data.drop(columns=['target'])
        pred1 = model1.predict(X_test)
        pred2 = model2.predict(X_test)
        
        # Results should be identical due to random_state=42
        assert np.array_equal(pred1, pred2)
    
    def test_train_model_with_string_features(self):
        """Test train_model behavior with string features (should handle or fail gracefully)"""
        string_data = pd.DataFrame({
            'feature1': ['a', 'b', 'c'] * 33 + ['a'],
            'feature2': np.random.rand(100),
            'target': np.random.choice([0, 1], 100)
        })
        
        # This may fail or require preprocessing - test the behavior
        try:
            model = train_model(string_data, target_col='target')
            # If it succeeds, test basic functionality
            assert model is not None
        except (ValueError, TypeError):
            # It's acceptable for the function to fail with string features
            pass
    
    def test_train_model_feature_importance(self):
        """Test that trained model has feature importance"""
        model = train_model(self.data, target_col='target')
        
        # RandomForest should have feature_importances_
        assert hasattr(model, 'feature_importances_')
        
        importances = model.feature_importances_
        assert len(importances) == 3  # 3 features
        assert all(imp >= 0 for imp in importances)
        assert abs(sum(importances) - 1.0) < 1e-10  # Should sum to 1
    
    @patch('services.ml.components.train_model.RandomForestClassifier')
    def test_train_model_handles_fit_exception(self, mock_rf_class):
        """Test that train_model handles fit exceptions"""
        mock_model = MagicMock()
        mock_model.fit.side_effect = Exception("Fit failed")
        mock_rf_class.return_value = mock_model
        
        with pytest.raises(Exception):
            train_model(self.data, target_col='target')
    
    def test_train_model_with_boolean_target(self):
        """Test train_model with boolean target values"""
        boolean_data = self.data.copy()
        boolean_data['target'] = np.random.choice([True, False], 100)
        
        model = train_model(boolean_data, target_col='target')
        
        assert model is not None
        
        # Test prediction
        X_test = boolean_data.drop(columns=['target'])
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
    
    def test_train_model_probability_predictions(self):
        """Test that trained model can predict probabilities"""
        model = train_model(self.data, target_col='target')
        
        X_test = self.data.drop(columns=['target'])
        probabilities = model.predict_proba(X_test)
        
        assert probabilities.shape[0] == len(X_test)
        assert probabilities.shape[1] == 2  # Binary classification
        
        # Probabilities should sum to 1 for each sample
        prob_sums = np.sum(probabilities, axis=1)
        assert np.allclose(prob_sums, 1.0)


if __name__ == "__main__":
    pytest.main([__file__])