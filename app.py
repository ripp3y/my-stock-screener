import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- 1. CORE ARCHITECTURE ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent storage to bridge YFRateLimitError gaps
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. COMMAND CENTER (SIDEBAR) ---
st.sidebar.header("🕹️ Command Center")

# Manual sync logic to minimize API pings
if st.sidebar.button("🔄 Sync Terminal"):
    try:
        with st.spinner("Bypassing Rate Limits..."):
            # Fetch 2-month window for momentum and correlation
            data = yf.download(portfolio, period="2mo")['Close']
            st.session_state.portfolio_data = data
            st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
            st.toast("Terminal Synced Successfully!", icon="🚀")
    except Exception:
        st.sidebar.error("Yahoo Limit Active. Cool-down required.")

st.sidebar.write(f"**Last Sync:** {st.session_state.last_sync}")
st.sidebar.divider()

# --- 3. ALPHA GUARDIAN & YIELD ENGINE ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    st.header("🛡️ Portfolio Alpha Guardian")
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Correlation-based Diversification Score
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")
        st.caption(f"Status as of {st.session_state.last_sync}")
        
    with col_b:
        # Strategic Sector Mapping
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # Yield Engine - Uses session data to avoid extra calls
    st.sidebar.header("📊 Yield & Harvest Engine")
    selected = st.sidebar.selectbox("Select Asset", portfolio)
    cost_basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)
    current_p = data[selected].iloc[-1]
    st.sidebar.metric(f"Current {selected}", f"${current_p:.2f}")
else:
    # Landing state during throttling
    st.info("💡 Terminal is in cool-down. Please wait 15 minutes before hitting 'Sync Terminal'.")
