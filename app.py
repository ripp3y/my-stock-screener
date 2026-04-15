import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. NEURAL DATA RECON (April 15, 2026) ---
GUARDIAN_INTEL = {
    "SNDK": {"price": 880.22, "change": -6.80, "support": 873.93, "institutional": "92.4%"},
    "MRVL": {"price": 132.81, "change": -0.76, "support": 132.29, "institutional": "78.4%"},
    "CIEN": {"price": 460.47, "change": -1.45, "support": 454.34, "institutional": "97.8%"},
    "STX": {"price": 507.77, "change": -4.81, "support": 503.11, "institutional": "94.2%"},
    "AUGO": {"price": 105.01, "change": -3.35, "support": 103.47, "institutional": "42.0%"}
}

# --- 2. THE SIGNAL PULSE ---
st.set_page_config(page_title="Strategic Terminal v3.13", layout="wide")

if 'sync' not in st.session_state: st.session_state.sync = datetime.now().strftime("%H:%M:%S")

st.title("🛡️ Strategic Command Center v3.13")
st.caption(f"Neural Link Active | Last Handshake: {st.session_state.sync}")

# --- 3. LIVE TARGET RECON ---
target = st.selectbox("🎯 Target Analysis", list(GUARDIAN_INTEL.keys()))
intel = GUARDIAN_INTEL[target]

# LIVE CHART INTEGRATION
@st.cache_data(ttl=60)
def get_chart_data(ticker):
    # Fetching 5-day view to visualize the Tax Day Flush
    return yf.download(ticker, period="5d", interval="15m", progress=False)

df = get_chart_data(target)

if not df.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#22C55E', decreasing_line_color='#EF4444'
    )])
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# THE COMMAND TILES
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Live Price", f"${intel['price']}", f"{intel['change']}%")
with col2:
    st.metric("Institutional Support", intel['institutional'])
with col3:
    st.metric("Guardian Floor (Low)", f"${intel['support']}")

st.divider()
st.info(f"💡 Strategy: {target} is currently testing its daily floor. Holding for the April 20 liquidity pivot.")
