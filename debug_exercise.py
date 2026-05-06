#!/usr/bin/env python3
"""
Debug Exercise 2: Bug Injection and Debugging Practice

This script demonstrates how to debug the pipeline when the amount column is missing.
"""

import pandas as pd
import logging
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from load import load_data
from transform import clean_data, aggregate_by_account
from fraud import detect_fraud, get_fraud_summary

def setup_debug_logging():
    """Configure detailed logging for debugging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def debug_pipeline_with_buggy_data():
    """
    Debug the pipeline with buggy data (missing amount column).
    """
    print("=" * 60)
    print("DEBUG EXERCISE 2: Bug Injection and Debugging")
    print("=" * 60)
    
    try:
        # Step 1: Load the buggy data
        print("\n1. Loading buggy data...")
        df = load_data("data/transactions_buggy.csv")
        print(f"Loaded data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("First few rows:")
        print(df.head())
        
        # Step 2: Try to clean the data (this should fail)
        print("\n2. Attempting to clean data...")
        try:
            clean_df = clean_data(df)
            print("Data cleaning succeeded (unexpected!)")
        except Exception as e:
            print(f"ERROR during data cleaning: {e}")
            print("This is the expected error due to missing 'amount' column")
            
        # Step 3: Debug the issue
        print("\n3. Debugging the issue...")
        print("Checking for required columns:")
        required_columns = ['transaction_id', 'account_id', 'amount', 'transaction_type', 'transaction_date']
        for col in required_columns:
            if col in df.columns:
                print(f"✓ {col}: Present")
            else:
                print(f"✗ {col}: MISSING")
        
        # Step 4: Fix the data
        print("\n4. Fixing the data...")
        # Add a default amount column
        df['amount'] = 100.0  # Default amount for demonstration
        print("Added default amount column with value 100.0")
        print(f"Updated columns: {list(df.columns)}")
        
        # Step 5: Try the pipeline again
        print("\n5. Running pipeline with fixed data...")
        clean_df = clean_data(df)
        print("✓ Data cleaning succeeded")
        
        fraud_df = detect_fraud(clean_df)
        print("✓ Fraud detection succeeded")
        
        agg_df = aggregate_by_account(clean_df)
        print("✓ Aggregation succeeded")
        
        print("\n6. Results:")
        print(f"Cleaned data shape: {clean_df.shape}")
        print(f"Fraud detection flagged {fraud_df['is_fraud'].sum()} transactions")
        print(f"Aggregation results for {len(agg_df)} accounts")
        
        print("\n" + "=" * 60)
        print("DEBUG EXERCISE COMPLETED SUCCESSFULLY!")
        print("Key learnings:")
        print("- Always validate input data schema")
        print("- Use logging to trace execution flow")
        print("- Add data validation checks in pipeline")
        print("- Handle missing columns gracefully")
        print("=" * 60)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

def demonstrate_data_validation():
    """
    Demonstrate adding data validation to prevent such bugs.
    """
    print("\n" + "=" * 60)
    print("DEMONSTRATION: Adding Data Validation")
    print("=" * 60)
    
    def validate_transaction_data(df):
        """
        Validate transaction data schema.
        
        Args:
            df (pd.DataFrame): Transaction data to validate
            
        Returns:
            bool: True if valid, raises Exception if invalid
        """
        required_columns = ['transaction_id', 'account_id', 'amount', 'transaction_type', 'transaction_date']
        
        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for empty data
        if df.empty:
            raise ValueError("Dataframe is empty")
        
        # Check data types
        if not pd.api.types.is_numeric_dtype(df['amount']):
            raise ValueError("Amount column must be numeric")
        
        print("✓ Data validation passed")
        return True
    
    # Test validation with good data
    print("\n1. Testing validation with good data:")
    good_data = pd.DataFrame({
        'transaction_id': [1, 2],
        'account_id': [1001, 1002],
        'amount': [100.0, 200.0],
        'transaction_type': ['credit', 'debit'],
        'transaction_date': ['2024-01-01', '2024-01-02']
    })
    
    try:
        validate_transaction_data(good_data)
        print("Good data validation: PASSED")
    except Exception as e:
        print(f"Good data validation: FAILED - {e}")
    
    # Test validation with bad data
    print("\n2. Testing validation with bad data (missing amount):")
    bad_data = pd.DataFrame({
        'transaction_id': [1, 2],
        'account_id': [1001, 1002],
        'transaction_type': ['credit', 'debit'],
        'transaction_date': ['2024-01-01', '2024-01-02']
    })
    
    try:
        validate_transaction_data(bad_data)
        print("Bad data validation: PASSED (unexpected!)")
    except Exception as e:
        print(f"Bad data validation: FAILED as expected - {e}")

if __name__ == "__main__":
    setup_debug_logging()
    
    # Run the main debug exercise
    debug_pipeline_with_buggy_data()
    
    # Demonstrate data validation
    demonstrate_data_validation()
