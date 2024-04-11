import streamlit as st

# Function to generate example portfolio based on selected strategy and year
def generate_portfolio(strategy, year):
    # Here you would implement the logic to generate the portfolio based on the selected strategy and year
    # For the sake of this example, we'll just display a dummy portfolio
    if strategy == "Fully Weighted by Market Cap":
        portfolio = {
            "Bitcoin": 25,
            "Ethereum": 25,
            "Solana": 9,
            "Other": 41
        }
    elif strategy == "Weighted by Market Cap with Cap":
        portfolio = {
            "Bitcoin": 30,
            "Ethereum": 30,
            "Solana": 10,
            "Other": 30
        }
    else:  # "Top 15 Cryptos by Volume"
        portfolio = {
            "Bitcoin": 20,
            "Ethereum": 20,
            "Solana": 10,
            "Other": 50
        }
    return portfolio

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

    # Display information about dummy coins
    st.write("### About Dummy Coins:")
    st.write("In this simulator, we use a few dummy coins to represent various cryptocurrencies.")
    st.write("These coins have been selected purely for demonstration purposes and do not reflect real-world data.")

# Run the main function
if __name__ == "__main__":
    main()
