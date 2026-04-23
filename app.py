import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

# --- [1. GLOBAL OVERRIDE] ---
# Forces 'st' definition to stick on Streamlit Cloud's Python 3.12 engine
if 'st' not in globals():
    import streamlit as st

# --- [2. TERMINAL CONFIG] ---
st.set_page_config(page_title="Radar v9.50", layout="wide")

# --- [3. HARDENED DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Standardized on 3mo/1d for 60-day visual stability
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception:
        return None

# --- [4. MANUAL COLOR ENGINE] ---
# Fail-safe logic: Highlights RVOL > 1.5 in Green and > 2.2 in Bright Lime
def style_heatmap(row):
    rvol = row['RVOL_NUM']
    if rvol > 2.2:
        return ['background-color: #00FF00; color: black; font-weight: bold'] * len(row)
    elif rvol > 1.5:
        return ['background-color: #008000; color: white'] * len(row)
    return [''] * len(row)

# --- [5. HEADER & COUNTDOWN] ---
# NVTS Earnings: May 5, 2026
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days

st.title("📟 Strategic Terminal v9.50")
col_info, col_count = st.columns([3, 1])
with col_info:
    st.caption(f"Engine: Python {sys.version.split()[0]} | Status: 🟢 MASTER CORE ACTIVE")
with col_count:
    st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [6. NAVIGATION TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO SCALED", "🔥 HEAT MAP"])

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
        
        st.table(pd.DataFrame(recon_list))
        st.divider()
        target = st.selectbox("Deep-Dive (60-Day):", portfolio)
        st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO SCALED] ---
with tab_crypto:
    st.subheader("₿ 60-Day Asset Velocity")
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF", "RIOT"]
    c_data = get_clean_data(crypto_list)
    
    if c_data is not None:
        for c in crypto_list:
            col_c1, col_c2 = st.columns([1, 3])
            with col_c1:
                price = c_data[c]['Close'].iloc[-1]
                st.metric(c, f"${price:,.2f}")
            with col_c2:
                # Orange for BTC, Green for Miners
                st.area_chart(c_data[c]['Close'].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")

# --- [TAB 3: HEAT MAP - REBUILT] ---
with tab_heatmap:
    st.subheader("🔥 Institutional RVOL Monitor")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        h_list = []
        for h in h_tickers:
            try:
                # Calculate RVOL: Today vs 20-Day Avg
                recent_vol = h_data[h]['Volume'].iloc[-1]
                avg_vol = h_data[h]['Volume'].tail(20).mean()
                r_val = recent_vol / avg_vol
                
                h_list.append({
                    "Ticker": h,
                    "RVOL": f"{r_val:.2f}x",
                    "RVOL_NUM": r_val, # Hidden column for styling
                    "Price": f"${h_data[h]['Close'].iloc[-1]:.2f}",
                    "Intensity": "🚨 EXTREME" if r_val > 2.2 else "🔥 HIGH" if r_val > 1.5 else "Normal"
                })
            except: continue
        
        df_heat = pd.DataFrame(h_list)
        # Displaying with manual row highlighting
        st.table(df_heat.style.apply(style_heatmap, axis=1))
        st.caption("Strategy: Highlighting RVOL > 1.5x (Institutional Accumulation)")

st.divider()
st.caption("v9.50 | Target: NVTS $19.50 Pivot | BTC Support Flip: $78,118")
