import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.6", layout="wide")

# --- [2. DATA CLEANER - THE FIX] ---
def flatten_data(df, ticker):
    try:
        # This explicitly grabs one ticker and one column (Close) 
        # to prevent the 'MultiIndex' format error
        if ticker in df.columns.levels[0]:
            return df[ticker]['Close'].dropna().astype(float)
        return None
    except:
        # Fallback for single-ticker downloads
        return df['Close'].astype(float) if 'Close' in df.columns else None

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    try:
        # Download with group_by to keep tickers separated
        df = yf.download(tickers, period="6mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df
    except: return None

# --- [4. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days
st.title("📟 Strategic Terminal v10.6")
st.caption("Engine: v10.6 | Wytheville Hub | Fix: MultiIndex Flattening")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [5. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                # Use our new flattener to get a clean price list
                prices = flatten_data(data, t)
                if prices is not None:
                    curr_p = float(prices.iloc[-1])
                    recon_list.append({
                        "Ticker": t,
                        "Price": f"${curr_p:.2f}",
                        "20% Target": f"${curr_p * 1.20:.2f}"
                    })
            except: continue
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Chart for NVTS using the flattened data
        nvts_prices = flatten_data(data, "NVTS")
        if nvts_prices is not None:
            st.area_chart(nvts_prices.tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(c_list)
    if c_data is not None:
        for c in c_list:
            try:
                c_prices = flatten_data(c_data, c)
                if c_prices is not None:
                    curr_c = float(c_prices.iloc[-1])
                    st.metric(c, f"${curr_c:,.2f}")
                    st.area_chart(c_prices.tail(60), height=140, color="#FF9900" if "BTC" in c else "#00FF00")
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional RVOL")
    if data is not None:
        for h in ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]:
            try:
                # Fetch volume separately to avoid formatting clashes
                vol_data = data[h]['Volume'].dropna()
                v_now = float(vol_data.iloc[-1])
                v_avg = float(vol_data.tail(20).mean())
                rvol = v_now / v_avg
                
                c1, c2 = st.columns([1, 2])
                c1.write(f"**{h}**")
                if rvol > 1.5:
                    c2.markdown(f":green[**HIGH: {rvol:.2f}x**]")
                else:
                    c2.markdown(f"Normal: {rvol:.2f}x")
            except: continue
