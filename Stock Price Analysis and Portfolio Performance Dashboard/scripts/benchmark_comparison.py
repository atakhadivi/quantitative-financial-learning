import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Directory paths
DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL']  # Portfolio ticker
BENCHMARK_TICKER = 'SPY'  # Benchmark ticker

def plot_portfolio_vs_benchmark(portfolio_ticker: str, benchmark_ticker: str):
    """Plot portfolio vs benchmark cumulative returns comparison."""
    # Load portfolio and benchmark data
    portfolio_file = DATA_PROCESSED_DIR / f"{portfolio_ticker}_cleaned.csv"
    benchmark_file = DATA_PROCESSED_DIR / f"{benchmark_ticker}_cleaned.csv"
    
    df_portfolio = pd.read_csv(portfolio_file, parse_dates=['Date'], index_col='Date')
    df_benchmark = pd.read_csv(benchmark_file, parse_dates=['Date'], index_col='Date')
    
    # Ensure the necessary columns exist
    if 'Close' not in df_portfolio.columns or 'Close' not in df_benchmark.columns:
        print(f"Error: Missing 'Close' column in the data files.")
        return

    # Calculate cumulative returns for both portfolio and benchmark
    df_portfolio['Cumulative_Returns'] = (df_portfolio['Close'] / df_portfolio['Close'].iloc[0]) - 1
    df_benchmark['Cumulative_Returns'] = (df_benchmark['Close'] / df_benchmark['Close'].iloc[0]) - 1
    
    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(14, 12))
    
    # Portfolio Cumulative Returns
    ax[0].plot(df_portfolio.index, df_portfolio['Cumulative_Returns'], label=f'{portfolio_ticker} Cumulative Returns', color='blue')
    ax[0].set_title(f'{portfolio_ticker} Cumulative Returns')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Cumulative Returns')
    ax[0].legend(loc='best')
    ax[0].grid(True)

    # Benchmark Cumulative Returns
    ax[1].plot(df_benchmark.index, df_benchmark['Cumulative_Returns'], label=f'{benchmark_ticker} Cumulative Returns', color='red')
    ax[1].set_title(f'{benchmark_ticker} Cumulative Returns')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel('Cumulative Returns')
    ax[1].legend(loc='best')
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print(f"Comparing portfolio {TICKERS[0]} with benchmark {BENCHMARK_TICKER}...")
    plot_portfolio_vs_benchmark(TICKERS[0], BENCHMARK_TICKER)
