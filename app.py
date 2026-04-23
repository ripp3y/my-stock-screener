import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.1", layout="wide")

# --- [2. HARDENED SIGNAL ENGINE] ---
def get_technical_signal(ticker_df):
    try:
        # We ensure the data is "Flat" before calculating
        # This prevents the 'Invalid Format' MultiIndex error
        df = ticker_df.copy()
        
        # Calculate Short (8) and Long (21) Moving Averages
        sma8 = df['Close'].rolling(window=8).mean()
        sma21 = df['Close'].rolling(window=21).mean()
        
        curr_8, curr_21 = sma8.iloc[-1], sma21.iloc[-1]
        prev_8, prev_21 = sma8.iloc[-2], sma21.iloc[-2]
        
        if curr_8 > curr_21 and prev_8 <= prev_21:
            return "🔥 BUY SIGNAL"
        elif curr_8 < curr_21 and prev_8 >= prev_21:
            return "⚠️ SELL SIGNAL"
        elif curr_8 > curr_21:
            return "🟢 BULLISH"
        else:
            return "🔴 BEARISH"
    except:
        return "⚖️ NEUTRAL"

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Download with 'auto_adjust' to keep columns simple
        df = yf.download(tickers, period="6mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [4. HEADER] ---
earnings_date = datetime(2026, 5, 5)
days_left = (earnings_date - datetime.now()).days

st.title("📟 Strategic Terminal v10.1")
st.caption(f"Engine: Python 3.12 | Wytheville Hub | Fix: MultiIndex Patch")
st.metric("NVTS Earnings Countdown", f"{max(0, days_left)} Days")

# --- [5. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON + SIGNALS", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                # FIX: Check if ticker exists in data
                if t in data.columns.levels[0]:
                    ticker_data = data[t].dropna()
                    curr_p = ticker_data['Close'].iloc[-1]
                    # Pass only the clean slice to the signal engine
                    signal = get_technical_signal(ticker_data)
                    
                    recon_list.append({
                        "Ticker": t,
                        "Price": f"${curr_p:.2f}",
                        "20% Target": f"${curr_p * 1.20:.2f}",
                        "Technical Signal": signal
                    })
            except: continue
        
        st.table(pd.DataFrame(recon_list))
        st.divider()
        target = st.selectbox("Deep-Dive Chart:", portfolio)
        if target in data.columns.levels[0]:
            st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO] ---
with tab_crypto:
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(crypto_list)
    if c_data is not None:
        for c in crypto_list:
            col_1, col_2 = st.columns([1, 3])
            with col_1: st.metric(c, f"${c_data[c]['Close'].iloc[-1]:,.2f}")
            with col_2: 
                color = "#FF9900" if "BTC" in c else "#00FF00"
                st.area_chart(c_data[c]['Close'].tail(60), height=140, color=color)

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional Volume (RVOL)")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        for h in h_tickers:
            try:
                if h in h_data.columns.levels[0]:
                    rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                    price = h_data[h]['Close'].iloc[-1]
                    
                    col_t, col_v, col_p = st.columns([1, 2, 1])
                    with col_t: st.markdown(f"**{h}**")
                    with col_v:
                        if rvol > 2.2: st.badge(f"EXTREME: {rvol:.2f}x", color="red", icon="🚨")
                        elif rvol > 1.5: st.badge(f"HIGH: {rvol:.2f}x", color="green", icon="🔥")
                        else: st.badge(f"Normal: {rvol:.2f}x", color="gray")
                    with col_p: st.write(f"${price:.2f}")
            except: continue

st.divider()
st.caption("v10.1 | Anti-Format-Error Patch Active")
