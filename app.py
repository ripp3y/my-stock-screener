import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v11.3", layout="wide")

# --- [2. GHOST ENGINE - NO SCIPY] ---
@st.cache_data(ttl=600)
def get_ghost_data(ticker):
    """Uses .history instead of .download to bypass scipy dependency."""
    try:
        t_obj = yf.Ticker(ticker)
        # .history is 'raw' and doesn't trigger the scipy-based repair logic
        df = t_obj.history(period="6mo", interval="1d")
        
        if df is not None and not df.empty:
            # Standardize columns to avoid any MultiIndex errors
            df = df.reset_index()
            # Ensure we only have the columns we need
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            return df
        return None
    except:
        return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v11.3")
st.caption("Engine: v11.3 Ghost | Fix: Zero-Scipy Dependency | Hub: Galax")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    recon_list = []
    
    # Progress status for mobile
    with st.status("📡 Connecting to Market Ghost...", expanded=False) as status:
        for t in portfolio:
            st.write(f"Scanning {t}...")
            data = get_ghost_data(t)
            if data is not None:
                try:
                    curr_p = float(data['Close'].iloc[-1])
                    # Manual Moving Average to avoid advanced math libraries
                    p_list = data['Close'].tail(20).tolist()
                    sma_20 = sum(p_list) / len(p_list)
                    
                    recon_list.append({
                        "Ticker": t,
                        "Price": f"${curr_p:.2f}",
                        "20% Target": f"${curr_p * 1.20:.2f}",
                        "Signal": "🟢 BULL" if curr_p > sma_20 else "🟡 HOLD"
                    })
                except: continue
        status.update(label="✅ Recon Complete", state="complete")

    if recon_list:
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Clean line chart for NVTS
        nvts_data = get_ghost_data("NVTS")
        if nvts_data is not None:
            st.line_chart(nvts_data.set_index('Date')['Close'].tail(60))

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    for c in c_list:
        c_data = get_ghost_data(c)
        if c_data is not None:
            price = float(c_data['Close'].iloc[-1])
            st.metric(c, f"${price:,.2f}")
            st.area_chart(c_data.set_index('Date')['Close'].tail(45), height=140)

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 RVOL Institutional Flow")
    h_list = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    for h in h_list:
        h_data = get_ghost_data(h)
        if h_data is not None:
            try:
                v_now = float(h_data['Volume'].iloc[-1])
                v_avg = sum(h_data['Volume'].tail(20).tolist()) / 20
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}**")
                if rvol > 1.5:
                    c2.success(f"🔥 HIGH: {rvol:.2f}x")
                else:
                    c2.info(f"Normal: {rvol:.2f}x")
            except: continue
