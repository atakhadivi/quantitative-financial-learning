import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Directory paths
DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL']  # Add more tickers if needed

def plot_candlestick(ticker: str):
    """Plot Candlestick chart for the given ticker."""
    # Load data
    file_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # Ensure necessary columns exist
    required_columns = ['Open', 'High', 'Low', 'Close']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Missing columns in {file_path}. Required: {required_columns}")
        return

    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=f'{ticker} Candlestick'
    )])

    # Set the layout
    fig.update_layout(
        title=f'{ticker} Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,  # Hide the range slider
        template='plotly_dark',  # Use dark theme
        title_x=0.5,  # Center title
        width=1000,  # Set width
        height=600,  # Set height
    )

    # Show the chart
    fig.show()

if __name__ == "__main__":
    for ticker in TICKERS:
        print(f"Plotting candlestick chart for {ticker}...")
        plot_candlestick(ticker)
