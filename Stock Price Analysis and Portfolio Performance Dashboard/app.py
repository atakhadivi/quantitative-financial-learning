import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.clean_stock_data import clean_data
from scripts.moving_average import calculate_moving_averages
from scripts.rolling_volatility import calculate_rolling_volatility
from scripts.annualized_sharpe_ratio import calculate_annualized_sharpe_ratio
from scripts.maximum_drawdown import calculate_max_drawdown
from scripts.candlestick_charts import plot_candlestick
from scripts.plot_price_Trends_with_moving_averages import plot_price_with_moving_averages
from scripts.portfolio_performance import calculate_cumulative_returns, calculate_portfolio_returns
from scripts.benchmark_comparison import plot_portfolio_vs_benchmark
from scripts.volatility_and_drawdown_charts import plot_volatility, plot_drawdown

@st.cache_data
def load_data(stock):
    # Load cleaned data from data/processed/
    file_path = f"data/processed/{stock}_cleaned.csv"
    return pd.read_csv(file_path, parse_dates=['Date'])

stocks = ["AAPL", "SPY"]  # Add more stocks if needed

st.sidebar.title("Stock Dashboard")
selected_stock = st.sidebar.selectbox("Select Stock", stocks)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

data = load_data(selected_stock)
data['Date'] = pd.to_datetime(data['Date'])
data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Price Trends", "Candlestick Chart", "Risk Metrics", 
    "Portfolio Performance", "Benchmark Comparison", "Volatility & Drawdown"
])

with tab1:
    st.subheader("Price Trends with Moving Averages")
    fig1 = plot_price_with_moving_averages(data)
    st.pyplot(fig1)

with tab2:
    st.subheader("Candlestick Chart")
    fig2 = plot_candlestick(data)
    st.pyplot(fig2)

with tab3:
    st.subheader("Risk Metrics")
    sharpe_ratio = calculate_annualized_sharpe_ratio(data)
    max_drawdown = calculate_max_drawdown(data)
    rolling_volatility = calculate_rolling_volatility(data)

    st.metric("Annualized Sharpe Ratio", f"{sharpe_ratio:.2f}")
    st.metric("Maximum Drawdown", f"{max_drawdown:.2%}")
    st.line_chart(rolling_volatility)

with tab4:
    st.subheader("Portfolio Performance")
    portfolio_returns = calculate_portfolio_returns(data)
    cumulative_returns = calculate_cumulative_returns(portfolio_returns)
    st.line_chart(cumulative_returns)

with tab5:
    st.subheader("Benchmark Comparison")
    benchmark = "SPY"
    benchmark_data = load_data(benchmark)
    benchmark_data = benchmark_data[(benchmark_data['Date'] >= start_date) & (benchmark_data['Date'] <= end_date)]
    
    comparison_fig = plot_portfolio_vs_benchmark(data, benchmark_data, selected_stock, benchmark)
    st.pyplot(comparison_fig)

with tab6:
    st.subheader("Volatility & Drawdown")
    fig3, ax = plt.subplots(2, 1, figsize=(10, 8))
    plot_volatility(data, ax[0])
    plot_drawdown(data, ax[1])
    st.pyplot(fig3)