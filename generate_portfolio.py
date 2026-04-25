import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# --- Config ---
st.set_page_config(page_title="Crypto Portfolio Pro", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Premium Look ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Metric Cards */
        div[data-testid="metric-container"] {
            background-color: #1E2329;
            border: 1px solid #2B3139;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 255, 128, 0.1);
            border-color: #00FF80;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #EAECEF;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        
        /* Premium Gradient Text */
        .gradient-text {
            background: linear-gradient(90deg, #00FF80 0%, #00BFFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #12161C;
        }
        
        /* Success Badge */
        .pro-badge {
            background: linear-gradient(90deg, #FFD700, #FFA500);
            color: #000;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
            vertical-align: middle;
            margin-left: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- Data Fetching Functions ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_top_cryptos(limit=50):
    """Fetch top N cryptos by market cap to populate selectbox"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {coin['id']: coin['name'] for coin in data}
    except Exception as e:
        st.sidebar.error(f"Error fetching top coins: {e}")
        # Fallback list if API fails
        return {'bitcoin': 'Bitcoin', 'ethereum': 'Ethereum', 'solana': 'Solana', 'binancecoin': 'BNB', 'cardano': 'Cardano'}

@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_data(crypto_id, days=365):
    """Fetch historical daily prices for a given crypto"""
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms').dt.normalize()
        prices = prices.drop_duplicates(subset='date').set_index('date')
        return prices['price'].rename(crypto_id)
    except Exception as e:
        st.error(f"Failed to fetch data for {crypto_id}. CoinGecko API rate limit might be exceeded.")
        return None

# --- Financial Metrics Calculations ---
def calculate_metrics(portfolio_series, risk_free_rate=0.02):
    """Calculate key financial metrics for a portfolio equity curve"""
    # Daily Returns
    daily_returns = portfolio_series.pct_change().dropna()
    
    # Total Return
    total_return = (portfolio_series.iloc[-1] / portfolio_series.iloc[0]) - 1
    
    # CAGR (Compound Annual Growth Rate)
    days = (portfolio_series.index[-1] - portfolio_series.index[0]).days
    years = days / 365.25
    cagr = (portfolio_series.iloc[-1] / portfolio_series.iloc[0]) ** (1 / years) - 1 if years > 0 else 0
    
    # Annualized Volatility
    volatility = daily_returns.std() * np.sqrt(365)
    
    # Sharpe Ratio
    sharpe_ratio = (cagr - risk_free_rate) / volatility if volatility > 0 else 0
    
    # Max Drawdown
    rolling_max = portfolio_series.cummax()
    drawdown = (portfolio_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    metrics = {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
        "Drawdown Series": drawdown
    }
    return metrics

# --- Main App ---
def main():
    inject_custom_css()
    
    # Header
    st.markdown('<div class="gradient-text">Crypto Portfolio Pro <span class="pro-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("Advanced quantitative analysis and backtesting engine for cryptocurrency portfolios.")
    st.markdown("---")
    
    # Sidebar Configuration
    st.sidebar.title("⚙️ Strategy Configuration")
    
    # 1. Investment Settings
    st.sidebar.subheader("1. Parameters")
    initial_investment = st.sidebar.number_input("Initial Investment ($)", min_value=100, max_value=10000000, value=10000, step=1000)
    timeframe_days = st.sidebar.slider("Timeframe (Days)", min_value=30, max_value=1095, value=365, step=30)
    
    # 2. Asset Selection
    st.sidebar.subheader("2. Asset Allocation")
    available_coins_dict = get_top_cryptos()
    available_coin_ids = list(available_coins_dict.keys())
    
    # Default selection
    default_coins = ['bitcoin', 'ethereum']
    selected_coins = st.sidebar.multiselect(
        "Select Assets (Max 5 recommended)",
        options=available_coin_ids,
        default=default_coins,
        format_func=lambda x: f"{available_coins_dict.get(x, x).title()} ({x})"
    )
    
    if not selected_coins:
        st.warning("Please select at least one asset to build your portfolio.")
        st.stop()
        
    if len(selected_coins) > 5:
        st.sidebar.warning("Selecting more than 5 coins may hit free API rate limits.")
        
    # 3. Weighting
    weights = {}
    st.sidebar.caption("Assign weights (must sum to 100%)")
    
    # Equal weight distribution initially
    eq_weight = int(100 / len(selected_coins))
    remainder = 100 - (eq_weight * len(selected_coins))
    
    total_weight = 0
    for i, coin in enumerate(selected_coins):
        w = eq_weight + remainder if i == 0 else eq_weight
        weight = st.sidebar.number_input(f"{available_coins_dict.get(coin, coin).title()} Weight %", min_value=0, max_value=100, value=w, key=f"w_{coin}")
        weights[coin] = weight / 100.0
        total_weight += weight
        
    if total_weight != 100:
        st.sidebar.error(f"Total weight is {total_weight}%. Must be exactly 100%.")
        st.stop()
        
    # Optional: Benchmark
    benchmark_coin = 'bitcoin'

    # --- Data Processing ---
    with st.spinner("Crunching historical market data..."):
        price_series_list = []
        
        # Fetch data for selected coins
        for coin in selected_coins:
            series = get_historical_data(coin, days=timeframe_days)
            if series is not None:
                price_series_list.append(series)
                
        # Fetch benchmark if not in selected
        if benchmark_coin not in selected_coins:
            bench_series = get_historical_data(benchmark_coin, days=timeframe_days)
            if bench_series is not None:
                price_series_list.append(bench_series)
                
        if not price_series_list:
            st.error("Failed to load any data. Please try again later.")
            st.stop()
            
        # Combine into a single DataFrame
        df_prices = pd.concat(price_series_list, axis=1).dropna()
        
        if df_prices.empty:
            st.error("Not enough overlapping historical data for selected coins.")
            st.stop()
            
        # Calculate daily normalized returns for each asset (starting at 1.0)
        df_norm = df_prices / df_prices.iloc[0]
        
        # Calculate Portfolio Value Over Time
        portfolio_val = pd.Series(0.0, index=df_norm.index)
        for coin in selected_coins:
            if coin in df_norm.columns:
                portfolio_val += df_norm[coin] * weights[coin]
                
        # Scale to initial investment
        portfolio_val = portfolio_val * initial_investment
        benchmark_val = df_norm[benchmark_coin] * initial_investment if benchmark_coin in df_norm.columns else None

    # --- Metrics Computation ---
    metrics = calculate_metrics(portfolio_val)
    # bench_metrics = calculate_metrics(benchmark_val) if benchmark_val is not None else None

    # --- Dashboard Layout ---
    
    # Row 1: KPI Cards
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Return", f"{metrics['Total Return']:.2%}", f"{(metrics['Total Return']*100):.1f}%")
    with cols[1]:
        st.metric("CAGR", f"{metrics['CAGR']:.2%}")
    with cols[2]:
        st.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}", delta_color="inverse")
    with cols[3]:
        st.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}", help="Risk-adjusted return. >1 is Good, >2 is Excellent.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Main Charts
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("📈 Portfolio Equity Curve")
        fig_equity = go.Figure()
        
        # Portfolio Line
        fig_equity.add_trace(go.Scatter(
            x=portfolio_val.index, 
            y=portfolio_val.values,
            mode='lines',
            name='Your Portfolio',
            line=dict(color='#00FF80', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 128, 0.1)'
        ))
        
        # Benchmark Line
        if benchmark_val is not None:
            fig_equity.add_trace(go.Scatter(
                x=benchmark_val.index, 
                y=benchmark_val.values,
                mode='lines',
                name=f'Benchmark ({available_coins_dict.get(benchmark_coin, benchmark_coin).title()})',
                line=dict(color='#FAFAFA', width=2, dash='dot')
            ))
            
        fig_equity.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis_title='Portfolio Value ($)',
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_equity, use_container_width=True)
        
        # Drawdown Chart
        st.subheader("📉 Drawdown Profile")
        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=metrics['Drawdown Series'].index,
            y=metrics['Drawdown Series'].values,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#FF4B4B', width=1),
            fillcolor='rgba(255, 75, 75, 0.3)',
            name='Drawdown'
        ))
        fig_dd.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            yaxis_title='Drawdown %',
            yaxis=dict(tickformat=".1%")
        )
        st.plotly_chart(fig_dd, use_container_width=True)

    with col_side:
        st.subheader("Pie Asset Allocation")
        labels = [available_coins_dict.get(c, c).title() for c in selected_coins]
        values = [weights[c] for c in selected_coins]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.6,
            marker=dict(colors=px.colors.qualitative.Pastel)
        )])
        fig_pie.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        # Fix pie chart overlap by setting height
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Correlation Heatmap (only if > 1 asset)
        if len(selected_coins) > 1:
            st.subheader("Asset Correlation")
            corr_df = df_prices[selected_coins].pct_change().corr()
            
            # Map column names to title case for better display
            display_cols = [available_coins_dict.get(c, c).title() for c in corr_df.columns]
            
            fig_corr = px.imshow(
                corr_df, 
                x=display_cols,
                y=display_cols,
                text_auto=".2f",
                color_continuous_scale='RdBu_r',
                zmin=-1, zmax=1
            )
            fig_corr.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=20, b=0),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_corr, use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("Data provided by CoinGecko API. For demonstration and proof-of-work purposes only. Not financial advice.")

if __name__ == "__main__":
    main()
