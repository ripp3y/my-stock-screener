import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Initialize persistent session state
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. COMMAND CENTER (SIDEBAR) ---
st.sidebar.header("🕹️ Command Center")

# Manual Sync to bypass YFRateLimitError
if st.sidebar.button("🔄 Sync Terminal"):
    try:
        with st.spinner("Fetching Market Data..."):
            data = yf.download(portfolio, period="2mo")['Close']
            st.session_state.portfolio_data = data
            st.session_state.last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.toast("Terminal Synced!", icon="🚀")
    except Exception as e:
        st.error(f"Sync Interrupted: {e}")

st.sidebar.write(f"**Last Update:** {st.session_state.last_sync}")
st.sidebar.divider()

# --- 3. YIELD & HARVEST ENGINE ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    st.sidebar.header("📊 Yield & Harvest Engine")
    selected = st.sidebar.selectbox("Select Asset", portfolio)
    cost_basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)
    
    # Static info fetch for current price
    current_price = data[selected].iloc[-1]
    st.sidebar.metric(f"Current {selected}", f"${current_price:.2f}")

    # --- 4. ALPHA GUARDIAN VISUALIZATION ---
    st.header("🛡️ Portfolio Alpha Guardian")
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Correlation-based Diversification Score
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")
        st.caption(f"Status updated at {st.session_state.last_sync}")
        
    with col_right:
        # Strategic Sector Mapping
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)
else:
    # Initial landing state
    st.info("💡 Click 'Sync Terminal' in the sidebar to load your portfolio data.")
