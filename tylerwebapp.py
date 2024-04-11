import streamlit as st
import requests
import plotly.graph_objs as go

# Function to fetch cryptocurrency data from CoinGecko API
def get_crypto_data():
    # Fetching data for Bitcoin, Ethereum, Solana, and another dummy coin
    coins = ["bitcoin", "ethereum", "solana", "dummycoin"]
    data = {}
    for coin in coins:
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin}")
        if response.status_code == 200:
            coin_data = response.json()
            data[coin] = {
                "name": coin_data["name"],
                "symbol": coin_data["symbol"],
                "current_price": coin_data["market_data"]["current_price"]["usd"],
                "market_cap": coin_data["market_data"]["market_cap"]["usd"],
                "total_volume": coin_data["market_data"]["total_volume"]["usd"],
                "image": coin_data["image"]["small"]
            }
    return data

# Function to generate example portfolio based on selected strategy and year
def generate_portfolio(strategy, year):
    # Dummy portfolio generation based on strategy and year
    if strategy == "Fully Weighted by Market Cap":
        portfolio = {
            "Bitcoin": 25,
            "Ethereum": 25,
            "Solana": 25,
            "DummyCoin": 25
        }
    elif strategy == "Weighted by Market Cap with Cap":
        portfolio = {
            "Bitcoin": 30,
            "Ethereum": 30,
            "Solana": 20,
            "DummyCoin": 20
        }
    else:  # "Top 15 Cryptos by Volume"
        portfolio = {
            "Bitcoin": 20,
            "Ethereum": 20,
            "Solana": 30,
            "DummyCoin": 30
        }
    return portfolio

# Function to create a dummy trend graph
def create_dummy_trend_graph():
    x_values = [1, 2, 3, 4, 5]
    y_values = [100, 120, 90, 110, 130]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Dummy Trend'))
    fig.update_layout(title='Dummy Coin Price Trend', xaxis_title='Time', yaxis_title='Price (USD)')
    return fig

# Main function to run the web application
def main():
    # Set page title and page icon
    st.set_page_config(page_title="Crypto Portfolio Simulator", page_icon=":money_with_wings:")

    # Set page background color and text color
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header with title and description
    st.title("Crypto Portfolio Simulator")
    st.write("Welcome to the Crypto Portfolio Simulator. Select a portfolio strategy and year to see an example portfolio.")

    # Portfolio strategy selection
    strategy = st.selectbox("Select Portfolio Strategy", ["Fully Weighted by Market Cap", "Weighted by Market Cap with Cap", "Top 15 Cryptos by Volume"])

    # Year selection
    year = st.slider("Select Year", min_value=2020, max_value=2025, value=2022, step=1)

    # Generate portfolio based on selected strategy and year
    portfolio = generate_portfolio(strategy, year)

    # Display the generated portfolio
    st.write("### Example Portfolio:")
    st.write("Year:", year)
    st.write("Strategy:", strategy)
    st.write("Portfolio Composition:")
    for asset, weight in portfolio.items():
        st.write(f"- {asset}: {weight}%")

    # Display cryptocurrency details
    st.write("### Cryptocurrency Details:")
    crypto_data = get_crypto_data()
    for coin, details in crypto_data.items():
        st.write(f"#### {details['name']} ({details['symbol']})")
        st.write(f"Current Price: ${details['current_price']}")
        st.write(f"Market Cap: ${details['market_cap']}")
        st.write(f"Total Volume: ${details['total_volume']}")
        st.image(details['image'], use_column_width=True)

    # Display a dummy trend graph
    st.write("### Dummy Trend Graph:")
    dummy_trend_fig = create_dummy_trend_graph()
    st.plotly_chart(dummy_trend_fig)

# Run the main function
if __name__ == "__main__":
    main()
