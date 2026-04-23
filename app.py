import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.8", layout="wide")

# --- [2. HARDENED FETCH ENGINE] ---
@st.cache_data(ttl=300)
def get_verified_data(ticker):
    """Downloads data and verifies it isn't empty before passing it to the app."""
    try:
        # We add 'repair=True' to fix common Yahoo data glitches
        df = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, repair=True, progress=False)
        
        # Check if the data is actually there
        if df is None or df.empty or len(df) < 5:
            return None
        return df
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v10.8")
st.caption("Engine: v10.8 | Status: VERIFYING CONNECTION | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_list = []
    
    with st.spinner("Connecting to Yahoo..."):
        for t in portfolio:
            data = get_verified_data(t)
            if data is not None:
                try:
                    curr_p = float(data['Close'].iloc[-1])
                    recon_list.append({
                        "Ticker": t,
                        "Price": f"${curr_p:.2f}",
                        "20% Target": f"${curr_p * 1.20:.2f}",
                        "Signal": "🟢 BULLISH" if curr_p > data['Close'].tail(20).mean() else "🟡 NEUTRAL"
                    })
                except: continue

    if recon_list:
        st.table(pd.DataFrame(recon_list))
        st.divider()
        nvts_data = get_verified_data("NVTS")
        if nvts_data is not None:
            st.area_chart(nvts_data['Close'].tail(60), color="#00FF00")
    else:
        st.error("⚠️ DATA CONNECTION ERROR: Yahoo Finance is currently blocking the request. Please refresh in 30 seconds.")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    for c in crypto_list:
        c_data = get_verified_data(c)
        if c_data is not None:
            try:
                c_price = float(c_data['Close'].iloc[-1])
                st.metric(c, f"${c_price:,.2f}")
                st.area_chart(c_data['Close'].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional RVOL Monitor")
    heat_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    
    for h in heat_tickers:
        h_data = get_verified_data(h)
        if h_data is not None:
            try:
                v_now = float(h_data['Volume'].iloc[-1])
                v_avg = float(h_data['Volume'].tail(20).mean())
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}**")
                if rvol > 1.5:
                    c2.success(f"🔥 HIGH: {rvol:.2f}x")
                else:
                    c2.info(f"Normal: {rvol:.2f}x")
            except: continue
