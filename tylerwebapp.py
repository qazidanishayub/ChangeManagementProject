import streamlit as st
import requests
import plotly.graph_objs as go

# Function to fetch cryptocurrency data from CoinGecko API
def get_crypto_data():
    # Fetching data for Bitcoin, Ethereum, Solana, and other coins
    coins = ["bitcoin", "ethereum", "solana", "ripple", "cardano", "polkadot", "litecoin", "chainlink", "stellar", "tezos", "vechain", "theta-token", "monero", "eos", "trading-view", "dummycoin"]
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
            "Bitcoin": 15,
            "Ethereum": 15,
            "Solana": 10,
            "Ripple": 10,
            "Cardano": 10,
            "Polkadot": 5,
            "Litecoin": 5,
            "Chainlink": 5,
            "Stellar": 5,
            "Tezos": 5,
            "VeChain": 5,
            "Theta Token": 5,
            "Monero": 5,
            "EOS": 5,
            "Trading View": 5,
            "DummyCoin": 5
        }
    elif strategy == "Weighted by Market Cap with Cap":
        portfolio = {
            "Bitcoin": 20,
            "Ethereum": 20,
            "Solana": 15,
            "Ripple": 15,
            "Cardano": 10,
            "Polkadot": 5,
            "Litecoin": 5,
            "Chainlink": 5,
            "Stellar": 5,
            "Tezos": 5,
            "VeChain": 5,
            "Theta Token": 5,
            "Monero": 5,
            "EOS": 5,
            "Trading View": 5,
            "DummyCoin": 5
        }
    else:  # "Top 15 Cryptos by Volume"
        portfolio = {
            "Bitcoin": 10,
            "Ethereum": 10,
            "Solana": 10,
            "Ripple": 10,
            "Cardano": 10,
            "Polkadot": 5,
            "Litecoin": 5,
            "Chainlink": 5,
            "Stellar": 5,
            "Tezos": 5,
            "VeChain": 5,
            "Theta Token": 5,
            "Monero": 5,
            "EOS": 5,
            "Trading View": 5,
            "DummyCoin": 5
        }
    return portfolio

# Function to create a dummy trend graph
def create_dummy_trend_graph(coin, years):
    fig = go.Figure()
    for year in years:
        x_values = list(range(1, 13))  # Assuming 12 months in a year
        y_values = [100 + i * 10 for i in range(12)]  # Dummy price data
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name=f"{coin} ({year})"))
    fig.update_layout(title=f"{coin} Price Trend", xaxis_title='Time', yaxis_title='Price (USD)')
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
    st.write("Welcome to the Crypto Portfolio Simulator. Select a portfolio strategy, year, and coin to see an example portfolio and trend graph.")

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

    # Cryptocurrency selection
    selected_coin = st.selectbox("Select Coin", ["Bitcoin", "Ethereum", "Solana", "Ripple", "Cardano", "Polkadot", "Litecoin", "Chainlink", "Stellar", "Tezos", "VeChain", "Theta Token", "Monero", "EOS", "Trading View", "DummyCoin"])

    # Display cryptocurrency details
    st.write("### Cryptocurrency Details:")
    crypto_data = get_crypto_data()
    if selected_coin in crypto_data:
        details = crypto_data[selected_coin]
        st.write(f"#### {details['name']} ({details['symbol']})")
        st.write(f"Current Price: ${details['current_price']}")
        st.write(f"Market Cap: ${details['market_cap']}")
        st.write(f"Total Volume: ${details['total_volume']}")
        st.image(details['image'], use_column_width=True)

    # Display trend graph
    st.write("### Price Trend Graph:")
    years_to_show = st.multiselect("Select Years to Show", list(range(2020, 2026)), default=[year])
    trend_fig = create_dummy_trend_graph(selected_coin, years_to_show)
    st.plotly_chart(trend_fig)

# Run the main function
if __name__ == "__main__":
    main()
