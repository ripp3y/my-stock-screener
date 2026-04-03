import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- 1. CORE ARCHITECTURE ---
st.set_page_config(page_title="Strategic US Terminal", layout="wide")

# Persistent storage to handle YFRateLimitError
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'last_sync' not in st.session_state:
    st.session_state.last_sync = "Never"

portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF", "XOM", "CVX", "GEV"]

# --- 2. COMMAND CENTER ---
st.sidebar.header("🕹️ Command Center")

if st.sidebar.button("🔄 Sync Terminal"):
    try:
        with st.spinner("Synchronizing with Market..."):
            # Fetch Close prices for the 2-month alpha window
            data = yf.download(portfolio, period="2mo")['Close']
            st.session_state.portfolio_data = data
            st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
            st.toast("Terminal Synced!", icon="🚀")
    except Exception:
        st.sidebar.error("Yahoo Limit Active. Cooling down...")

st.sidebar.write(f"**Last Sync:** {st.session_state.last_sync}")
st.sidebar.divider()

# --- 3. ALPHA GUARDIAN & YIELD ENGINE ---
if st.session_state.portfolio_data is not None:
    data = st.session_state.portfolio_data
    
    st.header("🛡️ Portfolio Alpha Guardian")
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation-based Diversification Score
        rets = data.pct_change().dropna()
        avg_corr = rets.corr().where(np.triu(np.ones(len(portfolio)), k=1).astype(bool)).stack().mean()
        st.write(f"## Diversification Score: {round((1-avg_corr)*100, 1)}%")
        st.caption(f"Based on data from {st.session_state.last_sync}")
        
    with col2:
        # Strategic Sector View
        sectors = {"Energy": 5, "Materials": 2, "Industrials": 1}
        fig = px.pie(values=list(sectors.values()), names=list(sectors.keys()), hole=.4)
        st.plotly_chart(fig, use_container_width=True)

    # Yield Engine - uses data from st.session_state
    st.sidebar.header("📊 Yield Engine")
    selected = st.sidebar.selectbox("Select Asset", portfolio)
    cost = st.sidebar.number_input(f"Avg Cost for {selected}", value=25.0)
    current_p = data[selected].iloc[-1]
    st.sidebar.metric(f"Price: {selected}", f"${current_p:.2f}")
else:
    # Landing state during rate-limiting
    st.info("💡 Terminal is in cool-down. Please wait 15 minutes before hitting 'Sync Terminal'.")
