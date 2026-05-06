import pytest
import pandas as pd
import os
import sys
from pathlib import Path

# Add src directory to Python path for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from load import load_data
from transform import clean_data, aggregate_by_account
from fraud import detect_fraud, get_fraud_summary
from save import save_data, save_pipeline_outputs

@pytest.fixture
def sample_data():
    """Create sample transaction data for testing."""
    return pd.DataFrame({
        'transaction_id': [1, 2, 3, 4, 4],
        'account_id': [1001, 1002, 1001, 1003, 1003],
        'amount': [500.0, 200.0, None, 1000.0, 1000.0],
        'transaction_type': ['credit', 'debit', 'credit', 'debit', 'debit'],
        'transaction_date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02', '2024-01-02']
    })

@pytest.fixture
def temp_csv(tmp_path, sample_data):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test_transactions.csv"
    sample_data.to_csv(csv_file, index=False)
    return csv_file

class TestLoadData:
    """Test cases for data loading functionality."""
    
    def test_load_data_success(self, temp_csv):
        """Test successful data loading."""
        df = load_data(str(temp_csv))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert list(df.columns) == ['transaction_id', 'account_id', 'amount', 'transaction_type', 'transaction_date']
    
    def test_load_file_not_found(self):
        """Test loading non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_data("nonexistent_file.csv")
    
    def test_load_empty_file(self, tmp_path):
        """Test loading empty CSV file."""
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("")
        with pytest.raises(pd.errors.EmptyDataError):
            load_data(str(empty_file))

class TestTransformData:
    """Test cases for data transformation functionality."""
    
    def test_clean_data_removes_duplicates(self, sample_data):
        """Test that duplicates are removed."""
        cleaned = clean_data(sample_data)
        assert len(cleaned) == 4  # One duplicate removed
    
    def test_clean_data_handles_nulls(self, sample_data):
        """Test that null values are handled."""
        cleaned = clean_data(sample_data)
        assert cleaned['amount'].isnull().sum() == 0  # No nulls remaining
        assert cleaned['amount'].iloc[2] == 0  # Null replaced with 0
    
    def test_clean_data_data_types(self, sample_data):
        """Test data type conversions."""
        cleaned = clean_data(sample_data)
        assert pd.api.types.is_numeric_dtype(cleaned['amount'])
        assert pd.api.types.is_datetime64_any_dtype(cleaned['transaction_date'])
    
    def test_aggregate_by_account(self, sample_data):
        """Test account aggregation."""
        cleaned = clean_data(sample_data)
        agg = aggregate_by_account(cleaned)
        
        assert len(agg) == 3  # 3 unique accounts
        assert list(agg.columns) == ['account_id', 'total_amount']
        
        # Check specific aggregations
        account_1001 = agg[agg['account_id'] == 1001]['total_amount'].iloc[0]
        assert account_1001 == 500.0  # 500 + 0 (null filled)

class TestFraudDetection:
    """Test cases for fraud detection functionality."""
    
    def test_detect_fraud_default_threshold(self, sample_data):
        """Test fraud detection with default threshold."""
        cleaned = clean_data(sample_data)
        fraud_df = detect_fraud(cleaned)
        
        assert 'is_fraud' in fraud_df.columns
        assert fraud_df['is_fraud'].sum() == 1  # One transaction > 800 (after removing duplicate)
        
        # Check specific transactions
        high_value = fraud_df[fraud_df['amount'] > 800]
        assert high_value['is_fraud'].all()
    
    def test_detect_fraud_custom_threshold(self, sample_data):
        """Test fraud detection with custom threshold."""
        cleaned = clean_data(sample_data)
        fraud_df = detect_fraud(cleaned, threshold=600)
        
        assert fraud_df['is_fraud'].sum() == 1  # One transaction > 600 (after removing duplicate)
    
    def test_get_fraud_summary(self, sample_data):
        """Test fraud summary generation."""
        cleaned = clean_data(sample_data)
        fraud_df = detect_fraud(cleaned)
        summary = get_fraud_summary(fraud_df)
        
        assert len(summary) == 3  # 3 unique accounts
        expected_columns = ['account_id', 'fraud_transactions', 'total_transactions', 'total_amount', 'fraud_percentage']
        assert all(col in summary.columns for col in expected_columns)

class TestSaveData:
    """Test cases for data saving functionality."""
    
    def test_save_data_success(self, sample_data, tmp_path):
        """Test successful data saving."""
        output_file = tmp_path / "test_output.csv"
        save_data(sample_data, str(output_file), "test data")
        
        assert output_file.exists()
        
        # Verify saved data
        loaded = pd.read_csv(output_file)
        assert len(loaded) == len(sample_data)
        assert list(loaded.columns) == list(sample_data.columns)
    
    def test_save_pipeline_outputs(self, sample_data, tmp_path):
        """Test saving all pipeline outputs."""
        cleaned = clean_data(sample_data)
        agg = aggregate_by_account(cleaned)
        fraud_df = detect_fraud(cleaned)
        summary = get_fraud_summary(fraud_df)
        
        output_dir = tmp_path / "outputs"
        save_pipeline_outputs(cleaned, agg, fraud_df, summary, str(output_dir))
        
        # Check all output files exist
        expected_files = [
            "clean_transactions.csv",
            "account_aggregations.csv", 
            "fraud_detection.csv",
            "fraud_summary.csv"
        ]
        
        for file in expected_files:
            assert (output_dir / file).exists()

class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_full_pipeline_integration(self, temp_csv, tmp_path):
        """Test the complete pipeline integration."""
        # Load data
        df = load_data(str(temp_csv))
        assert len(df) > 0
        
        # Clean data
        clean_df = clean_data(df)
        assert len(clean_df) <= len(df)
        
        # Detect fraud
        fraud_df = detect_fraud(clean_df)
        assert 'is_fraud' in fraud_df.columns
        
        # Generate summary
        summary = get_fraud_summary(fraud_df)
        assert len(summary) > 0
        
        # Aggregate
        agg = aggregate_by_account(clean_df)
        assert len(agg) > 0
        
        # Save outputs
        output_dir = tmp_path / "integration_test"
        save_pipeline_outputs(clean_df, agg, fraud_df, summary, str(output_dir))
        
        # Verify outputs
        assert (output_dir / "clean_transactions.csv").exists()
        assert (output_dir / "account_aggregations.csv").exists()
        assert (output_dir / "fraud_detection.csv").exists()
        assert (output_dir / "fraud_summary.csv").exists()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
