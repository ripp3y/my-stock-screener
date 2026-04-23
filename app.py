import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.3", layout="wide")

# --- [2. DATA ENGINE - HARDENED] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    try:
        # auto_adjust=True and actions=False keeps the data structure flat
        df = yf.download(tickers, period="6mo", interval="1d", auto_adjust=True, progress=False)
        return df
    except: return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_to_earnings = (target_date - datetime.now()).days

st.title("📟 Strategic Terminal v10.3")
st.caption("Engine: v10.3 | Wytheville Hub | Fix: Zero-Format Crash")
st.metric("NVTS Earnings", f"{max(0, days_to_earnings)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                # Force extraction of exactly one price as a number
                # This prevents the ',2f' format error on your phone
                raw_price = data['Close'][t].dropna().iloc[-1]
                price = float(raw_price) 
                
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${price:.2f}",
                    "20% Target": f"${price * 1.20:.2f}"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list))
        st.divider()
        st.area_chart(data['Close']["NVTS"].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(c_list)
    if c_data is not None:
        for c in c_list:
            try:
                c_price = float(c_data['Close'][c].dropna().iloc[-1])
                st.metric(c, f"${c_price:,.2f}") # Force-casted to single float
                st.area_chart(c_data['Close'][c].tail(60), height=140)
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Volume (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        for h in h_tickers:
            try:
                v_now = float(h_data['Volume'][h].iloc[-1])
                v_avg = float(h_data['Volume'][h].tail(20).mean())
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}**")
                # Using simple text colors to avoid library errors
                if rvol > 1.5:
                    c2.markdown(f":green[**HIGH: {rvol:.2f}x**]")
                else:
                    c2.markdown(f"Normal: {rvol:.2f}x")
            except: continue
