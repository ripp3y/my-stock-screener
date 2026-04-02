# --- STEP 1: INITIALIZATION ---
import streamlit as st  # Fixes 'st' is not defined
import yfinance as yf    # Core market data engine
import pandas as pd

# --- STEP 2: USER INPUTS ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=23.0, step=0.1)
ticker_input = st.sidebar.text_input("Ticker for Volume Check", value="PBR")

# --- STEP 3: PERFORMANCE TARGETS ---
if buy_price > 0:
    st.header("🎯 Target Alpha: The 80% Path")
    # Projecting the $41.40 target based on $23.00 entry
    st.success(f"🚀 **Ultimate Target:** ${round(buy_price * 1.8, 2)}")
    
    st.subheader("🪜 Profit-Taking Milestones")
    c1, c2 = st.columns(2)
    c1.warning(f"20% Trim: ${round(buy_price * 1.2, 2)}")
    c2.warning(f"50% Trim: ${round(buy_price * 1.5, 2)}")

# --- STEP 4: INSTITUTIONAL FLOW ---
st.subheader("🏦 Institutional Flow")
if ticker_input:
    hist = yf.Ticker(ticker_input).history(period="5d")
    if not hist.empty:
        # Calculate volume ratio relative to 5-day average
        vol_ratio = hist['Volume'].iloc[-1] / hist['Volume'].mean()
        st.write(f"Current volume is **{round(float(vol_ratio), 2)}x** avg.")

# --- STEP 5: ALPHA SPREAD (STABILITY FIX) ---
st.subheader("📊 Alpha Spread")
spy = yf.download("SPY", period="1mo")
if ticker_input and not spy.empty:
    tick_data = yf.download(ticker_input, period="1mo")
    if not tick_data.empty:
        # FIX: Explicitly flatten the data to prevent TypeErrors
        # This extracts a clean column of numbers even if yfinance returns extra headers
        s_prices = spy['Close'].values.flatten()
        t_prices = tick_data['Close'].values.flatten()

        s_perf = ((s_prices[-1] - s_prices[0]) / s_prices[0]) * 100
        t_perf = ((t_prices[-1] - t_prices[0]) / t_prices[0]) * 100
        spread = t_perf - s_perf
        
        m1, m2 = st.columns(2)
        m1.metric("S&P 500 (1mo)", f"{round(s_perf, 2)}%")
        m2.metric("Alpha Spread", f"{round(spread, 2)}%", delta=f"{round(spread, 2)}%")
