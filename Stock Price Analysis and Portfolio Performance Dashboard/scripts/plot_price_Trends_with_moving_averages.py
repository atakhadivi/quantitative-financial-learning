import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Directory paths
DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'SPY']  # Add more tickers if needed

def plot_price_with_moving_averages(ticker: str):
    """Plot stock price with pre-calculated moving averages (with ticker prefixes)."""
    # Load data with moving averages
    file_path = DATA_PROCESSED_DIR / f"{ticker}_with_moving_averages.csv"

    # چک کردن اینکه فایل وجود دارد یا نه
    if not file_path.exists():
        print(f"Error: Data file not found for {ticker}: {file_path}")
        return

    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # نمایش نام ستون‌ها برای دیباگ
    print(f"Columns in {ticker} dataset:", df.columns.tolist())

    # Dynamic column names based on the ticker
    close_col = 'Close'
    ma_20_col = f'{ticker}_20MA'
    ma_50_col = f'{ticker}_50MA'
    ma_200_col = f'{ticker}_200MA'

    # Ensure necessary columns exist
    required_columns = [close_col, ma_20_col, ma_50_col, ma_200_col]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Missing columns in {file_path}. Required: {required_columns}")
        return

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(df[close_col], label=f'{ticker} Close Price', color='blue')
    plt.plot(df[ma_20_col], label='20-Day MA', color='orange', linestyle='--')
    plt.plot(df[ma_50_col], label='50-Day MA', color='green', linestyle='--')
    plt.plot(df[ma_200_col], label='200-Day MA', color='red', linestyle='--')

    plt.title(f'{ticker} Price Trends with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Plotting price trends for {ticker}...")
        plot_price_with_moving_averages(ticker)
