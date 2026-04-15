import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. NEURAL LINK (Strategic Insider Board) ---
INTEL_BOARD = {
    "SNDK": {"memo": "Nasdaq-100 inclusion 4.20.26. Passive funds MUST buy millions of shares this week. Signal: Golden Cross.", "news": "SanDisk Nasdaq 100 inclusion"},
    "AUGO": {"memo": "Board approved $386M Guatemala build (4.13.26). Target: 111k oz gold/yr. Floor: $105.", "news": "Aura Minerals Era Dorada"},
    "FIX": {"memo": "Record $11.94B backlog (up 99% YoY). AI data centers = 45% rev. Breakout holding.", "news": "Comfort Systems AI backlog"},
    "MRVL": {"memo": "2nm DSP breakthrough. $2B NVIDIA partnership (4.1.26). AI networking lead.", "news": "Marvell NVIDIA 2nm partnership"},
    "TSM": {"memo": "2nm node ramping for 2026. High demand from NVDA/AAPL clusters. Bullish RSI.", "news": "TSMC 2nm manufacturing"}
}
SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. MOBILE RECON CONFIG ---
st.set_page_config(page_title="Strategic Terminal", layout="wide", initial_sidebar_state="collapsed")

# CSS: High-contrast mobile colors
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
st.title("🛡️ Strategic Terminal v3.7")

# The Sync Button acts as a "Wake Up" for the browser
if st.button("🔄 WAKE CONNECTION / RE-SYNC", on_click=hard_sync):
    st.toast(f"Terminal Synced at {st.session_state.sync_time}")

master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    # Target Selection with Auto-Wake Callback
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
