"""
Unit tests for ML Bias Detection component
Day 1-2: Implementation of ML components testing
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.ml.components.bias_detection import detect_bias


class TestBiasDetection:
    """Test suite for bias detection ML component"""
    
    def setup_method(self):
        """Setup test data for each test"""
        # Create sample data with groups and targets
        np.random.seed(42)
        n_samples = 100
        
        self.data = pd.DataFrame({
            'feature1': np.random.rand(n_samples),
            'feature2': np.random.rand(n_samples),
            'group': np.random.choice(['A', 'B', 'C'], n_samples),
            'target': np.random.choice([0, 1], n_samples)
        })
        
        # Create a mock model that returns predictions matching group sizes
        self.mock_model = MagicMock()
        
        def side_effect_predict(X):
            return np.random.choice([0, 1], len(X))
        
        self.mock_model.predict.side_effect = side_effect_predict
    
    def test_detect_bias_returns_dict(self):
        """Test that detect_bias returns a dictionary"""
        result = detect_bias(
            self.mock_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        assert isinstance(result, dict)
        
    def test_detect_bias_without_group_col_returns_error(self):
        """Test that detect_bias returns error when group_col is None"""
        result = detect_bias(
            self.mock_model, 
            self.data, 
            target_col='target', 
            group_col=None
        )
        
        assert "error" in result
        assert result["error"] == "group_col não informado"
        
    def test_detect_bias_contains_all_groups(self):
        """Test that bias report contains all groups"""
        result = detect_bias(
            self.mock_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        expected_groups = set(self.data['group'].unique())
        result_groups = set(result.keys())
        
        assert expected_groups.issubset(result_groups)
        
    def test_detect_bias_accuracy_values_valid(self):
        """Test that accuracy values are between 0 and 1"""
        result = detect_bias(
            self.mock_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        for group, accuracy in result.items():
            if group != "error":  # Skip error messages
                assert 0 <= accuracy <= 1
                
    def test_detect_bias_with_perfect_predictions(self):
        """Test bias detection with perfect model predictions"""
        # Create model that predicts perfectly for each group
        perfect_model = MagicMock()
        
        def perfect_predict(X):
            # Find corresponding targets for the features
            indices = X.index if hasattr(X, 'index') else range(len(X))
            return self.data.loc[indices, 'target'].values
        
        perfect_model.predict.side_effect = perfect_predict
        
        result = detect_bias(
            perfect_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        # All groups should have accuracy = 1.0
        for group, accuracy in result.items():
            assert accuracy == 1.0
            
    def test_detect_bias_with_random_predictions(self):
        """Test bias detection with random model predictions"""
        # Create model with random predictions that match input size
        random_model = MagicMock()
        
        def random_predict(X):
            np.random.seed(123)  # For reproducible test
            return np.random.choice([0, 1], len(X))
        
        random_model.predict.side_effect = random_predict
        
        result = detect_bias(
            random_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        # All accuracies should be reasonable (between 0 and 1)
        for group, accuracy in result.items():
            assert 0 <= accuracy <= 1
            
    def test_detect_bias_model_called_correctly(self):
        """Test that the model predict method is called correctly"""
        detect_bias(
            self.mock_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        # Model should be called with features (excluding target)
        call_args = self.mock_model.predict.call_args_list
        
        # Should be called at least once for each group
        assert len(call_args) >= len(self.data['group'].unique())
        
    def test_detect_bias_with_single_group(self):
        """Test bias detection with data containing only one group"""
        single_group_data = self.data.copy()
        single_group_data['group'] = 'A'  # All samples belong to group A
        
        result = detect_bias(
            self.mock_model, 
            single_group_data, 
            target_col='target', 
            group_col='group'
        )
        
        assert 'A' in result
        assert len(result) == 1
        
    def test_detect_bias_with_empty_groups(self):
        """Test bias detection handles empty data gracefully"""
        empty_data = pd.DataFrame({
            'feature1': [],
            'feature2': [],
            'group': [],
            'target': []
        })
        
        result = detect_bias(
            self.mock_model, 
            empty_data, 
            target_col='target', 
            group_col='group'
        )
        
        # Should return empty dict or handle gracefully
        assert isinstance(result, dict)
        
    def test_detect_bias_with_different_target_col(self):
        """Test bias detection with different target column name"""
        data_custom = self.data.copy()
        data_custom.rename(columns={'target': 'custom_target'}, inplace=True)
        
        result = detect_bias(
            self.mock_model, 
            data_custom, 
            target_col='custom_target', 
            group_col='group'
        )
        
        assert isinstance(result, dict)
        assert len(result) > 0
        
    def test_detect_bias_with_numeric_groups(self):
        """Test bias detection with numeric group labels"""
        numeric_data = self.data.copy()
        numeric_data['group'] = np.random.choice([1, 2, 3], len(self.data))
        
        result = detect_bias(
            self.mock_model, 
            numeric_data, 
            target_col='target', 
            group_col='group'
        )
        
        # Results should contain string representations of numeric groups
        for group_key in result.keys():
            assert isinstance(group_key, str)
            
    @patch('services.ml.components.bias_detection.logging')
    def test_detect_bias_logging(self, mock_logging):
        """Test that bias detection logs appropriately"""
        detect_bias(
            self.mock_model, 
            self.data, 
            target_col='target', 
            group_col='group'
        )
        
        # Should log info for each group
        assert mock_logging.info.call_count >= len(self.data['group'].unique())
        
    def test_detect_bias_handles_model_exceptions(self):
        """Test that bias detection handles model prediction exceptions"""
        failing_model = MagicMock()
        failing_model.predict.side_effect = Exception("Model prediction failed")
        
        with pytest.raises(Exception):
            detect_bias(
                failing_model, 
                self.data, 
                target_col='target', 
                group_col='group'
            )


if __name__ == "__main__":
    pytest.main([__file__])