import pandas as pd
import logging

def detect_fraud(df: pd.DataFrame, threshold: float = 800) -> pd.DataFrame:
    """
    Flag high-value transactions for fraud detection.
    
    Args:
        df (pd.DataFrame): Transaction data
        threshold (float): Amount threshold for fraud detection (default: 800)
        
    Returns:
        pd.DataFrame: Transaction data with fraud detection flags
    """
    try:
        logging.info(f"Starting fraud detection with threshold: {threshold}")
        
        # Create a copy to avoid SettingWithCopyWarning
        df_fraud = df.copy()
        
        # Flag high-value transactions
        df_fraud['is_fraud'] = df_fraud['amount'] > threshold
        
        # Count flagged transactions
        fraud_count = df_fraud['is_fraud'].sum()
        total_count = len(df_fraud)
        
        logging.info(f"Fraud detection completed: {fraud_count}/{total_count} transactions flagged")
        
        return df_fraud
        
    except Exception as e:
        logging.error(f"Error during fraud detection: {str(e)}")
        raise

def get_fraud_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of fraud detection by account.
    
    Args:
        df (pd.DataFrame): Transaction data with fraud flags
        
    Returns:
        pd.DataFrame: Fraud summary by account
    """
    try:
        logging.info("Generating fraud summary")
        
        fraud_summary = df.groupby('account_id').agg({
            'is_fraud': ['sum', 'count'],
            'amount': 'sum'
        }).round(2)
        
        # Flatten column names
        fraud_summary.columns = ['fraud_transactions', 'total_transactions', 'total_amount']
        fraud_summary = fraud_summary.reset_index()
        
        # Calculate fraud percentage
        fraud_summary['fraud_percentage'] = (fraud_summary['fraud_transactions'] / 
                                           fraud_summary['total_transactions'] * 100).round(2)
        
        logging.info(f"Fraud summary generated for {len(fraud_summary)} accounts")
        return fraud_summary
        
    except Exception as e:
        logging.error(f"Error generating fraud summary: {str(e)}")
        raise
