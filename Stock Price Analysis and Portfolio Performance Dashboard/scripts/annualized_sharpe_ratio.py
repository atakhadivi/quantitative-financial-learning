import pandas as pd
from pathlib import Path
import numpy as np

DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']
RISK_FREE_RATE = 0.02  # Example risk-free rate (2%)

def calculate_annualized_sharpe_ratio(ticker: str, window: int = 252) -> float:
    """Calculate annualized Sharpe ratio.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        window: The window size for rolling standard deviation (default is 252 trading days)
    
    Returns:
        Annualized Sharpe ratio
    """
    # Load cleaned data
    processed_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(processed_path, parse_dates=['Date'], index_col='Date')
    
    # Calculate daily returns if not present
    if 'daily_returns' not in df.columns:
        df['daily_returns'] = df['Close'].pct_change()
    
    # Calculate average daily return
    mean_daily_return = df['daily_returns'].mean()
    
    # Calculate daily volatility (standard deviation of returns)
    daily_volatility = df['daily_returns'].std()

    # Calculate Sharpe ratio (annualized)
    sharpe_ratio = (mean_daily_return - RISK_FREE_RATE / 252) / daily_volatility  # Daily Sharpe ratio
    annualized_sharpe_ratio = sharpe_ratio * np.sqrt(252)  # Annualize it
    
    return annualized_sharpe_ratio

if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Calculating annualized Sharpe ratio for {ticker}...")
        sharpe_ratio = calculate_annualized_sharpe_ratio(ticker)
        print(f"Annualized Sharpe ratio for {ticker}: {sharpe_ratio:.4f}")
