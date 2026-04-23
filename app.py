import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v11.2", layout="wide")

# --- [2. ZERO-DEPENDENCY DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_raw_data(ticker):
    """Bypasses scipy by disabling auto-repair and using legacy fetch."""
    try:
        # We explicitly turn off 'repair' and 'auto_adjust' 
        # These are the two features that trigger the 'scipy' requirement
        df = yf.download(
            ticker, 
            period="6mo", 
            interval="1d", 
            repair=False, 
            auto_adjust=False, 
            progress=False
        )
        if df is not None and not df.empty:
            # Manually clean up headers to keep it simple
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days

st.title("📟 Strategic Terminal v11.2")
st.caption("Engine: v11.2 Zero-Dep | Fix: Scipy Hard-Bypass | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_list = []
    
    for t in portfolio:
        data = get_raw_data(t)
        if data is not None:
            try:
                # Using standard indexing to avoid complex pandas lookups
                curr_p = float(data['Close'].iloc[-1])
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${curr_p:.2f}",
                    "20% Target": f"${curr_p * 1.20:.2f}",
                    "Status": "🟢" if curr_p > data['Close'].tail(10).mean() else "🟡"
                })
            except: continue

    if recon_list:
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Using native streamlit line chart (no scipy needed)
        nvts_data = get_raw_data("NVTS")
        if nvts_data is not None:
            st.line_chart(nvts_data['Close'].tail(60))
    else:
        st.warning("Connecting to server... Please refresh.")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    for c in c_list:
        c_data = get_raw_data(c)
        if c_data is not None:
            price = float(c_data['Close'].iloc[-1])
            st.metric(c, f"${price:,.2f}")
            st.line_chart(c_data['Close'].tail(45), height=150)

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 RVOL Institutional Monitor")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    for h in h_tickers:
        h_data = get_raw_data(h)
        if h_data is not None:
            try:
                v_now = float(h_data['Volume'].iloc[-1])
                v_avg = float(h_data['Volume'].tail(20).mean())
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}**")
                if rvol > 1.5:
                    c2.success(f"HIGH: {rvol:.2f}x")
                else:
                    c2.info(f"Normal: {rvol:.2f}x")
            except: continue
