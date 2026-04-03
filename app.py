import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
import random
import os

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent state & file-backups
SAVE_FILE = "terminal_alpha_state.csv"
if 'data' not in st.session_state:
    if os.path.exists(SAVE_FILE):
        st.session_state.data = pd.read_csv(SAVE_FILE, index_col=0, parse_dates=True)
    else:
        st.session_state.data = None

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. STEALTH SYNC ENGINE ---
def execute_stealth_sync():
    try:
        # Mimic human behavior
        time.sleep(random.uniform(5.0, 8.0))
        
        fresh_data = yf.download(portfolio, period="3mo", progress=False)['Close']
        
        if not fresh_data.empty:
            st.session_state.data = fresh_data
            fresh_data.to_csv(SAVE_FILE) # Persistent backup
            st.toast("Alpha State Saved to Disk", icon="💾")
    except Exception:
        st.sidebar.error("Yahoo Lockout Active. Using Cached Alpha State.")

# --- 3. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")
if st.sidebar.button("🔄 Stealth Sync"):
    execute_stealth_sync()

st.sidebar.write(f"**Status:** {'Data Cached' if st.session_state.data is not None else 'Cool-down'}")
st.sidebar.divider()

# --- 4. ALPHA GUARDIAN DASHBOARD ---
if st.session_state.data is not None:
    df = st.session_state.data
    st.header("🛡️ Portfolio Alpha Guardian")
    
    col_a, col_b = st.columns(2)
    with col_a:
        # Tracking the 70.3% goal
        rets = df.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.metric("Diversification Score", f"{round((1-avg_corr)*100, 1)}%")
        
    with col_b:
        # Strategic Sector Mapping
        sectors = {"Energy": 62.5, "Materials": 25.0, "Industrials": 12.5}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. PROFIT HARVEST ENGINE ---
    st.sidebar.header("📊 Profit Harvest Engine")
    asset = st.sidebar.selectbox("Asset", portfolio)
    basis = st.sidebar.number_input(f"Basis for {asset}", value=25.0)
    current = df[asset].iloc[-1]
    
    yoc = ((current / basis) - 1) * 100
    st.sidebar.metric(f"Current {asset}", f"${current:.2f}", f"{yoc:.1f}% YoC")
else:
    st.info("💡 Terminal is in stealth cool-down. Wait 15 minutes before re-engaging market data.")
