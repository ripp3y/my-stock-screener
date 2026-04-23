import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.5", layout="wide")

# --- [2. HARDENED DATA ENGINE] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    try:
        # multi_level_index=False is the specific fix for the ',2f' error
        df = yf.download(
            tickers=tickers, 
            period="6mo", 
            interval="1d", 
            multi_level_index=False, 
            auto_adjust=True, 
            progress=False
        )
        return df
    except: return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days

st.title("📟 Strategic Terminal v10.5")
st.caption("Engine: v10.5 Ironclad | Fix: multi_level_index=False")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [4. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None and not data.empty:
        recon_list = []
        for t in portfolio:
            try:
                # In flat mode, columns are simply 'Ticker'
                # We pull the very last price and force it to a float
                price = float(data[t].dropna().iloc[-1])
                
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${price:.2f}",
                    "20% Target": f"${price * 1.20:.2f}"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Chart for the lead ticker
        st.area_chart(data["NVTS"].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(c_list)
    
    if c_data is not None and not c_data.empty:
        for c in c_list:
            try:
                price = float(c_data[c].dropna().iloc[-1])
                st.metric(c, f"${price:,.2f}")
                st.area_chart(c_data[c].tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Volume Relative to 20D Avg")
    # We download volume separately to keep the logic clean
    v_data = yf.download(portfolio, period="1mo", multi_level_index=False, progress=False)['Volume']
    
    if v_data is not None:
        for t in portfolio:
            try:
                v_now = float(v_data[t].iloc[-1])
                v_avg = float(v_data[t].tail(20).mean())
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{t}**")
                if rvol > 1.5:
                    c2.success(f"HIGH: {rvol:.2f}x")
                else:
                    c2.info(f"Normal: {rvol:.2f}x")
            except: continue
