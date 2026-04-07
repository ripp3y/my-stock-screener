import streamlit as st
import pandas as pd
import yfinance as yf

# --- 1. CONFIG ---
st.set_page_config(page_title="Alpha Scout: Strategic Terminal", layout="wide")

def get_technical_signals(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    avg_vol = data['Volume'].rolling(window=20).mean()
    vol_spike = data['Volume'].iloc[-1] > (avg_vol.iloc[-1] * 1.5)
    return rsi.iloc[-1], vol_spike

# --- 2. TABS ---
tab1, tab2 = st.tabs(["🚀 Live Scout", "🎯 Goal Center"])

# --- TAB 1: LIVE SCOUT ---
with tab1:
    st.title("Market Intelligence: Monday, April 6, 2026")
    team_tickers = ["GEV", "BW", "PBR-A", "EQNR", "TPL", "SNDK", "MRNA"]
    
    try:
        data = yf.download(team_tickers, period="6mo", group_by='ticker')
        cols = st.columns(len(team_tickers))
        
        latest_prices = {}
        for i, ticker in enumerate(team_tickers):
            ticker_df = data[ticker].dropna()
            price = ticker_df['Close'].iloc[-1]
            latest_prices[ticker] = price
            rsi, has_spike = get_technical_signals(ticker_df)
            
            with cols[i]:
                st.metric(ticker, f"${price:.2f}")
                if rsi > 70: st.error(f"RSI: {rsi:.1f}")
                elif rsi < 35: st.success(f"RSI: {rsi:.1f}")
                else: st.caption(f"RSI: {rsi:.1f}")
                
                if has_spike: st.warning("🔥 VOL SPIKE")
                else: st.write("Normal Vol")

    except Exception as e:
        st.error(f"Sync Error: {e}")

# --- TAB 2: GOAL CENTER ---
with tab2:
    st.header("Strategic Execution: 2026 Goals")
    
    # 1. HARVEST GOAL
    st.subheader("🟢 Current Mission: The EQNR Harvest")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        shares_to_sell = 49  # Your EQNR shares for the ~$2k target
        target_cash = 2045.50
        current_value = shares_to_sell * latest_prices.get('EQNR', 41.95)
        
        st.write(f"**Target:** ${target_cash:,.2f}")
        st.write(f"**Current Value:** ${current_value:,.2f}")
        
        # Calculate percentage of goal
        progress = min(current_value / target_cash, 1.0)
        st.progress(progress)
    
    with col2:
        st.info(f"""
        **Insight:** EQNR is currently '
