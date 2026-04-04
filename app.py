import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
import random

# --- 1. CORE ARCHITECTURE ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent State Engine
if 'market_data' not in st.session_state:
    st.session_state.market_data = None
if 'sync_log' not in st.session_state:
    st.session_state.sync_log = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. STEALTH SYNC PROTOCOL ---
def execute_stealth_sync():
    try:
        # Randomized jitter to evade automated bot detection
        time.sleep(random.uniform(10.0, 15.0))
        
        # Efficient market data pull
        fresh_data = yf.download(portfolio, period="3mo", progress=False)['Close']
        
        if not fresh_data.empty:
            st.session_state.market_data = fresh_data
            st.session_state.sync_log = datetime.now().strftime("%H:%M:%S")
            st.toast("Alpha Intelligence Synced", icon="🥷")
    except Exception:
        # Retention logic: fail silently and keep cached dashboard active
        st.sidebar.error("Stealth lockout active. Stand by.")

# --- 3. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")
if st.sidebar.button("🔄 Stealth Sync"):
    execute_stealth_sync()

st.sidebar.write(f"**Status:** {'Engaged' if st.session_state.market_data is not None else 'Cool-down'}")
st.sidebar.write(f"**Last Sync:** {st.session_state.sync_log}")
st.sidebar.divider()

# --- 4. ALPHA GUARDIAN DASHBOARD ---
if st.session_state.market_data is not None:
    df = st.session_state.market_data
    st.header("🛡️ Portfolio Alpha Guardian")
    
    col_a, col_b = st.columns(2)
    with col_a:
        # Tracking for the 70.3% diversification goal
        rets = df.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.metric("Diversification Score", f"{round((1-avg_corr)*100, 1)}%")
        
    with col_b:
        # Strategic Sector Mapping
        sectors = {"Energy": 62.5, "Materials": 25.0, "Industrials": 12.5}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. PROFIT HARVEST ENGINE ---
    st.sidebar.header("📊 Profit Harvest Tool")
    asset = st.sidebar.selectbox("Select Asset", portfolio)
    basis = st.sidebar.number_input(f"Basis for {asset}", value=25.0)
    current = df[asset].iloc[-1]
    
    # Live Yield on Cost logic
    yoc = ((current / basis) - 1) * 100
    st.sidebar.metric(f"Current {asset}", f"${current:.2f}", f"{yoc:.1f}% YoC")
else:
    # Status feedback during API throttle
    st.info("💡 Terminal is in stealth cool-down. Stand by for the 15-minute API reset.")
