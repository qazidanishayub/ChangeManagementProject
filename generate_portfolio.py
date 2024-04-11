import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

import requests

def get_historical_data(crypto_id, days='max', currency='usd'):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': currency,
        'days': days
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_top_cryptos(limit=100):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    data = response.json()
    return [(crypto['id'], crypto['name']) for crypto in data]

# Assuming get_historical_data and get_top_cryptos are defined above

def main():
    st.title('Cryptocurrency Portfolio Strategy Simulator')

    # Fetch top 100 cryptocurrencies
    top_cryptos = get_top_cryptos()
    crypto_options = {name: id for id, name in top_cryptos}  # Dict for reverse lookup

    # Sidebar for user inputs
    selected_crypto_name = st.sidebar.selectbox('Select Cryptocurrency', list(crypto_options.keys()))
    crypto_id = crypto_options[selected_crypto_name]
    strategy = st.sidebar.selectbox('Select Strategy', ['Market Cap Weighted', 'Capped at X%', 'Top 15 by Volume'])
    start_date, end_date = st.sidebar.date_input('Select Date Range', [pd.to_datetime('2021-01-01'), pd.to_datetime('today')])

    # Fetch historical data within the selected date range
    days = (end_date - start_date).days
    data = get_historical_data(crypto_id, days=days)

    # Process data
    prices = pd.DataFrame(data['price'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    prices = prices[(prices['date'] >= start_date) & (prices['date'] <= end_date)]

    # Interactive Plotting with Plotly
    fig = px.line(prices, x='date', y='price', title=f'Price of {selected_crypto_name} over Selected Date Range', labels={'price': 'Price (USD)', 'date': 'Date'})
    st.plotly_chart(fig, use_container_width=True)

    # Add additional strategy simulations and visualizations as needed

if __name__ == "__main__":
    main()

