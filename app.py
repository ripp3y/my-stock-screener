import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. THE NEURAL RECON BOARD (April 15, 2026) ---
INTEL_BOARD = {
    "SNDK": {"memo": "Nasdaq-100 inclusion 4.20.26. Passive rebalance imminent. Structural trend: Bullish despite Tax Day flush.", "peer": "STX"},
    "MRVL": {"memo": "$2B NVIDIA partnership (4.1.26). Bucking broader market red. AI networking anchor.", "peer": "CIEN"},
    "CIEN": {"memo": "WaveLogic 6 lead. $7B backlog. Relative strength today +0.74%. Zacks #1 Rank.", "peer": "MRVL"},
    "STX": {"memo": "AI Storage play. Pre-earnings dip before 4.28.26 report. Entering 45-RSI support zone.", "peer": "SNDK"},
    "AUGO": {"memo": "$386M Guatemala project greenlit. Support floor: $105. Record Q1 GEO production.", "peer": "GFI"},
    "FIX": {"memo": "$11.94B record backlog. AI data center infrastructure lead. Industrial sector hedge.", "peer": "EMR"},
    "ATRO": {"memo": "Defense/Aero hedge. Boeing 737 MAX contract holding. 10.3% relative strength vs sector.", "peer": "TDG"}
}
SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. MOBILE INTERFACE & SIGNAL PULSE ---
st.set_page_config(page_title="Strategic Terminal", layout="wide", initial_sidebar_state="collapsed")

# Inject High-Contrast CSS for Shift Environments
st.markdown("""<style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { color: #93C5FD; font-size: 22px; }
    .stSelectbox label { color: #93C5FD; font-weight: bold; }
    div[data-testid="stExpander"] { background-color: #1E293B; border: 1px solid #3B82F6; }
    </style>""", unsafe_allow_html=True)

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

if 'sync_time' not in st.session_state:
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=120) 
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v3.9")

# Re-Sync Status Bar
col_sync, col_time = st.columns([1, 1])
if col_sync.button("🔄 WAKE / RE-SYNC", on_click=hard_sync):
    st.toast(f"Neural Link Active: {st.session_state.sync_time}")
col_time.caption(f"Last Hard-Sync: {st.session_state.sync_time}")

master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    sel = st.selectbox("🎯 Target Recon", SCAN_LIST, on_change=hard_sync)
    df_sel = master_data[sel].dropna()
    intel = INTEL_BOARD.get(sel, {"memo": "Tracking momentum...", "peer": "N/A"})
    
    # NEURAL LINK BRIEFING
    st.markdown(f"""<div style="background-color: #1E3A8A; padding: 12px; border-radius: 8px; border-left: 8px solid #3B82F6; margin-bottom: 10px;">
        <p style="color: #93C5FD; font-size: 13px; margin: 0;"><b>STRATEGIC INSIDER BOARD: {sel}</b></p>
        <p style="color: white; font-size: 15px; margin: 5px 0;">{intel['memo']}</p>
        <p style="color: #60A5FA; font-size: 11px; margin: 0;">Correlated Peer: {intel['peer']}</p>
    </div>""", unsafe_allow_html=True)

    # DUAL-MODE RECON (Charts & Multi-Timeframe)
    tab_live, tab_neural = st.tabs(["📊 Live Recon", "🧠 Neural Analysis"])
    
    with tab_live:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # KEY METRICS
        delta = df_sel['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi_val = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Current RSI", f"{rsi_val:.2f}")
        
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        stop_loss = df_sel['Close'].iloc[-1] - (atr * 2.5)
        col_m2.metric("Defense Floor", f"${stop_loss:.2f}")

    with tab_neural:
        st.write("### Sector-Relative Strength")
        # Relative strength logic compared to S&P 500 placeholder
        spy = yf.download("SPY", period="1y", progress=False)['Close'].ffill()
        rel_strength = (df_sel['Close'] / spy).pct_change(20).iloc[-1] * 100
        st.metric("20-Day Relative Strength", f"{rel_strength:.2f}%", delta_color="normal")
        st.caption("Performance vs. S&P 500 over the last 20 trading days.")

else:
    st.error("Feed Paused. Tap 'WAKE CONNECTION' above.")
