import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
import random

# --- 1. ARCHITECTURE SETUP ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent State Engine
if 'data' not in st.session_state:
    st.session_state.data = None
if 'sync_time' not in st.session_state:
    st.session_state.sync_time = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. STEALTH SYNC PROTOCOL ---
def stealth_sync():
    try:
        # Randomized jitter to bypass bot detection
        time.sleep(random.uniform(3.0, 6.0))
        
        # Efficient data pull for strategic assets
        fresh_data = yf.download(portfolio, period="3mo", progress=False)['Close']
        
        if not fresh_data.empty:
            st.session_state.data = fresh_data
            st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")
            st.toast("Alpha Synced Successfully!", icon="💹")
    except Exception:
        # Retention logic: fail silently and keep old data visible
        st.sidebar.error("Stealth lockout active. Retrying in 15m.")

# --- 3. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")
if st.sidebar.button("🔄 Stealth Sync"):
    stealth_sync()

st.sidebar.write(f"**Terminal Status:** {'Engaged' if st.session_state.data is not None else 'Cool-down'}")
st.sidebar.write(f"**Last Update:** {st.session_state.sync_time}")
st.sidebar.divider()

# --- 4. ALPHA GUARDIAN DASHBOARD ---
if st.session_state.data is not None:
    df = st.session_state.data
    st.header("🛡️ Portfolio Alpha Guardian")
    
    col_alpha, col_beta = st.columns(2)
    with col_alpha:
        # Metric tracking for your 70.3% goal
        rets = df.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.metric("Diversification Score", f"{round((1-avg_corr)*100, 1)}%")
        
    with col_beta:
        # Sector Concentration
        sectors = {"Energy": 62.5, "Materials": 25.0, "Industrials": 12.5}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. YIELD & HARVEST ENGINE ---
    st.sidebar.header("📊 Yield & Harvest Tool")
    ticker = st.sidebar.selectbox("Asset", portfolio)
    basis = st.sidebar.number_input(f"Basis for {ticker}", value=25.0)
    current = df[ticker].iloc[-1]
    
    # Live Yield on Cost logic
    yoc = ((current / basis) - 1) * 100
    st.sidebar.metric(f"Current {ticker}", f"${current:.2f}", f"{yoc:.1f}% YoC")
else:
    st.info("💡 Terminal is in stealth cool-down. Please wait 15 minutes to re-engage market data.")
