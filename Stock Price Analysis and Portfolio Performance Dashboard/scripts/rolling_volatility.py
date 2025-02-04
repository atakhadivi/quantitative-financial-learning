import pandas as pd
from pathlib import Path

DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']

def calculate_rolling_volatility(ticker: str, window: int = 20) -> pd.DataFrame:
    """Calculate rolling volatility (standard deviation) of daily returns.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        window: Rolling window size (default is 20)
    
    Returns:
        DataFrame with rolling volatility added
    """
    # Load cleaned data
    processed_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(processed_path, parse_dates=['Date'], index_col='Date')
    
    # Calculate rolling volatility (standard deviation) of daily returns
    df[f'{ticker}_rolling_volatility'] = df['daily_returns'].rolling(window=window).std()
    
    return df

if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Calculating rolling volatility for {ticker}...")
        df_with_volatility = calculate_rolling_volatility(ticker)
        
        # Save the results with rolling volatility to a new CSV file
        volatility_path = DATA_PROCESSED_DIR / f"{ticker}_with_rolling_volatility.csv"
        df_with_volatility.to_csv(volatility_path)
        print(f"Saved rolling volatility data to {volatility_path}")
