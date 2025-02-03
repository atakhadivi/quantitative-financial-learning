# clean_stock_data.py
import pandas as pd
from pathlib import Path
import numpy as np

DATA_RAW_DIR = Path("data/raw")
DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']

def clean_data(ticker: str, method: str = 'ffill') -> pd.DataFrame:
    """Clean stock data and handle missing values.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        method: 'ffill' (forward-fill) or 'drop' (remove rows)
    
    Returns:
        Cleaned DataFrame with returns calculated
    """
    # Load raw data
    raw_path = DATA_RAW_DIR / f"{ticker}_historical.csv"
    df = pd.read_csv(raw_path, parse_dates=['Date'], index_col='Date')
    
    # Handle missing values
    if method == 'ffill':
        df = df.ffill()  # Forward-fill missing values
    elif method == 'drop':
        df = df.dropna()  # Remove rows with any missing values
    
    # Calculate returns
    df['daily_returns'] = df['Close'].pct_change()  # Percentage returns
    df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))  # Log returns
    
    # Drop initial NaN row from returns calculation
    df = df.dropna()
    
    return df

if __name__ == "__main__":
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    for ticker in TICKERS:
        print(f"Cleaning {ticker} data...")
        cleaned_df = clean_data(ticker, method='ffill')  # Change to 'drop' if preferred
        
        # Save processed data
        processed_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
        cleaned_df.to_csv(processed_path)
        print(f"Saved cleaned data to {processed_path}")