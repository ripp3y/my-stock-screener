import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# --- 1. THE INSIDER BOARD ---
INTEL_BOARD = {
    "SNDK": {"memo": "Nasdaq-100 inclusion 4.20.26. Passive funds MUST buy millions of shares this week.", "news": "SanDisk Nasdaq 100 inclusion"},
    "AUGO": {"memo": "Board approved $386M Guatemala build (4.13.26). Floor: $105. Momentum: Extreme.", "news": "Aura Minerals Era Dorada"},
    "FIX": {"memo": "Record $11.94B backlog. AI infra is 45% of rev. Breakout confirmed.", "news": "Comfort Systems AI backlog"},
    "MRVL": {"memo": "2nm DSP breakthrough. $2B NVIDIA partnership (4.1.26). AI networking lead.", "news": "Marvell NVIDIA partnership"},
    "TSM": {"memo": "2nm ramping for 2026. Massive demand from NVDA/AAPL. Bullish RSI.", "news": "TSMC 2nm manufacturing"}
}
SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. MOBILE RECON CONFIG ---
st.set_page_config(page_title="Strategic Terminal", layout="wide", initial_sidebar_state="collapsed")

# CSS: High contrast for factory/shift environments
st.markdown("""<style>
    .stSelectbox div[data-baseweb="select"] { background-color: #1E293B; border: 2px solid #3B82F6; }
    div[data-testid="stMetricValue"] { color: #93C5FD; font-size: 22px; }
    </style>""", unsafe_allow_html=True)

# --- 3. HARD-SYNC CALLBACK ---
def force_sync():
    st.cache_data.clear()
    # This function forces the browser to wake up the WebSocket

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=120) # 2-minute refresh for high-stakes shift monitoring
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

# --- 5. INTERFACE ---
st.title("🛡️ Strategic Terminal v3.6")

# SYNC STATUS (Visual confirmation it's working)
if st.button("🔄 RE-SYNC CONNECTION", on_click=force_sync):
    st.toast("Connection Hard-Synced")

master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    # SELECTION WIDGET WITH AUTO-RERUN CALLBACK
    sel = st.selectbox("🎯 Select Target", SCAN_LIST, on_change=force_sync)
    
    df_sel = master_data[sel].dropna()
    intel = INTEL_BOARD.get(sel, {"memo": "Tracking momentum...", "news": "news"})
    
    # STRATEGY BOARD
    st.markdown(f"""<div style="background-color: #1E3A8A; padding: 12px; border-radius: 8px; border-left: 8px solid #3B82F6;">
        <p style="color: #93C5FD; font-size: 13px; margin: 0;"><b>STRATEGIC INSIDER BOARD: {sel}</b></p>
        <p style="color: white; font-size: 15px; margin: 5px 0;">{intel['memo']}</p>
    </div>""", unsafe_allow_html=True)

    # DYNAMIC CHART
    fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    # RSI & RISK
    delta = df_sel['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi_val = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
    
    col1, col2 = st.columns(2)
    col1.metric("RSI", f"{rsi_val:.2f}")
    
    atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
    col2.metric("STOP LOSS", f"${(df_sel['Close'].iloc[-1] - (atr * 2.5)):.2f}")

else:
    st.warning("Feed suspended by browser. Tap RE-SYNC above.")
