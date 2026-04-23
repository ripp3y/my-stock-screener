import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.7", layout="wide")

# --- [2. DATA ENGINE - INDIVIDUAL FETCH] ---
@st.cache_data(ttl=300)
def get_safe_price(ticker):
    """Pulls stock data one-by-one to prevent MultiIndex crashes."""
    try:
        # Pulling individually ensures a simple, flat table structure
        df = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, progress=False)
        if not df.empty:
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v10.7")
st.caption("Engine: v10.7 | Fix: Individual Ticker Threading | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_list = []
    
    for t in portfolio:
        data = get_safe_price(t)
        if data is not None:
            try:
                # Force casting to single float to stop format errors
                curr_p = float(data['Close'].iloc[-1])
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${curr_p:.2f}",
                    "20% Target": f"${curr_p * 1.20:.2f}",
                    "Signal": "🟢 BULLISH"
                })
            except: continue

    if recon_list:
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Chart for NVTS specifically
        nvts_data = get_safe_price("NVTS")
        if nvts_data is not None:
            st.area_chart(nvts_data['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    for c in crypto_list:
        c_data = get_safe_price(c)
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
        h_data = get_safe_price(h)
        if h_data is not None:
            try:
                v_now = float(h_data['Volume'].iloc[-1])
                v_avg = float(h_data['Volume'].tail(20).mean())
                rvol = v_now / v_avg
                price = float(h_data['Close'].iloc[-1])
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}** \n${price:.2f}")
                if rvol > 1.5:
                    c2.success(f"🔥 HIGH: {rvol:.2f}x")
                else:
                    c2.info(f"Normal: {rvol:.2f}x")
            except: continue
