import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. THE UNIFIED INSIDER BOARD (April 15, 2026) ---
INTEL_BOARD = {
    "SNDK": {"memo": "Nasdaq-100 inclusion 4.20.26. Massive rebalance this week. Front-running target: $1k.", "news": "SanDisk Nasdaq 100 inclusion"},
    "AUGO": {"memo": "Record Q1 production (82k oz). $386M Guatemala project greenlit. Target: 111k oz/yr.", "news": "Aura Minerals gold production record"},
    "FIX": {"memo": "$11.94B record backlog. 45% AI data center exposure. Dividend raised to $0.70.", "news": "Comfort Systems AI data center backlog"},
    "MRVL": {"memo": "$2B NVIDIA investment (3.31.26). NVLink Fusion networking lead. Bucking Tax Day red.", "news": "Marvell NVIDIA AI partnership"},
    "CIEN": {"memo": "Zacks #1 Rank. Optical AI networking leader. $5B in AI orders expected in FY2026.", "news": "Ciena AI networking orders record"},
    "STX": {"memo": "AI storage boom. Pre-earnings run expected before 4.28.26 report. Bullish P/S re-rating.", "news": "Seagate AI storage demand earnings"},
    "ATRO": {"memo": "Boeing 737 MAX contract (3.20.26). Defense hedge with 10.3% relative strength vs sector.", "news": "Astronics Boeing contract defense demand"}
}
SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. MOBILE RECON CONFIG ---
st.set_page_config(page_title="Strategic Terminal", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { color: #93C5FD; font-size: 20px; }
    .stSelectbox label { color: #93C5FD; font-weight: bold; }
    </style>""", unsafe_allow_html=True)

# --- 3. THE "SIGNAL PULSE" (Prevents Mobile Freeze) ---
def hard_sync():
    st.cache_data.clear()
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

if 'sync_time' not in st.session_state:
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=120) 
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

# --- 5. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v3.8")

if st.button("🔄 WAKE CONNECTION / RE-SYNC", on_click=hard_sync):
    st.toast(f"Terminal Synced at {st.session_state.sync_time}")

master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    sel = st.selectbox("🎯 Target Recon", SCAN_LIST, on_change=hard_sync)
    df_sel = master_data[sel].dropna()
    intel = INTEL_BOARD.get(sel, {"memo": "Tracking momentum...", "news": "news"})
    
    # STRATEGY ALERT BOARD
    st.markdown(f"""<div style="background-color: #1E3A8A; padding: 12px; border-radius: 8px; border-left: 8px solid #3B82F6; margin-bottom: 10px;">
        <p style="color: #93C5FD; font-size: 13px; margin: 0;"><b>STRATEGIC INSIDER BOARD: {sel}</b></p>
        <p style="color: white; font-size: 15px; margin: 5px 0;">{intel['memo']}</p>
        <p style="color: #93C5FD; font-size: 11px; margin: 0;">Last Hard-Sync: {st.session_state.sync_time}</p>
    </div>""", unsafe_allow_html=True)

    # LIVE CHART
    fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    # METRICS
    delta = df_sel['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi_val = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
    
    col1, col2 = st.columns(2)
    col1.metric("RSI", f"{rsi_val:.2f}")
    
    atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
    col2.metric("STOP LOSS", f"${(df_sel['Close'].iloc[-1] - (atr * 2.5)):.2f}")

else:
    st.error("Feed Paused. Tap 'WAKE CONNECTION' above.")
