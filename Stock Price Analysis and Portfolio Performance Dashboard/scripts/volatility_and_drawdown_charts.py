import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Directory paths
DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL']  # Add more tickers if needed

def plot_volatility(ticker: str):
    """Plot stock rolling volatility."""
    # Load data with rolling volatility
    file_path = DATA_PROCESSED_DIR / f"{ticker}_with_rolling_volatility.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # Ensure necessary column exists
    volatility_col = f'{ticker}_rolling_volatility'
    if volatility_col not in df.columns:
        print(f"Error: Missing {volatility_col} column in {file_path}.")
        return

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df[volatility_col], label='Rolling Volatility', color='blue')

    plt.title(f'{ticker} Rolling Volatility')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def plot_drawdown(ticker: str):
    """Plot stock drawdown."""
    # Load cleaned data with close prices
    file_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # Calculate drawdown
    df['Running_Max'] = df['Close'].cummax()  # Running maximum of the 'Close'
    df['Drawdown'] = (df['Close'] - df['Running_Max']) / df['Running_Max']  # Calculate drawdown

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Drawdown'], label='Drawdown', color='red')

    plt.title(f'{ticker} Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Plotting volatility for {ticker}...")
        plot_volatility(ticker)
        
        print(f"Plotting drawdown for {ticker}...")
        plot_drawdown(ticker)
