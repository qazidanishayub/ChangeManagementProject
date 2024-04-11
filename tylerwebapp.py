import streamlit as st
import requests
import plotly.graph_objs as go
import numpy as np

# Function to generate random portfolio
def generate_random_portfolio():
    coins = ["Bitcoin", "Ethereum", "Solana", "Ripple", "Cardano", "Polkadot", "Litecoin", "Chainlink", "Stellar", "Tezos", "VeChain", "Theta Token", "Monero", "EOS", "Trading View", "DummyCoin"]
    portfolio = {}
    for coin in coins:
        portfolio[coin] = np.random.randint(1, 20)
    total = sum(portfolio.values())
    for coin in portfolio:
        portfolio[coin] = round((portfolio[coin] / total) * 100, 2)
    return portfolio

# Function to create dummy trend graph
def create_dummy_trend_graph(selected_assets, years):
    fig = go.Figure()
    for asset in selected_assets:
        for year in years:
            x_values = list(range(1, 13))  # Assuming 12 months in a year
            y_values = np.random.randint(50, 300, size=12)  # Random price data
            fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name=f"{asset} ({year})"))
    fig.update_layout(title="Price Trend", xaxis_title='Time', yaxis_title='Price (USD)')
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
    st.write("Welcome to the Crypto Portfolio Simulator. Select a year and coin to see the trend graph.")

    # Year selection
    year = st.slider("Select Year", min_value=2020, max_value=2025, value=2022, step=1)

    # Generate random portfolio
    portfolio = generate_random_portfolio()

    # Cryptocurrency selection
    selected_coins = st.multiselect("Select Coins/ETF Tokens", list(portfolio.keys()), default=["Bitcoin", "Ethereum"])

    # Display the generated portfolio
    st.write("### Example Portfolio:")
    st.write("Year:", year)
    st.write("Portfolio Composition:")
    for asset, weight in portfolio.items():
        st.write(f"- {asset}: {weight}%")

    # Display trend graph
    st.write("### Price Trend Graph:")
    years_to_show = st.multiselect("Select Years to Show", list(range(2020, 2026)), default=[year])
    trend_fig = create_dummy_trend_graph(selected_coins, years_to_show)
    st.plotly_chart(trend_fig)

# Run the main function
if __name__ == "__main__":
    main()
