import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

# --- [1. CONFIG] ---
st.set_page_config(page_title="Radar v10.0", layout="wide")

# --- [2. SIGNAL ENGINE] ---
def get_technical_signal(df):
    try:
        # Calculate Short (8) and Long (21) Moving Averages
        close = df['Close']
        sma8 = close.rolling(window=8).mean()
        sma21 = close.rolling(window=21).mean()
        
        curr_8, curr_21 = sma8.iloc[-1], sma21.iloc[-1]
        prev_8, prev_21 = sma8.iloc[-2], sma21.iloc[-2]
        
        # Bullish Crossover (Golden Cross)
        if curr_8 > curr_21 and prev_8 <= prev_21:
            return "🔥 BUY SIGNAL"
        # Bearish Crossover (Death Cross)
        elif curr_8 < curr_21 and prev_8 >= prev_21:
            return "⚠️ SELL SIGNAL"
        # Trending Up
        elif curr_8 > curr_21:
            return "🟢 BULLISH"
        # Trending Down
        else:
            return "🔴 BEARISH"
    except:
        return "⚖️ NEUTRAL"

# --- [3. DATA ENGINE] ---
@st.cache_data(ttl=600)
def get_clean_data(tickers):
    if not tickers: return None
    try:
        # Fetching 3 months to ensure SMA calculations have enough lead-in data
        df = yf.download(tickers, period="3mo", interval="1d", group_by='ticker', auto_adjust=True, progress=False)
        return df if not df.empty else None
    except Exception: return None

# --- [4. HEADER & EARNINGS] ---
# NVTS Q1 2026 Earnings: May 5, 2026
earnings_date = datetime(2026, 5, 5)
days_left = (earnings_date - datetime.now()).days

st.title("📟 Strategic Terminal v10.0")
col_info, col_count = st.columns([2, 1])
with col_info:
    st.caption(f"Engine: Python 3.12 | Wytheville Hub | Signal: SMA 8/21")
with col_count:
    # Highlighting the critical countdown to May 5th
    color = "inverse" if days_left > 7 else "off"
    st.metric("NVTS Earnings", f"{max(0, days_left)} Days", help="Reporting May 5th After Hours")

# --- [5. TABS] ---
tab_recon, tab_crypto, tab_heatmap = st.tabs(["📊 RECON + SIGNALS", "₿ CRYPTO", "🔥 HEAT MAP"])

# --- [TAB 1: RECON + SIGNALS] ---
with tab_recon:
    portfolio = ["NVTS", "FIX", "SNDK", "MRVL", "STX", "MTZ", "CIEN"]
    data = get_clean_data(portfolio)
    
    if data is not None:
        recon_list = []
        for t in portfolio:
            try:
                # Get current price and technical signal
                ticker_df = data[t].dropna()
                curr_p = ticker_df['Close'].iloc[-1]
                signal = get_technical_signal(ticker_df)
                
                recon_list.append({
                    "Ticker": t,
                    "Price": f"${curr_p:.2f}",
                    "20% Target": f"${curr_p * 1.20:.2f}",
                    "Technical Signal": signal
                })
            except: continue
        
        # Displaying with Signal Intelligence
        st.table(pd.DataFrame(recon_list))
        st.divider()
        target = st.selectbox("Deep-Dive Chart (60-Day):", portfolio)
        st.area_chart(data[target]['Close'].tail(60), color="#00FF00")

# --- [TAB 2: CRYPTO SCALED] ---
with tab_crypto:
    st.subheader("₿ 60-Day Crypto Velocity")
    crypto_list = ["BTC-USD", "MARA", "IREN", "WULF"]
    c_data = get_clean_data(crypto_list)
    
    if c_data is not None:
        for c in crypto_list:
            col_1, col_2 = st.columns([1, 3])
            with col_1:
                st.metric(c, f"${c_data[c]['Close'].iloc[-1]:,.2f}")
            with col_2:
                # Orange for BTC, Green for Mining stocks
                chart_col = "#FF9900" if "BTC" in c else "#00FF00"
                st.area_chart(c_data[c]['Close'].tail(60), height=140, color=chart_col)

# --- [TAB 3: HEAT MAP] ---
with tab_heatmap:
    st.subheader("🔥 Institutional RVOL Badges")
    h_tickers = ["NVTS", "FIX", "MRVL", "ALAB", "CRUS", "VRT", "SMCI"]
    h_data = get_clean_data(h_tickers)
    
    if h_data is not None:
        st.write("---")
        for h in h_tickers:
            try:
                # RVOL calculation
                rvol = h_data[h]['Volume'].iloc[-1] / h_data[h]['Volume'].tail(20).mean()
                price = h_data[h]['Close'].iloc[-1]
                
                col_t, col_v, col_p = st.columns([1, 2, 1])
                with col_t: st.markdown(f"**{h}**")
                with col_v:
                    if rvol > 2.2: st.badge(f"EXTREME: {rvol:.2f}x", color="red", icon="🚨")
                    elif rvol > 1.5: st.badge(f"HIGH: {rvol:.2f}x", color="green", icon="🔥")
                    else: st.badge(f"Normal: {rvol:.2f}x", color="gray")
                with col_p: st.write(f"${price:.2f}")
                st.write("---")
            except: continue

st.divider()
st.caption("v10.0 | BTC Support Flip: $78,410 | NVTS Bullish Pivot: $19.44")
