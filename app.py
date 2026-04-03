import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- 1. TERMINAL CONFIGURATION ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Initialize persistent session storage
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. COMMAND CENTER (SIDEBAR) ---
st.sidebar.header("🕹️ Command Center")

# Sync function to handle Yahoo Finance blocks
if st.sidebar.button("🔄 Sync Terminal"):
    try:
        with st.spinner("Bypassing Rate Limits..."):
            # Download price data
            data = yf.download(portfolio, period="2mo")['Close']
            st.session_state.portfolio_data = data
            st.session_state.last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.toast("Alpha Data Synced!", icon="🚀")
    except Exception as e:
        st.sidebar.error("Yahoo Finance still throttling. Wait 15 mins.")

st.sidebar.write(f"**Last Sync:** {st.session_state.last_sync}")
st.sidebar.divider()

# --- 3. ALPHA GUARDIAN DASHBOARD ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    # Portfolio Analysis logic
    st.header("🛡️ Portfolio Alpha Guardian")
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Diversification Math
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")
        st.caption(f"Sync Timestamp: {st.session_state.last_sync}")
        
    with col_b:
        # Sector Weighting
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # --- 4. YIELD & HARVEST ENGINE ---
    st.sidebar.header("📊 Yield & Harvest Engine")
    selected = st.sidebar.selectbox("Select Asset", portfolio)
    basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)
    
    # Static logic to avoid extra API calls
    price = data[selected].iloc[-1]
    st.sidebar.metric(f"Current {selected}", f"${price:.2f}")
else:
    # Landing state when rate limited
    st.info("💡 Terminal is in cool-down. Click 'Sync Terminal' to attempt data fetch.")
