import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.9", layout="wide")

# --- [2. DATA ENGINE - WITH SAFETY CHECK] ---
@st.cache_data(ttl=300)
def get_safe_data(ticker):
    try:
        # Fetching with repair and auto_adjust for maximum stability
        df = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, repair=True, progress=False)
        
        # VALIDATION: Only return data if it actually contains prices
        if df is not None and not df.empty and 'Close' in df.columns:
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v10.9")
st.caption("Engine: v10.9 | Fix: KeyError 'Close' Shield | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_list = []
    
    for t in portfolio:
        data = get_safe_data(t)
        if data is not None:
            try:
                # The Safety Net: Force conversion to float only if data exists
                curr_p = float(data['Close'].iloc[-1])
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${curr_p:.2f}",
                    "20% Target": f"${curr_p * 1.20:.2f}",
                    "Trend": "🟢" if curr_p > data['Close'].tail(20).mean() else "🟡"
                })
            except: continue

    if recon_list:
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Chart with secondary safety check
        nvts_data = get_safe_data("NVTS")
        if nvts_data is not None:
            st.area_chart(nvts_data['Close'].tail(60), color="#00FF00")
    else:
        st.warning("🔄 Syncing with Yahoo... Please refresh in 10 seconds.")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    for c in crypto_list:
        c_data = get_safe_data(c)
        if c_data is not None:
            try:
                c_price = float(c_data['Close'].iloc[-1])
                st.metric(c, f"${c_price:,.2f}")
                st.area_chart(c_data['Close'].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 RVOL Monitor")
    heat_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    for h in heat_tickers:
        h_data = get_safe_data(h)
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
