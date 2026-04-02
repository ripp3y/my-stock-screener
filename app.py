# --- STEP 1: INITIALIZE ---
import streamlit as st
import yfinance as yf
import pandas as pd

# --- STEP 2: INPUT GATE ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
ticker_symbol = st.sidebar.text_input("Ticker Symbol", value="CENX").upper()

# --- STEP 3: ALPHA & RS ENGINE ---
if buy_price > 0:
    # 80% Target Logic
    target_80 = buy_price * 1.80
    st.header(f"🎯 {ticker_symbol} Alpha: The 80% Path")
    st.success(f"🚀 **Target Price:** ${round(target_80, 2)}")

    # --- NEW: Relative Strength (RS) Comparison ---
    st.subheader("📈 Market Relative Strength (30D)")
    
    # Fetch Data for Stock and S&P 500
    stock_data = yf.download(ticker_symbol, period="1mo")['Close']
    spy_data = yf.download("SPY", period="1mo")['Close']
    
    # Calculate % Returns
    stock_perf = ((stock_data.iloc[-1] - stock_data.iloc[0]) / stock_data.iloc[0]) * 100
    spy_perf = ((spy_data.iloc[-1] - spy_data.iloc[0]) / spy_data.iloc[0]) * 100
    rs_gap = stock_perf - spy_perf

    col1, col2 = st.columns(2)
    col1.metric(f"{ticker_symbol} Return", f"{round(stock_perf, 2)}%")
    col2.metric("RS vs S&P 500", f"{round(rs_gap, 2)}%", delta=f"{round(rs_gap, 2)}% Alpha")

    # --- VOLUME HEAT CHECK ---
    st.subheader("📊 Institutional Heat Check")
    # (Previous volume logic continues here...)
