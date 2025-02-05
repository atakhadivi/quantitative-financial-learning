import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# Directory paths
DATA_PROCESSED_DIR = Path("data/processed")
TICKERS = ['AAPL', 'AMZN', 'SPY']  # List of available tickers (add more as needed)

# Function to load data
def load_data(ticker, start_date, end_date):
    file_path = DATA_PROCESSED_DIR / f"{ticker}_cleaned.csv"
    
    # Check if data exists in the processed folder
    if file_path.exists():
        df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
        df = df.loc[start_date:end_date]  # Filter by date range
        # Check if the required columns exist
        if 'Daily_Returns' not in df.columns:
            st.error(f"Error: 'Daily_Returns' column is missing in the cleaned data for {ticker}.")
            return None
    else:
        st.error(f"Error: Cleaned data for {ticker} not found.")
        return None
    
    return df

# Function to calculate Sharpe ratio and Maximum Drawdown
def calculate_risk_metrics(df):
    # Calculate Sharpe ratio (annualized)
    annualized_sharpe = np.sqrt(252) * df['Daily_Returns'].mean() / df['Daily_Returns'].std()

    # Calculate Maximum Drawdown
    cumulative_returns = (1 + df['Daily_Returns']).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    return annualized_sharpe, max_drawdown

# Function to create candlestick chart
def plot_candlestick(df, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=f'{ticker} Candlestick'
    )])
    fig.update_layout(
        title=f'{ticker} Stock Price Candlestick',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark'
    )
    st.plotly_chart(fig)

# Function to plot price trends with moving averages
def plot_price_with_moving_averages(df, ticker):
    ma_20_col = f'{ticker}_20MA'
    ma_50_col = f'{ticker}_50MA'
    ma_200_col = f'{ticker}_200MA'

    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label=f'{ticker} Close Price', color='blue')
    plt.plot(df[ma_20_col], label='20-Day MA', color='orange', linestyle='--')
    plt.plot(df[ma_50_col], label='50-Day MA', color='green', linestyle='--')
    plt.plot(df[ma_200_col], label='200-Day MA', color='red', linestyle='--')

    plt.title(f'{ticker} Price Trends with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend(loc='best')
    plt.grid(True)
    st.pyplot()

# Streamlit dashboard layout
st.title("Stock Price Analysis and Portfolio Performance Dashboard")

# Widget to select the stock ticker
ticker = st.selectbox("Select Stock Ticker", TICKERS)

# Widget to select the date range
start_date = st.date_input("Start Date", pd.to_datetime('2020-01-01'))
end_date = st.date_input("End Date", pd.to_datetime('2023-01-01'))

# Load data based on user selection
df_stock = load_data(ticker, start_date, end_date)

if df_stock is not None:
    # Calculate risk metrics
    sharpe_ratio, max_drawdown = calculate_risk_metrics(df_stock)

    # Display risk metrics
    st.subheader("Risk Metrics")
    st.write(f"**Annualized Sharpe Ratio**: {sharpe_ratio:.2f}")
    st.write(f"**Maximum Drawdown**: {max_drawdown:.2%}")

    # Plot the candlestick chart
    st.subheader(f"{ticker} Candlestick Chart")
    plot_candlestick(df_stock
