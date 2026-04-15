import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. NEURAL LINK (Strategic Insider Board) ---
INTEL_BOARD = {
    "AUGO": {
        "memo": "Era Dorada construction greenlit (4.14.26). $386M+ capex. Floor: $105.",
        "news": "Aura Minerals Era Dorada gold production"
    },
    "FIX": {
        "memo": "Record $11.94B backlog (99% YoY growth). AI infrastructure = 45% revenue.",
        "news": "Comfort Systems AI data center backlog"
    },
    "MRVL": {
        "memo": "2nm DSP breakthrough. $2B NVIDIA partnership for AI interconnects.",
        "news": "Marvell 2nm chip NVIDIA partnership"
    },
    "SNDK": {
        "memo": "Nasdaq-100 inclusion on 4.20.26. Passive fund buying surge expected.",
        "news": "SanDisk Nasdaq 100 inclusion index buying"
    },
    "TSM": {
        "memo": "2nm node ramping for 2026. High demand from NVDA/AAPL clusters.",
        "news": "TSMC 2nm node manufacturing news"
    }
}

SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. MOBILE OPTIMIZATION CONFIG ---
st.set_page_config(page_title="Strategic Terminal", layout="wide", initial_sidebar_state="collapsed")

# CSS: Better contrast and larger touch targets for phone use
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { font-size: 20px; color: #93C5FD; }
    .stSelectbox label { color: #93C5FD; font-size: 16px; font-weight: bold; }
    div[data-testid="stExpander"] { background-color: #1E293B; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data(ttl="5m") # Short TTL to ensure you see fresh price action every break
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

def calculate_rsi(data):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v3.3")

master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    # 1. Target Recon Selection
    sel = st.selectbox("🎯 Target Recon Selection", SCAN_LIST)
    df_sel = master_data[sel].dropna()
    rsi_val = calculate_rsi(df_sel['Close']).iloc[-1]
    
    # 2. THE INSIDER BOARD (Detailed Strategy Alert)
    intel = INTEL_BOARD.get(sel, {"memo": "Tracking institutional momentum...", "news": "stock news"})
    
    st.markdown(f"""
        <div style="background-color: #1e3a8a; padding: 12px; border-radius: 8px; border-left: 8px solid #3b82f6; margin-bottom: 10px;">
            <p style="color: #93c5fd; font-size: 13px; margin: 0;"><b>STRATEGIC INSIDER BOARD: {sel}</b></p>
            <p style="color: white; font-size: 15px; margin: 5px 0;">{intel['memo']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Link to Search Targets
    st.markdown(f"[🔍 Tap for {sel} Strategic News](https://www.google.com/search?q={sel}+{intel['news'].replace(' ', '+')}+news&tbm=nws)")

    # 3. CHART & ALERTS
    tab_chart, tab_risk = st.tabs(["📊 Live Chart", "🛡️ Risk Recon"])
    
    with tab_chart:
        # Candle Chart (Responsive for Phone Screens)
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=320, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # Dual-Col RSI and Action Order
        col_rsi, col_alert = st.columns([1, 2])
        col_rsi.metric("RSI", f"{rsi_val:.2f}")
        
        # Strategy Alert Logic
        if rsi_val > 80: a_msg, a_bg = "🔥 EXTREME MOMENTUM", "#7f1d1d"
        elif rsi_val > 70: a_msg, a_bg = "⚠️ OVERBOUGHT", "#991b1b"
        elif rsi_val > 55: a_msg, a_bg = "🚀 BULLISH TREND", "#1e3a8a"
        else: a_msg, a_bg = "⚖️ NEUTRAL", "#1f2937"
        
        col_alert.markdown(f'<div style="background-color: {a_bg}; padding: 10px; border-radius: 8px; text-align: center; color: white; margin-top: 5px;"><b>{a_msg}</b></div>', unsafe_allow_html=True)

    with tab_risk:
        cp = df_sel['Close'].iloc[-1]
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        st.markdown(f"""
            <div style="background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #374151;">
                <p style="color: #9CA3AF; margin:0;">Recommended Stop Loss</p>
                <p style="color: #F87171; font-size: 24px; margin:0;"><b>${(cp - (atr * 2.5)):.2f}</b></p>
                <p style="color: #9CA3AF; margin-top:10px; font-size: 12px;">Based on 2.5x ATR volatility</p>
            </div>
        """, unsafe_allow_html=True)

else:
    # This message helps you know if you need to refresh the page on your phone
    st.error("Connection Timed Out. Please refresh your browser page to re-sync.")
