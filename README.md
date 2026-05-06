# Banking Data Pipeline

A production-ready ETL pipeline for analyzing banking transactions with fraud detection capabilities.

## Overview

This pipeline processes banking transaction data to:
- Load transaction data from CSV files
- Clean duplicates and handle missing values
- Flag high-value transactions for fraud detection
- Aggregate total transaction amounts per account
- Generate comprehensive reports and summaries

## Features

- **Modular Design**: Separate modules for loading, transforming, fraud detection, and saving data
- **Error Handling**: Comprehensive error handling with detailed logging
- **Fraud Detection**: Configurable threshold-based fraud detection
- **Data Validation**: Automatic data type conversion and validation
- **Logging**: Detailed logging for monitoring and debugging
- **Unit Tests**: Complete test coverage for all components

## Project Structure

```
banking_pipeline/
├── data/
│   └── transactions.csv          # Input transaction data
├── src/
│   ├── load.py                   # Data loading module
│   ├── transform.py              # Data cleaning and aggregation
│   ├── fraud.py                  # Fraud detection logic
│   ├── save.py                   # Data saving utilities
│   └── main.py                   # Main pipeline orchestrator
├── tests/
│   └── test_pipeline.py          # Unit tests
├── output/                       # Generated output files
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── pipeline.log                  # Pipeline execution log
```

## Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd banking_pipeline
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Pipeline

Execute the main pipeline:
```bash
python src/main.py
```

### Custom Parameters

You can customize the pipeline by modifying the `run_pipeline()` call in `main.py`:

```python
run_pipeline(
    input_file="data/transactions.csv",  # Custom input file
    output_dir="output",                  # Custom output directory
    fraud_threshold=800                   # Custom fraud detection threshold
)
```

## Input Data Format

The pipeline expects CSV files with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | integer | Unique transaction identifier |
| account_id | integer | Customer account identifier |
| amount | float | Transaction amount |
| transaction_type | string | Transaction type (credit/debit) |
| transaction_date | string | Transaction date (YYYY-MM-DD) |

Example:
```csv
transaction_id,account_id,amount,transaction_type,transaction_date
1,1001,500,credit,2024-01-01
2,1002,200,debit,2024-01-01
3,1001,,credit,2024-01-02
4,1003,1000,debit,2024-01-02
```

## Output Files

The pipeline generates the following output files in the `output/` directory:

1. **clean_transactions.csv**: Cleaned transaction data with no duplicates or null values
2. **account_aggregations.csv**: Total transaction amounts aggregated by account
3. **fraud_detection.csv**: Transaction data with fraud detection flags
4. **fraud_summary.csv**: Summary of fraud detection by account

### Output Schema

#### clean_transactions.csv & fraud_detection.csv
- All original columns plus cleaned data
- `fraud_detection.csv` includes additional `is_fraud` boolean column

#### account_aggregations.csv
| Column | Description |
|--------|-------------|
| account_id | Account identifier |
| total_amount | Sum of all transactions for the account |

#### fraud_summary.csv
| Column | Description |
|--------|-------------|
| account_id | Account identifier |
| fraud_transactions | Number of flagged transactions |
| total_transactions | Total number of transactions |
| total_amount | Sum of all transaction amounts |
| fraud_percentage | Percentage of flagged transactions |

## Fraud Detection

The pipeline flags transactions as potentially fraudulent based on configurable thresholds:

- **Default Threshold**: $800
- **Logic**: Transactions with amount > threshold are flagged
- **Customization**: Modify the `fraud_threshold` parameter in `main.py`

## Testing

Run the unit tests:
```bash
pytest tests/
```

Run tests with verbose output:
```bash
pytest tests/ -v
```

## Logging

The pipeline provides comprehensive logging:
- **Console Output**: Real-time progress updates
- **Log File**: Detailed execution logs saved to `pipeline.log`

Log levels:
- INFO: General pipeline progress
- ERROR: Errors and exceptions

## Error Handling

The pipeline includes robust error handling for:
- File not found errors
- Empty data files
- Data type conversion issues
- File permission problems
- Invalid data formats

## Performance Considerations

- Memory-efficient processing for large datasets
- Configurable batch processing capabilities
- Optimized pandas operations

## Troubleshooting

### Common Issues

1. **File Not Found**: Ensure the input CSV file exists in the `data/` directory
2. **Permission Errors**: Check write permissions for the output directory
3. **Memory Issues**: For very large datasets, consider processing in chunks

### Debug Mode

Enable detailed logging by modifying the logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Extension Opportunities

The pipeline can be extended with:
- Database connectivity (PostgreSQL, MySQL)
- Real-time stream processing
- Machine learning-based fraud detection
- Data visualization dashboards
- API endpoints for data access

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate tests for new features
3. Update documentation for any changes
4. Ensure all tests pass before submitting

## License

This project is provided for educational purposes.
