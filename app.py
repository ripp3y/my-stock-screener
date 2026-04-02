# --- STEP 1: INITIALIZATION (MUST BE AT THE TOP) ---
import streamlit as st  # Fixes NameError
import yfinance as yf    # Powers market data
import pandas as pd      # Handles data structure

# --- STEP 2: PORTFOLIO TARGETS (CENX / EQNR / PBR) ---
st.sidebar.header("🎯 Target Alpha Engine")
# Using your $23.00 entry as the baseline
buy_price = st.sidebar.number_input("Purchase Price", value=23.0)
ticker_input = st.sidebar.text_input("Deep Dive Ticker", value="PBR")

if buy_price > 0:
    st.header(f"🚀 {ticker_input} Path to Alpha")
    st.success(f"**Ultimate Target (1.8x):** ${round(buy_price * 1.8, 2)}")
    
    c1, c2 = st.columns(2)
    c1.warning(f"20% Trim: ${round(buy_price * 1.2, 2)}")
    c2.warning(f"50% Trim: ${round(buy_price * 1.5, 2)}")

# --- STEP 3: MULTI-ALPHA TRACKER ---
st.subheader("📊 Portfolio Alpha Spread")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
spy = yf.download("SPY", period="1mo")

if not spy.empty:
    # Flatten MultiIndex to avoid TypeErrors
    spy_prices = spy['Close'].values.flatten()
    spy_perf = ((spy_prices[-1] - spy_prices[0]) / spy_prices[0]) * 100
    st.metric("S&P 500 (1mo)", f"{round(spy_perf, 2)}%")
    
    # Track your Energy & Materials rotation
    cols = st.columns(len(portfolio))
    for i, ticker in enumerate(portfolio):
        t_data = yf.download(ticker, period="1mo")
        if not t_data.empty:
            t_prices = t_data['Close'].values.flatten()
            t_perf = ((t_prices[-1] - t_prices[0]) / t_prices[0]) * 100
            alpha = t_perf - spy_perf
            # Absolute performance in the delta
            cols[i].metric(ticker, f"{round(alpha, 2)}%", delta=f"{round(t_perf, 2)}%")
