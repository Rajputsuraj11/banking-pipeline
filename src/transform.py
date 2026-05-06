import pandas as pd
import logging

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean transaction data by removing duplicates and handling missing values.
    
    Args:
        df (pd.DataFrame): Raw transaction data
        
    Returns:
        pd.DataFrame: Cleaned transaction data
    """
    try:
        logging.info("Starting data cleaning process")
        
        # Log initial state
        initial_count = len(df)
        logging.info(f"Initial record count: {initial_count}")
        
        # Remove duplicates
        df_cleaned = df.drop_duplicates()
        duplicates_removed = initial_count - len(df_cleaned)
        logging.info(f"Removed {duplicates_removed} duplicate records")
        
        # Handle missing values in amount column
        null_amounts = df_cleaned['amount'].isnull().sum()
        if null_amounts > 0:
            logging.info(f"Found {null_amounts} null values in amount column, filling with 0")
            df_cleaned['amount'] = df_cleaned['amount'].fillna(0)
        
        # Convert amount to numeric if needed
        df_cleaned['amount'] = pd.to_numeric(df_cleaned['amount'], errors='coerce')
        
        # Convert transaction_date to datetime
        df_cleaned['transaction_date'] = pd.to_datetime(df_cleaned['transaction_date'], errors='coerce')
        
        # Handle currency column - fill missing values with 'USD' as default
        if 'currency' in df_cleaned.columns:
            null_currencies = df_cleaned['currency'].isnull().sum()
            if null_currencies > 0:
                logging.info(f"Found {null_currencies} null values in currency column, filling with 'USD'")
                df_cleaned['currency'] = df_cleaned['currency'].fillna('USD')
            # Standardize currency codes to uppercase
            df_cleaned['currency'] = df_cleaned['currency'].str.upper()
        
        logging.info(f"Data cleaning completed. Final record count: {len(df_cleaned)}")
        return df_cleaned
        
    except Exception as e:
        logging.error(f"Error during data cleaning: {str(e)}")
        raise

def aggregate_by_account(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total transaction amount per account.
    
    Args:
        df (pd.DataFrame): Clean transaction data
        
    Returns:
        pd.DataFrame: Aggregated data by account
    """
    try:
        logging.info("Starting account aggregation")
        
        # Check if currency column exists and aggregate by currency as well
        if 'currency' in df.columns:
            agg_df = df.groupby(['account_id', 'currency'])['amount'].sum().reset_index()
            agg_df.columns = ['account_id', 'currency', 'total_amount']
            logging.info(f"Aggregation completed for {len(agg_df)} account-currency combinations")
        else:
            agg_df = df.groupby('account_id')['amount'].sum().reset_index()
            agg_df.columns = ['account_id', 'total_amount']
            logging.info(f"Aggregation completed for {len(agg_df)} unique accounts")
        
        return agg_df
        
    except Exception as e:
        logging.error(f"Error during aggregation: {str(e)}")
        raise
