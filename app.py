import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.2", layout="wide")

# --- [2. SIGNAL ENGINE] ---
def get_technical_signal(ticker_df):
    try:
        # Extract only the Close column and flatten it to avoid Format Errors
        close_series = ticker_df['Close'].astype(float)
        
        sma8 = close_series.rolling(window=8).mean()
        sma21 = close_series.rolling(window=21).mean()
        
        curr_8, curr_21 = sma8.iloc[-1], sma21.iloc[-1]
        prev_8, prev_21 = sma8.iloc[-2], sma21.iloc[-2]
        
        if curr_8 > curr_21 and prev_8 <= prev_21: return "🔥 BUY SIGNAL"
        elif curr_8 < curr_21 and prev_8 >= prev_21: return "⚠️ SELL SIGNAL"
        elif curr_8 > curr_21: return "🟢 BULLISH"
        else: return "🔴 BEARISH"
    except:
        return "⚖️ NEUTRAL"

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=300)
def get_clean_data(tickers):
    try:
        # Download with auto_adjust=True to flatten price columns
        df = yf.download(tickers, period="6mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df
    except: return None

# --- [4. HEADER] ---
st.title("📟 Strategic Terminal v10.2")
st.caption("Fix: Explicit Float Conversion | Engine: v10.2 Core")

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
                # Ensure we have a clean slice of data for the ticker
                t_df = data[t].dropna()
                curr_p = float(t_df['Close'].iloc[-1]) # Force to float here
                sig = get_technical_signal(t_df)
                
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${curr_p:.2f}",
                    "20% Target": f"${curr_p * 1.20:.2f}",
                    "Signal": sig
                })
            except: continue
        st.table(pd.DataFrame(recon_list))

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    c_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(c_list)
    if c_data is not None:
        for c in c_list:
            try:
                price = float(c_data[c]['Close'].iloc[-1])
                st.metric(c, f"${price:,.2f}") # comma for thousands
                st.area_chart(c_data[c]['Close'].tail(60), height=150)
            except: continue

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional RVOL")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        for h in h_tickers:
            try:
                vol_now = float(h_data[h]['Volume'].iloc[-1])
                vol_avg = float(h_data[h]['Volume'].tail(20).mean())
                rvol = vol_now / vol_avg
                
                col1, col2 = st.columns([1, 2])
                col1.write(f"**{h}**")
                if rvol > 1.5:
                    col2.success(f"HIGH: {rvol:.2f}x")
                else:
                    col2.info(f"Normal: {rvol:.2f}x")
            except: continue
