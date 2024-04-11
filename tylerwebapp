import streamlit as st

# Function to generate example portfolio based on selected strategy and year
def generate_portfolio(strategy, year):
    # Here you would implement the logic to generate the portfolio based on the selected strategy and year
    # For the sake of this example, we'll just display a dummy portfolio
    portfolio = {
        "Bitcoin": 25,
        "Ethereum": 25,
        "Solana": 9,
        "Other": 41
    }
    return portfolio

# Main function to run the web application
def main():
    st.title("Crypto Portfolio Simulator")

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

# Run the main function
if __name__ == "__main__":
    main()
