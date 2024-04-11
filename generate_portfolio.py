import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Functions from previous steps
def get_historical_data(crypto_id, days=500, currency='usd'):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': currency,
        'days': days
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_top_cryptos(limit=200):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    data = response.json()
    coins = [coin['id'] for coin in data]
    return coins

def main():
    st.title('Cryptocurrency Portfolio Strategy Simulator')

    # Fetching top cryptocurrencies
    top_coins = get_top_cryptos()

    # Sidebar for user inputs
    crypto_id = st.sidebar.selectbox('Select Cryptocurrency', top_coins)
    strategy = st.sidebar.selectbox('Select Strategy', ['Market Cap Weighted', 'Capped at X%', 'Top 15 by Volume'])
    days = st.sidebar.slider('Select Time Frame (Days)', 30, 365, step=30)

    data = get_historical_data(crypto_id, days=int(days))
    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    prices['price'] = prices['price'].astype(float)

    # Plotting using Plotly for interactive graphs
    fig = px.line(prices, x='date', y='price', title=f'Historical Price of {crypto_id}', labels={'price': 'Price (USD)'})
    st.plotly_chart(fig, use_container_width=True)

    # Additional strategy simulations and visualizations as needed

if __name__ == "__main__":
    main()
