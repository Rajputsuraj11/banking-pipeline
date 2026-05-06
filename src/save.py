import pandas as pd
import os
import logging

def save_data(df: pd.DataFrame, output_path: str, description: str = "data") -> None:
    """
    Save DataFrame to CSV file with error handling.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        output_path (str): Output file path
        description (str): Description of the data for logging
        
    Raises:
        Exception: If saving fails
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        logging.info(f"Saving {description} to {output_path}")
        df.to_csv(output_path, index=False)
        logging.info(f"Successfully saved {len(df)} records to {output_path}")
        
    except Exception as e:
        logging.error(f"Error saving {description} to {output_path}: {str(e)}")
        raise

def save_pipeline_outputs(clean_df: pd.DataFrame, agg_df: pd.DataFrame, 
                         fraud_df: pd.DataFrame, fraud_summary: pd.DataFrame,
                         output_dir: str = "output") -> None:
    """
    Save all pipeline outputs to files.
    
    Args:
        clean_df (pd.DataFrame): Cleaned transaction data
        agg_df (pd.DataFrame): Aggregated data by account
        fraud_df (pd.DataFrame): Transaction data with fraud flags
        fraud_summary (pd.DataFrame): Fraud summary by account
        output_dir (str): Output directory path
    """
    try:
        logging.info("Saving all pipeline outputs")
        
        # Save cleaned data
        save_data(clean_df, f"{output_dir}/clean_transactions.csv", "cleaned transactions")
        
        # Save aggregated data
        save_data(agg_df, f"{output_dir}/account_aggregations.csv", "account aggregations")
        
        # Save fraud detection results
        save_data(fraud_df, f"{output_dir}/fraud_detection.csv", "fraud detection results")
        
        # Save fraud summary
        save_data(fraud_summary, f"{output_dir}/fraud_summary.csv", "fraud summary")
        
        logging.info("All pipeline outputs saved successfully")
        
    except Exception as e:
        logging.error(f"Error saving pipeline outputs: {str(e)}")
        raise
