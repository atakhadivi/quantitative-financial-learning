import yfinance as yf
import pandas as pd
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Configuration
DEFAULT_TICKERS = ['AAPL', 'SPY']
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"
DATA_DIR = Path("data/raw")

def fetch_data(tickers: list, start_date: str, end_date: str) -> dict:
    """Fetch historical prices for multiple stocks concurrently"""
    results = {}
    
    def fetch_single(ticker):
        try:
            data = yf.download(
                tickers=ticker,
                start=start_date,
                end=end_date,
                interval="1d",
                auto_adjust=True,
                progress=False
            )
            if data.empty:
                print(f"Warning: No data found for {ticker}")
            return {ticker: data}
        except Exception as e:
            print(f"Failed to fetch {ticker}: {str(e)}")
            return {}
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_single, t) for t in tickers]
        for future in futures:
            results.update(future.result())
    
    return results

def save_data(stock_data: dict, save_dir: Path):
    """Save fetched data to CSV files"""
    save_dir.mkdir(parents=True, exist_ok=True)
    for ticker, df in stock_data.items():
        if not df.empty:
            df.to_csv(save_dir / f"{ticker}_historical.csv")
            print(f"Saved {ticker}_historical.csv to {save_dir}")

def main(tickers=None):
    tickers = tickers if tickers else DEFAULT_TICKERS
    print(f"Fetching data for {tickers}...")
    data = fetch_data(tickers, START_DATE, END_DATE)
    save_data(data, DATA_DIR)
    print("Data download complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()