import pandas as pd
import logging

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load transaction data from CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded transaction data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
        Exception: For other loading errors
    """
    try:
        logging.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded {len(df)} records")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"File is empty: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {str(e)}")
        raise
