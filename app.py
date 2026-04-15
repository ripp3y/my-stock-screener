import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. THE NEURAL RECON BOARD (April 15, 2026) ---
INTEL_BOARD = {
    "SNDK": {"memo": "Nasdaq-100 inclusion 4.20.26. Passive funds managing $600B+ forced to buy. Structural trend: Bullish.", "peer": "STX"},
    "MRVL": {"memo": "$2B NVIDIA partnership (4.1.26). Bucking Tax Day red. AI networking anchor.", "peer": "CIEN"},
    "CIEN": {"memo": "WaveLogic 6 lead. $7B backlog. Relative strength +0.74%. Zacks #1 Rank.", "peer": "MRVL"},
    "STX": {"memo": "AI Storage boom. Pre-earnings dip before 4.28.26 report. Entering 45-RSI support.", "peer": "SNDK"},
    "AUGO": {"memo": "$386M Guatemala project greenlit. Support floor: $105. Record Q1 production.", "peer": "GFI"},
    "FIX": {"memo": "$11.94B record backlog. 45% AI data center exposure. Industrial sector hedge.", "peer": "EMR"},
    "ATRO": {"memo": "Defense/Aero hedge. Boeing 737 MAX contract holding. 10.3% relative strength.", "peer": "TDG"}
}
SCAN_LIST = list(INTEL_BOARD.keys()) + ["NVDA", "AMD", "AAPL", "MSFT"]

# --- 2. MOBILE INTERFACE & ERROR SHIELD ---
st.set_page_config(page_title="Strategic Terminal", layout="wide", initial_sidebar_state="collapsed")

def hard_sync():
    st.cache_data.clear()
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

if 'sync_time' not in st.session_state:
    st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")

@st.cache_data(ttl=120) 
def fetch_prices(tickers):
    try: return yf.download(list(tickers), period="1y", group_by='ticker', progress=False).ffill()
    except: return None

# --- 3. MAIN INTERFACE ---
st.title("🛡️ Strategic Terminal v3.10")

if st.button("🔄 WAKE / RE-SYNC", on_click=hard_sync):
    st.toast("Neural Link Repaired.")

master_data = fetch_prices(SCAN_LIST)

if master_data is not None:
    sel = st.selectbox("🎯 Target Recon", SCAN_LIST, on_change=hard_sync)
    df_sel = master_data[sel].dropna()
    intel = INTEL_BOARD.get(sel, {"memo": "Tracking momentum...", "peer": "N/A"})
    
    st.markdown(f"""<div style="background-color: #1E3A8A; padding: 12px; border-radius: 8px; border-left: 8px solid #3B82F6; margin-bottom: 10px;">
        <p style="color: white; font-size: 15px; margin: 5px 0;"><b>{sel} BRIEF:</b> {intel['memo']}</p>
        <p style="color: #60A5FA; font-size: 11px; margin: 0;">Last Hard-Sync: {st.session_state.sync_time}</p>
    </div>""", unsafe_allow_html=True)

    tab_live, tab_neural = st.tabs(["📊 Live Recon", "🧠 Neural Analysis"])
    
    with tab_live:
        fig = go.Figure(data=[go.Candlestick(x=df_sel.index, open=df_sel['Open'], high=df_sel['High'], low=df_sel['Low'], close=df_sel['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        delta = df_sel['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi_val = 100 - (100 / (1 + (gain / (loss + 1e-9)))).iloc[-1]
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Current RSI", f"{float(rsi_val):.2f}")
        
        atr = (df_sel['High'] - df_sel['Low']).rolling(14).mean().iloc[-1]
        stop_loss = df_sel['Close'].iloc[-1] - (atr * 2.5)
        col_m2.metric("Defense Floor", f"${float(stop_loss):.2f}")

    with tab_neural:
        st.write("### Sector-Relative Strength (vs SPY)")
        try:
            # FIX: Using robust calculation to prevent TypeError
            spy_data = yf.download("SPY", period="1y", progress=False)['Close']
            rel_strength = ((df_sel['Close'].iloc[-1] / df_sel['Close'].iloc[-20]) / 
                            (spy_data.iloc[-1] / spy_data.iloc[-20]) - 1) * 100
            # FIX: Explicitly convert to float to prevent format error
            st.metric("20-Day Rel. Strength", f"{float(rel_strength):.2f}%")
        except:
            st.warning("Relative Strength feed calibrating...")

else:
    st.error("Feed Paused. Tap 'WAKE CONNECTION' above.")
