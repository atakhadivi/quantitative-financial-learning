import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']  # Your portfolio + S&P 500 (SPY)
PORTFOLIO_TICKERS = ['AAPL']  # Example portfolio tickers, update with your actual portfolio tickers
PORTFOLIO_WEIGHTS = [0.5, 0.5]  # Example portfolio weights (sum must be 1)

def calculate_cumulative_returns(ticker: str) -> pd.Series:
    """Calculate cumulative returns for a given ticker."""
    # Load cleaned data
    processed_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(processed_path, parse_dates=['Date'], index_col='Date')
    
    # Calculate daily returns if not already present
    if 'daily_returns' not in df.columns:
        df['daily_returns'] = df['Close'].pct_change()
    
    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod() - 1
    return df['cumulative_returns']

def calculate_portfolio_returns(portfolio_tickers: list, weights: list) -> pd.Series:
    """Calculate portfolio cumulative returns."""
    portfolio_returns = pd.DataFrame()

    # Calculate weighted daily returns for the portfolio
    for ticker, weight in zip(portfolio_tickers, weights):
        daily_returns = calculate_cumulative_returns(ticker)
        portfolio_returns[ticker] = daily_returns * weight
    
    # Calculate cumulative portfolio returns
    portfolio_returns['portfolio'] = portfolio_returns.sum(axis=1)
    return portfolio_returns['portfolio']

if __name__ == "__main__":
    # Calculate portfolio returns
    portfolio_cumulative_returns = calculate_portfolio_returns(PORTFOLIO_TICKERS, PORTFOLIO_WEIGHTS)
    
    # Calculate S&P 500 (SPY) returns for comparison
    spy_cumulative_returns = calculate_cumulative_returns('SPY')
    
    # Plot cumulative returns comparison
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_cumulative_returns, label='Portfolio')
    plt.plot(spy_cumulative_returns, label='S&P 500 (SPY)', linestyle='--')
    
    plt.title("Portfolio Performance vs. S&P 500")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns")
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

    # Print final cumulative returns for comparison
    print(f"Final Portfolio Cumulative Return: {portfolio_cumulative_returns[-1]:.4f}")
    print(f"Final S&P 500 Cumulative Return: {spy_cumulative_returns[-1]:.4f}")
