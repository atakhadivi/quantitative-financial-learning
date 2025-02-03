# fetch_stock_data.py
import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configuration
TICKERS = ['AAPL', 'SPY']
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime(2024, 12, 31)
DATA_DIR = Path("data/raw")

def fetch_data(tickers, start_date, end_date):
    """Fetch historical stock data from Yahoo Finance"""
    print(f"Fetching data for {tickers} from {start_date} to {end_date}")
    
    # Download data with 1-day interval
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        interval="1d",
        group_by='ticker',
        auto_adjust=True  # Use adjusted closing prices
    )
    
    return data

def save_data(data, data_dir):
    """Save data to CSV files"""
    for ticker in TICKERS:
        df = data[ticker]
        filename = data_dir / f"{ticker}_historical.csv"
        df.to_csv(filename)
        print(f"Saved {filename}")

if __name__ == "__main__":
    # Fetch and save data
    stock_data = fetch_data(TICKERS, START_DATE, END_DATE)
    save_data(stock_data, DATA_DIR)
    print("Data download complete!")