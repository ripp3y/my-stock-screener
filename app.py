import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
import random

st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# --- 1. PERSISTENT STATE ENGINE ---
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. RESILIENT SYNC FUNCTION ---
def sync_with_stealth():
    try:
        # Add a small random delay to avoid bot detection
        time.sleep(random.uniform(1.5, 3.5))
        
        # Pull data using the internal download method
        new_data = yf.download(portfolio, period="2mo", progress=False)['Close']
        
        if not new_data.empty:
            st.session_state.portfolio_data = new_data
            st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
            st.toast("Stealth Sync Successful!", icon="🥷")
    except Exception as e:
        st.sidebar.error("Yahoo still enforcing lockout. Wait 15-30 mins.")

# --- 3. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")
if st.sidebar.button("🔄 Stealth Sync"):
    sync_with_stealth()

st.sidebar.write(f"**Last Update:** {st.session_state.last_sync}")
st.sidebar.divider()

# --- 4. ALPHA GUARDIAN DASHBOARD ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    st.header("🛡️ Portfolio Alpha Guardian")
    col_a, col_b = st.columns(2)
    
    with col_a:
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        # Visualizing your 70.3% target
        st.metric("Diversification Score", f"{round((1-avg_corr)*100, 1)}%")
        
    with col_b:
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. YIELD ENGINE ---
    st.sidebar.header("📊 Yield & Harvest Tool")
    selected = st.sidebar.selectbox("Asset", portfolio)
    basis = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)
    price = data[selected].iloc[-1]
    
    st.sidebar.metric(f"Current {selected}", f"${price:.2f}")
    st.sidebar.caption(f"Yield on Cost: {round(((price/basis)-1)*100, 2)}%")
else:
    st.info("💡 Terminal is cooling down. Use 'Stealth Sync' in 15 minutes to refresh data.")
