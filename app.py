import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.4", layout="wide")

# --- [2. DATA ENGINE - HARDENED FOR MOBILE] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    try:
        # We download and then immediately 'stack' the data to fix the MultiIndex error
        raw = yf.download(tickers, period="6mo", interval="1d", auto_adjust=True, progress=False)
        if raw.empty: return None
        
        # This 'stacks' the tickers into a single clean column
        df = raw.stack(level=1, future_stack=True).reset_index()
        df.columns = ['Date', 'Ticker', 'Close', 'High', 'Low', 'Open', 'Volume']
        return df
    except: return None

# --- [3. HEADER] ---
target_date = datetime(2026, 5, 5)
days_left = (target_date - datetime.now()).days

st.title("📟 Strategic Terminal v10.4")
st.caption("Engine: v10.4 Ironclad | Wytheville Hub | Fix: MultiIndex Stack")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

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
                # Filter for just this ticker and get the last row
                t_row = data[data['Ticker'] == t].iloc[-1]
                price = float(t_row['Close'])
                
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${price:.2f}",
                    "20% Target": f"${price * 1.20:.2f}"
                })
            except: continue
        
        st.table(pd.DataFrame(recon_list))
        st.divider()
        # Chart uses the filtered dataframe for NVTS
        nvts_chart = data[data['Ticker'] == "NVTS"].set_index('Date')['Close'].tail(60)
        st.area_chart(nvts_chart, color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(c_list)
    
    if c_data is not None:
        for c in c_list:
            try:
                c_row = c_data[c_data['Ticker'] == c].iloc[-1]
                c_price = float(c_row['Close'])
                st.metric(c, f"${c_price:,.2f}") # This will now work perfectly
                
                c_chart = c_data[c_data['Ticker'] == c].set_index('Date')['Close'].tail(60)
                st.area_chart(c_chart, height=140, color="#FF9900" if "BTC" in c else "#00FF00")
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Volume (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        for h in h_tickers:
            try:
                h_rows = h_data[h_data['Ticker'] == h]
                v_now = float(h_rows['Volume'].iloc[-1])
                v_avg = float(h_rows['Volume'].tail(20).mean())
                rvol = v_now / v_avg
                
                col1, col2 = st.columns([1, 2])
                col1.write(f"**{h}**")
                # Using standard markdown colors for maximum mobile stability
                if rvol > 1.5:
                    col2.markdown(f":green[**HIGH: {rvol:.2f}x**]")
                else:
                    col2.markdown(f"Normal: {rvol:.2f}x")
            except: continue
