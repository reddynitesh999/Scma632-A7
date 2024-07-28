pip install streamlit yfinance matplotlib

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data
@st.cache
def fetch_data(ticker, period='1y'):
    stock_data = yf.download(ticker, period=period)
    return stock_data

# App title
st.title('Stock Market Dashboard')

# Sidebar - Stock selection
st.sidebar.header('Select Stock')
ticker = st.sidebar.text_input('Ticker Symbol', 'AAPL')

# Sidebar - Date range selection
st.sidebar.header('Select Date Range')
period = st.sidebar.selectbox('Period', ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'])

# Fetch data
if ticker:
    data = fetch_data(ticker, period)
    st.header(f'{ticker} Stock Data')
    st.write(data.tail())

    # Plotting the data
    st.header('Stock Price')
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(plt)

    # Additional plots
    st.header('Moving Averages')
    ma_periods = [10, 20, 50]
    for ma in ma_periods:
        data[f'MA{ma}'] = data['Close'].rolling(window=ma).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price')
    for ma in ma_periods:
        plt.plot(data[f'MA{ma}'], label=f'MA {ma} days')
    plt.title(f'{ticker} Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(plt)

    # Volume Plot
    st.header('Stock Volume')
    plt.figure(figsize=(10, 5))
    plt.bar(data.index, data['Volume'], label='Volume')
    plt.title(f'{ticker} Stock Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    st.pyplot(plt)

    # Summary statistics
    st.header('Summary Statistics')
    st.write(data.describe())
else:
    st.write("Please enter a ticker symbol.")
