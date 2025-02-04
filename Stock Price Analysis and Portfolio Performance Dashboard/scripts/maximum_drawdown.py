import pandas as pd
from pathlib import Path
import numpy as np

DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']

def calculate_max_drawdown(ticker: str) -> float:
    """Calculate the Maximum Drawdown (MDD).
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
    
    Returns:
        Maximum Drawdown (MDD) value as a percentage
    """
    # Load cleaned data
    processed_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(processed_path, parse_dates=['Date'], index_col='Date')
    
    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod()
    
    # Calculate rolling peak
    df['rolling_peak'] = df['cumulative_returns'].cummax()
    
    # Calculate drawdown
    df['drawdown'] = (df['cumulative_returns'] - df['rolling_peak']) / df['rolling_peak']
    
    # Maximum drawdown
    max_drawdown = df['drawdown'].min()  # Find the minimum (most negative) drawdown
    
    return max_drawdown

if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Calculating Maximum Drawdown for {ticker}...")
        max_drawdown = calculate_max_drawdown(ticker)
        print(f"Maximum Drawdown for {ticker}: {max_drawdown * 100:.2f}%")
