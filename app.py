import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. RESILIENT DATA FETCHING ---
# Cache data for 15 mins (900 seconds) to avoid Rate Limits
@st.cache_data(ttl=900)
def get_portfolio_data(tickers):
    try:
        data = yf.download(tickers, period="2mo")['Close']
        return data
    except Exception as e:
        st.error(f"Throttling Detected: {e}")
        return None

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = get_portfolio_data(portfolio)

if raw_data is not None:
    # --- 2. YIELD & HARVEST ENGINE ---
    st.sidebar.header("📊 Yield & Harvest Engine")
    selected = st.sidebar.selectbox("Select Asset", portfolio, index=0)
    cost_basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)

    # Cache Ticker Info to avoid redundant API calls
    @st.cache_data(ttl=3600)
    def get_ticker_info(ticker):
        return yf.Ticker(ticker).info

    info = get_ticker_info(selected)
    div_y = info.get('dividendYield', 0)
    if div_y:
        ann_div = div_y * raw_data[selected].iloc[-1]
        yoc = (ann_div / cost_basis) * 100
        st.sidebar.metric("Yield on Cost", f"{round(yoc, 2)}%")

    # --- 3. HARVEST TOOL & ALPHA GUARDIAN ---
    # (Previous logic for Diversification Score and Sector Pie remains stable)
    st.sidebar.divider()
    st.sidebar.header("💰 Profit Harvest Tool")
    h_ticker = st.sidebar.selectbox("Trim Target", ["EQNR", "CF"])
    h_cash = (98 * 0.5) * raw_data[h_ticker].iloc[-1]
    st.sidebar.success(f"Harvested Cash: ${h_cash:,.2f}")

    st.header("🛡️ Portfolio Alpha Guardian")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        rets = raw_data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")

    with col_b:
        sectors = {"Energy": ["PBR", "EQNR", "CNQ", "XOM", "CVX"], "Materials": ["CENX", "CF"], "Industrials": ["GEV"]}
        weight_data = pd.DataFrame([{"Sector": s, "Weight": len(t)} for s, t in sectors.items()])
        fig = px.pie(weight_data, values='Weight', names='Sector', hole=.4, height=350)
        st.plotly_chart(fig)
else:
    st.warning("🔄 System cooling down. Data will refresh shortly once rate limits reset.")
