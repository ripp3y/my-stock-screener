import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- 1. RESILIENT DATA ARCHITECTURE ---
# Cache portfolio prices for 1 hour to prevent 429 errors
@st.cache_data(ttl=3600)
def fetch_resilient_data(tickers):
    try:
        return yf.download(tickers, period="2mo")['Close']
    except Exception:
        return None

# Cache ticker info (Dividends/Beta) for 24 hours as it changes slowly
@st.cache_data(ttl=86400)
def fetch_ticker_stats(ticker):
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}

st.set_page_config(page_title="Strategic US Terminal", layout="wide")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]
raw_data = fetch_resilient_data(portfolio)

if raw_data is not None:
    # --- 2. YIELD ENGINE ---
    st.sidebar.header("📊 Yield & Harvest Engine")
    selected = st.sidebar.selectbox("Select Asset", portfolio)
    cost_basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)

    stats = fetch_ticker_stats(selected)
    div_y = stats.get('dividendYield', 0)
    
    if div_y:
        ann_div = div_y * raw_data[selected].iloc[-1]
        yoc = (ann_div / cost_basis) * 100
        st.sidebar.metric("Yield on Cost", f"{round(yoc, 2)}%")
    
    # --- 3. ALPHA GUARDIAN VISUALS ---
    st.header("🛡️ Portfolio Alpha Guardian")
    col_a, col_b = st.columns(2)
    
    with col_a:
        rets = raw_data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

    with col_b:
        # Static weights based on your current strategy
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("🛑 Yahoo Finance Rate Limit Active. Please wait 15-30 minutes for the reset.")
