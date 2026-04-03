import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- 1. CORE ARCHITECTURE ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent state to bridge API lockout periods
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")

if st.sidebar.button("🔄 Sync Terminal"):
    try:
        with st.spinner("Bypassing Throttling..."):
            # Fetching fresh alpha data
            new_data = yf.download(portfolio, period="2mo")['Close']
            if not new_data.empty:
                st.session_state.portfolio_data = new_data
                st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
                st.toast("Sync Complete!", icon="🚀")
    except Exception:
        # Silently fail and keep old data visible
        st.sidebar.error("Yahoo Lockout Active. Try again in 15m.")

st.sidebar.write(f"**Status**: {'Ready' if st.session_state.portfolio_data is not None else 'Initial Sync Needed'}")
st.sidebar.write(f"**Last Update**: {st.session_state.last_sync}")
st.sidebar.divider()

# --- 3. ALPHA GUARDIAN & YIELD ENGINE ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    st.header("🛡️ Portfolio Alpha Guardian")
    col1, col2 = st.columns(2)
    
    with col1:
        # High-Conviction Diversification Score
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.metric("Diversification Score", f"{round((1-avg_corr)*100, 1)}%")
        
    with col2:
        # Strategic Sector Weights
        sectors = {"Energy": 62.5, "Materials": 25.0, "Industrials": 12.5}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # Yield & Harvest Tool
    st.sidebar.header("📊 Yield & Harvest Tool")
    selected = st.sidebar.selectbox("Asset", portfolio)
    basis = st.sidebar.number_input(f"Basis for {selected}", value=25.0)
    current = data[selected].iloc[-1]
    
    st.sidebar.metric(f"Current Price", f"${current:.2f}", 
                     f"{((current/basis)-1)*100:.1f}% Yield")
else:
    # Landing state during cool-down
    st.info("💡 Terminal is currently in cool-down mode. Click 'Sync Terminal' to attempt a data refresh.")
