import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v11.1", layout="wide")

# --- [2. LIGHTWEIGHT DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_verified_data(ticker):
    """Simplified fetch to avoid needing advanced math modules like scipy."""
    try:
        # We fetch only the bare essentials to stay under the radar
        df = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, progress=False)
        if df is not None and not df.empty and 'Close' in df.columns:
            # Flatten columns just in case Yahoo sends a multi-index
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v11.1")
st.caption("Engine: v11.1 Lite | Fix: Scipy Dependency Bypass | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_data = []
    
    with st.status("📡 Establishing Secure Connection...", expanded=False) as status:
        for t in portfolio:
            st.write(f"Checking {t}...")
            data = get_verified_data(t)
            if data is not None:
                try:
                    curr_p = float(data['Close'].iloc[-1])
                    # Manual math to avoid using 'rolling' or 'mean' if it triggers scipy
                    prices = data['Close'].tail(20).tolist()
                    avg_20 = sum(prices) / len(prices)
                    
                    recon_data.append({
                        "Ticker": t,
                        "Price": f"${curr_p:.2f}",
                        "20% Target": f"${curr_p * 1.20:.2f}",
                        "Signal": "🟢 BULL" if curr_p > avg_20 else "🟡 NEUTRAL"
                    })
                except: continue
        status.update(label="✅ Connection Stable", state="complete")

    if recon_data:
        st.table(pd.DataFrame(recon_data))
        st.divider()
        nvts_data = get_verified_data("NVTS")
        if nvts_data is not None:
            st.line_chart(nvts_data['Close'].tail(60), color="#00FF00")
    else:
        st.error("🔄 Data stream interrupted. Please refresh in 15 seconds.")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    for c in crypto_list:
        c_data = get_verified_data(c)
        if c_data is not None:
            c_price = float(c_data['Close'].iloc[-1])
            st.metric(c, f"${c_price:,.2f}")
            st.area_chart(c_data['Close'].tail(45), height=140, color="#FF9900" if "BTC" in c else "#00FF00")

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 RVOL Institutional Monitor")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    
    for h in h_tickers:
        h_data = get_verified_data(h)
        if h_data is not None:
            try:
                v_now = float(h_data['Volume'].iloc[-1])
                v_list = h_data['Volume'].tail(20).tolist()
                v_avg = sum(v_list) / len(v_list)
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}**")
                if rvol > 1.5:
                    c2.success(f"🔥 HIGH: {rvol:.2f}x")
                else:
                    c2.info(f"Normal: {rvol:.2f}x")
            except: continue
