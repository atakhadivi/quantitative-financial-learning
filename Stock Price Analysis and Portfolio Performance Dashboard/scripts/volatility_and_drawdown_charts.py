import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL']

def plot_volatility(ticker: str, ax: plt.Axes = None):
    """Plot stock rolling volatility on provided Axes."""
    file_path = DATA_PROCESSED_DIR / f"{ticker}_with_rolling_volatility.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    
    volatility_col = f'{ticker}_rolling_volatility'
    if volatility_col not in df.columns:
        print(f"Error: Column {volatility_col} missing in {file_path}")
        return
    
    # Create figure and subplot if not provided
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(df.index, df[volatility_col], label='Rolling Volatility', color='blue')
    ax.set_title(f"{ticker} Rolling Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.legend()
    ax.grid()
    ax.tick_params(axis='x', rotation=45)
    
    if standalone:
        plt.tight_layout()
        plt.show()

def plot_drawdown(ticker: str, ax: plt.Axes = None):
    """Plot stock drawdown on provided Axes."""
    file_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    
    df['Running_Max'] = df['Close'].cummax()
    df['Drawdown'] = (df['Close'] - df['Running_Max']) / df['Running_Max']
    
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(df.index, df['Drawdown'], label='Drawdown', color='red')
    ax.set_title(f"{ticker} Drawdown")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.legend()
    ax.grid()
    ax.tick_params(axis='x', rotation=45)
    
    if standalone:
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    for ticker in TICKERS:
        plot_volatility(ticker)
        plot_drawdown(ticker)