import streamlit as st
import pandas as pd
import yfinance as yf
import sys
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v9.00", layout="wide")

# --- [2. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [3. HEADER & COUNTDOWN] ---
earnings_date = datetime(2026, 5, 5)
days_to_earnings = (earnings_date - datetime.now()).days

st.title("📟 Strategic Terminal v9.00")
col_info, col_countdown = st.columns([3, 1])
with col_info:
    st.caption(f"Engine: Python {sys.version.split()[0]} | Status: 🟢 FULL INTELLIGENCE")
with col_countdown:
    # High-visibility countdown for your lead stock
    st.metric("NVTS Earnings Countdown", f"{days_to_earnings} Days", delta="-1" if days_to_earnings > 0 else "LIVE")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_solar = st.tabs(["📊 RECON", "₿ CRYPTO & MINERS", "☀️ SOLAR"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                curr = data[t]['Close'].iloc[-1]
                recon_list.append({
                    "Ticker": t, "Price": f"${curr:.2f}", 
                    "20% Target": f"${curr * 1.20:.2f}",
                    "Mission Status": "🚀 Blue Sky" if t == "NVTS" else "🟢 Steady"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list).style.set_properties(**{'background-color': '#0d0d0d', 'color': '#00FF00'}, subset=['Ticker']))
        
        st.divider()
        target = st.selectbox("Deep-Dive Inspection:", portfolio)
        st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO & MINERS] ---
with tab_crypto:
    st.subheader("₿ Asset Velocity")
    # MARA and IREN are moving with BTC's $78k test
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(crypto_list)
    
    if c_data is not None:
        for c in crypto_list:
            col_c1, col_c2 = st.columns([1, 2])
            with col_c1:
                price = c_data[c]['Close'].iloc[-1]
                st.metric(c, f"${price:,.2f}")
            with col_c2:
                st.line_chart(c_data[c]['Close'].tail(30), height=100)

# --- [TAB 3: SOLAR] ---
with tab_solar:
    st.subheader("☀️ Enphase Monitoring Bridge")
    st.info("System Ready. Waiting for local Envoy API handshake...")
    # Placeholder for your local energy metrics
    st.metric("Today's Production", "0.0 kWh", delta="0%")
    st.caption("Monitoring Zeo Energy installation at Galax property.")
