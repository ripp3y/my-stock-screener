import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
import random

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent storage to handle API lockout periods
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. STEALTH SYNC ENGINE ---
def execute_stealth_sync():
    try:
        # Randomized delay to mimic human behavior
        time.sleep(random.uniform(2.0, 4.5))
        
        # Pull data with suppressed progress bars to save bandwidth
        new_data = yf.download(portfolio, period="2mo", progress=False)['Close']
        
        if not new_data.empty:
            st.session_state.portfolio_data = new_data
            st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
            st.toast("Stealth Alpha Synced!", icon="🥷")
    except Exception:
        # Graceful failure: retain old data for dashboard continuity
        st.sidebar.error("Yahoo Lockout Persistent. Stand by.")

# --- 3. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")
if st.sidebar.button("🔄 Stealth Sync"):
    execute_stealth_sync()

st.sidebar.write(f"**Last Sync:** {st.session_state.last_sync}")
st.sidebar.divider()

# --- 4. ALPHA GUARDIAN DASHBOARD ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    st.header("🛡️ Portfolio Alpha Guardian")
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation-based Alpha Check
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.metric("Diversification Score", f"{round((1-avg_corr)*100, 1)}%")
        st.caption(f"Status as of {st.session_state.last_sync}")
        
    with col2:
        # Strategic Sector Mapping
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. YIELD & HARVEST ENGINE ---
    st.sidebar.header("📊 Yield & Harvest Tool")
    selected = st.sidebar.selectbox("Select Asset", portfolio)
    cost = st.sidebar.number_input(f"Basis for {selected}", value=25.0)
    current_p = data[selected].iloc[-1]
    
    # Calculate Yield on Cost dynamically
    yoc = ((current_p / cost) - 1) * 100
    st.sidebar.metric(f"Current {selected}", f"${current_p:.2f}", f"{yoc:.2f}% YoC")
else:
    # Landing state during rate-limiting
    st.info("💡 Terminal is in stealth cool-down. Use 'Stealth Sync' in 15 minutes to re-engage.")
