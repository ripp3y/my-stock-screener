# --- STEP 1: INITIALIZATION (MUST BE AT THE TOP) ---
import streamlit as st  # Fixes 'st' is not defined
import yfinance as yf    # Powers market data
import pandas as pd      # Handles data structure

# --- STEP 2: TARGET ALPHA ENGINE ---
st.sidebar.header("🎯 Target Alpha Engine")
# Preserving your $23.00 entry point
buy_price = st.sidebar.number_input("Actual Purchase Price", value=23.0)
ticker_input = st.sidebar.text_input("Ticker Deep Dive", value="PBR")

if buy_price > 0:
    st.header(f"🚀 {ticker_input} Path to Alpha")
    st.success(f"Ultimate Target (1.8x): ${round(buy_price * 1.8, 2)}")
    
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.2, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.5, 2)}")

# --- STEP 3: PORTFOLIO ALPHA WITH MILESTONE ALERTS ---
st.subheader("📊 Portfolio Alpha Spread")
portfolio = ["PBR", "CENX", "EQNR", "CNQ", "CF"]
spy = yf.download("SPY", period="1mo")

if not spy.empty:
    # Flattening data to prevent TypeErrors
    spy_prices = spy['Close'].values.flatten()
    spy_perf = ((spy_prices[-1] - spy_prices[0]) / spy_prices[0]) * 100
    st.caption(f"S&P 500 (1mo) Benchmark: {round(spy_perf, 2)}%")
    
    cols = st.columns(len(portfolio))
    for i, ticker in enumerate(portfolio):
        t_data = yf.download(ticker, period="1mo")
        if not t_data.empty:
            t_prices = t_data['Close'].values.flatten()
            curr_price = float(t_prices[-1])
            t_perf = ((curr_price - t_prices[0]) / t_prices[0]) * 100
            alpha = t_perf - spy_perf
            
            # --- MEDAL LOGIC ---
            gain = (curr_price - buy_price) / buy_price
            medal = ""
            if gain >= 0.50:
                medal = "🥇 " # Gold milestone
            elif gain >= 0.20:
                medal = "🥉 " # Bronze milestone
                
            cols[i].metric(
                label=f"{medal}{ticker}", 
                value=f"{round(alpha, 2)}%", 
                delta=f"{round(t_perf, 2)}% Abs"
            )
