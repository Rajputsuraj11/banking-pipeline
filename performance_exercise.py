#!/usr/bin/env python3
"""
Performance Exercise 3: Performance Optimization with 10k Records

This script demonstrates performance optimization techniques for large datasets.
"""

import pandas as pd
import numpy as np
import time
import logging
import sys
import os
from memory_profiler import profile

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from load import load_data
from transform import clean_data, aggregate_by_account
from fraud import detect_fraud, get_fraud_summary
from save import save_pipeline_outputs

def setup_performance_logging():
    """Configure logging for performance testing."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def generate_large_dataset(num_records: int = 10000) -> pd.DataFrame:
    """
    Generate a large transaction dataset for performance testing.
    
    Args:
        num_records (int): Number of records to generate
        
    Returns:
        pd.DataFrame: Large transaction dataset
    """
    print(f"Generating {num_records} transaction records...")
    
    np.random.seed(42)  # For reproducible results
    
    # Generate realistic transaction data
    data = {
        'transaction_id': list(range(1, num_records + 1)),
        'account_id': np.random.randint(1000, 2000, num_records).tolist(),
        'amount': np.random.uniform(10, 2000, num_records).round(2).tolist(),
        'transaction_type': np.random.choice(['credit', 'debit'], num_records, p=[0.6, 0.4]).tolist(),
        'transaction_date': pd.date_range('2024-01-01', '2024-12-31', periods=num_records).tolist(),
        'currency': np.random.choice(['USD', 'EUR', 'GBP'], num_records, p=[0.7, 0.2, 0.1]).tolist()
    }
    
    # Add some duplicates for testing
    duplicate_indices = np.random.choice(num_records, size=int(num_records * 0.05), replace=False)
    duplicate_data = {col: [data[col][i] for i in duplicate_indices] for col in data}
    
    # Add some null values for testing
    null_indices = np.random.choice(num_records, size=int(num_records * 0.02), replace=False)
    for idx in null_indices:
        data['amount'][idx] = np.nan
    
    # Combine original and duplicate data
    for col in data:
        data[col].extend(duplicate_data[col])
    
    df = pd.DataFrame(data)
    print(f"Generated dataset with {len(df)} records")
    return df

def save_large_dataset(df: pd.DataFrame, filename: str):
    """Save large dataset to CSV."""
    print(f"Saving dataset to {filename}...")
    df.to_csv(filename, index=False)
    print(f"Dataset saved successfully")

def measure_performance(func, *args, **kwargs):
    """
    Measure execution time and memory usage of a function.
    
    Args:
        func: Function to measure
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        tuple: (result, execution_time)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def run_baseline_pipeline(df: pd.DataFrame) -> dict:
    """
    Run the baseline pipeline (current implementation).
    
    Args:
        df (pd.DataFrame): Input data
        
    Returns:
        dict: Performance metrics
    """
    print("\n" + "="*50)
    print("BASELINE PIPELINE PERFORMANCE")
    print("="*50)
    
    metrics = {}
    
    # Step 1: Data cleaning
    clean_df, clean_time = measure_performance(clean_data, df)
    metrics['cleaning_time'] = clean_time
    print(f"Data cleaning: {clean_time:.3f} seconds")
    
    # Step 2: Fraud detection
    fraud_df, fraud_time = measure_performance(detect_fraud, clean_df)
    metrics['fraud_detection_time'] = fraud_time
    print(f"Fraud detection: {fraud_time:.3f} seconds")
    
    # Step 3: Aggregation
    agg_df, agg_time = measure_performance(aggregate_by_account, fraud_df)
    metrics['aggregation_time'] = agg_time
    print(f"Aggregation: {agg_time:.3f} seconds")
    
    total_time = sum(metrics.values())
    metrics['total_time'] = total_time
    print(f"Total pipeline time: {total_time:.3f} seconds")
    
    return metrics

def optimized_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimized version of data cleaning.
    
    Args:
        df (pd.DataFrame): Raw transaction data
        
    Returns:
        pd.DataFrame: Cleaned transaction data
    """
    logging.info("Starting optimized data cleaning")
    
    # Use more efficient operations
    # Remove duplicates using drop_duplicates with subset
    df_cleaned = df.drop_duplicates(subset=['transaction_id', 'account_id', 'transaction_date'])
    
    # Handle missing values more efficiently
    if 'amount' in df_cleaned.columns:
        df_cleaned['amount'] = df_cleaned['amount'].fillna(0)
    
    # Convert data types in bulk
    numeric_columns = ['amount']
    for col in numeric_columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
    
    # Convert date column
    if 'transaction_date' in df_cleaned.columns:
        df_cleaned['transaction_date'] = pd.to_datetime(df_cleaned['transaction_date'], errors='coerce')
    
    # Handle currency column
    if 'currency' in df_cleaned.columns:
        df_cleaned['currency'] = df_cleaned['currency'].fillna('USD').str.upper()
    
    logging.info(f"Optimized cleaning completed. Records: {len(df_cleaned)}")
    return df_cleaned

def optimized_aggregate_by_account(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimized version of account aggregation.
    
    Args:
        df (pd.DataFrame): Clean transaction data
        
    Returns:
        pd.DataFrame: Aggregated data by account
    """
    logging.info("Starting optimized aggregation")
    
    # Use more efficient groupby operations
    if 'currency' in df.columns:
        agg_df = df.groupby(['account_id', 'currency'], observed=True)['amount'].sum().reset_index()
        agg_df.columns = ['account_id', 'currency', 'total_amount']
    else:
        agg_df = df.groupby('account_id', observed=True)['amount'].sum().reset_index()
        agg_df.columns = ['account_id', 'total_amount']
    
    logging.info(f"Optimized aggregation completed for {len(agg_df)} groups")
    return agg_df

def run_optimized_pipeline(df: pd.DataFrame) -> dict:
    """
    Run the optimized pipeline.
    
    Args:
        df (pd.DataFrame): Input data
        
    Returns:
        dict: Performance metrics
    """
    print("\n" + "="*50)
    print("OPTIMIZED PIPELINE PERFORMANCE")
    print("="*50)
    
    metrics = {}
    
    # Step 1: Optimized data cleaning
    clean_df, clean_time = measure_performance(optimized_clean_data, df)
    metrics['cleaning_time'] = clean_time
    print(f"Optimized data cleaning: {clean_time:.3f} seconds")
    
    # Step 2: Fraud detection (already optimized)
    fraud_df, fraud_time = measure_performance(detect_fraud, clean_df)
    metrics['fraud_detection_time'] = fraud_time
    print(f"Fraud detection: {fraud_time:.3f} seconds")
    
    # Step 3: Optimized aggregation
    agg_df, agg_time = measure_performance(optimized_aggregate_by_account, fraud_df)
    metrics['aggregation_time'] = agg_time
    print(f"Optimized aggregation: {agg_time:.3f} seconds")
    
    total_time = sum(metrics.values())
    metrics['total_time'] = total_time
    print(f"Total optimized pipeline time: {total_time:.3f} seconds")
    
    return metrics

def compare_performance(baseline_metrics: dict, optimized_metrics: dict):
    """
    Compare baseline and optimized performance.
    
    Args:
        baseline_metrics (dict): Baseline performance metrics
        optimized_metrics (dict): Optimized performance metrics
    """
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    print(f"{'Operation':<20} {'Baseline':<12} {'Optimized':<12} {'Improvement':<12}")
    print("-" * 60)
    
    for operation in ['cleaning_time', 'fraud_detection_time', 'aggregation_time', 'total_time']:
        baseline = baseline_metrics[operation]
        optimized = optimized_metrics[operation]
        improvement = ((baseline - optimized) / baseline) * 100
        
        operation_name = operation.replace('_', ' ').title()
        print(f"{operation_name:<20} {baseline:<12.3f} {optimized:<12.3f} {improvement:<12.1f}%")
    
    print("-" * 60)

def demonstrate_chunked_processing(df: pd.DataFrame, chunk_size: int = 5000):
    """
    Demonstrate chunked processing for very large datasets.
    
    Args:
        df (pd.DataFrame): Large dataset
        chunk_size (int): Size of each chunk
    """
    print(f"\n" + "="*50)
    print(f"CHUNKED PROCESSING (Chunk size: {chunk_size})")
    print("="*50)
    
    start_time = time.time()
    
    # Process in chunks
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        cleaned_chunk = optimized_clean_data(chunk)
        chunks.append(cleaned_chunk)
        
        if i % (chunk_size * 2) == 0:
            print(f"Processed chunk {i//chunk_size + 1}/{(len(df) + chunk_size - 1)//chunk_size}")
    
    # Combine results
    combined_df = pd.concat(chunks, ignore_index=True)
    
    # Final aggregation
    final_agg = optimized_aggregate_by_account(combined_df)
    
    end_time = time.time()
    chunked_time = end_time - start_time
    
    print(f"Chunked processing time: {chunked_time:.3f} seconds")
    print(f"Final aggregation records: {len(final_agg)}")
    
    return chunked_time

def run_performance_exercise():
    """
    Run the complete performance exercise.
    """
    print("="*80)
    print("PERFORMANCE EXERCISE 3: Large Dataset Optimization")
    print("="*80)
    
    # Generate large dataset
    large_df = generate_large_dataset(10000)
    
    # Save the large dataset
    save_large_dataset(large_df, "data/large_transactions.csv")
    
    # Run baseline pipeline
    baseline_metrics = run_baseline_pipeline(large_df)
    
    # Run optimized pipeline
    optimized_metrics = run_optimized_pipeline(large_df)
    
    # Compare performance
    compare_performance(baseline_metrics, optimized_metrics)
    
    # Demonstrate chunked processing
    chunked_time = demonstrate_chunked_processing(large_df)
    
    # Summary
    print("\n" + "="*80)
    print("PERFORMANCE OPTIMIZATION SUMMARY")
    print("="*80)
    print(f"Dataset size: {len(large_df)} records")
    print(f"Baseline total time: {baseline_metrics['total_time']:.3f} seconds")
    print(f"Optimized total time: {optimized_metrics['total_time']:.3f} seconds")
    print(f"Chunked processing time: {chunked_time:.3f} seconds")
    
    improvement = ((baseline_metrics['total_time'] - optimized_metrics['total_time']) / 
                   baseline_metrics['total_time']) * 100
    print(f"Performance improvement: {improvement:.1f}%")
    
    print("\nKey optimization techniques demonstrated:")
    print("1. Efficient data type conversions")
    print("2. Optimized groupby operations with observed=True")
    print("3. Bulk operations instead of row-by-row processing")
    print("4. Chunked processing for memory efficiency")
    print("5. Reduced intermediate data copies")
    
    print("="*80)

if __name__ == "__main__":
    setup_performance_logging()
    run_performance_exercise()
