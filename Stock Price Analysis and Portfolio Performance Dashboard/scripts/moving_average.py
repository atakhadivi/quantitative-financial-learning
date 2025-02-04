import pandas as pd
from pathlib import Path

DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']

def calculate_moving_averages(ticker: str) -> pd.DataFrame:
    """Calculate 20-day, 50-day, and 200-day moving averages.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
    
    Returns:
        DataFrame with moving averages added
    """
    # Load cleaned data
    processed_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(processed_path, parse_dates=['Date'], index_col='Date')
    
    # Calculate moving averages
    df[f'{ticker}_20MA'] = df['Close'].rolling(window=20).mean()
    df[f'{ticker}_50MA'] = df['Close'].rolling(window=50).mean()
    df[f'{ticker}_200MA'] = df['Close'].rolling(window=200).mean()
    
    return df

if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Calculating moving averages for {ticker}...")
        df_with_ma = calculate_moving_averages(ticker)
        
        # Save the results with moving averages to a new CSV file
        moving_avg_path = DATA_PROCESSED_DIR / f"{ticker}_with_moving_averages.csv"
        df_with_ma.to_csv(moving_avg_path)
        print(f"Saved moving averages data to {moving_avg_path}")
