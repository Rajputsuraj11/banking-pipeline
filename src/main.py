import logging
import os
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from load import load_data
from transform import clean_data, aggregate_by_account
from fraud import detect_fraud, get_fraud_summary
from save import save_pipeline_outputs

def setup_logging():
    """Configure logging for the pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('pipeline.log')
        ]
    )

def run_pipeline(input_file: str = "data/transactions.csv", 
                output_dir: str = "output",
                fraud_threshold: float = 800) -> None:
    """
    Run the complete banking data pipeline.
    
    Args:
        input_file (str): Path to input CSV file
        output_dir (str): Output directory path
        fraud_threshold (float): Threshold for fraud detection
    """
    try:
        logging.info("=" * 50)
        logging.info("Starting Banking Data Pipeline")
        logging.info("=" * 50)
        
        # Step 1: Load data
        logging.info("Step 1: Loading data")
        df = load_data(input_file)
        
        # Step 2: Clean data
        logging.info("Step 2: Cleaning data")
        clean_df = clean_data(df)
        
        # Step 3: Detect fraud
        logging.info("Step 3: Fraud detection")
        fraud_df = detect_fraud(clean_df, fraud_threshold)
        
        # Step 4: Generate fraud summary
        logging.info("Step 4: Generating fraud summary")
        fraud_summary = get_fraud_summary(fraud_df)
        
        # Step 5: Aggregate data
        logging.info("Step 5: Aggregating data by account")
        agg_df = aggregate_by_account(clean_df)
        
        # Step 6: Save outputs
        logging.info("Step 6: Saving outputs")
        save_pipeline_outputs(clean_df, agg_df, fraud_df, fraud_summary, output_dir)
        
        # Print summary
        logging.info("=" * 50)
        logging.info("Pipeline completed successfully!")
        logging.info(f"Processed {len(clean_df)} transactions")
        logging.info(f"Flagged {fraud_df['is_fraud'].sum()} suspicious transactions")
        logging.info(f"Generated aggregations for {len(agg_df)} accounts")
        logging.info(f"Outputs saved to: {output_dir}/")
        logging.info("=" * 50)
        
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    setup_logging()
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    # Change to project root
    os.chdir(project_root)
    
    # Run pipeline
    run_pipeline()
