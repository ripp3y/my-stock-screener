# --- STEP 1: INITIALIZE LIBRARIES (Must be at the very top) ---
import streamlit as st
import yfinance as yf

# --- STEP 2: ESTABLISH GLOBAL INPUTS ---
# This defines 'buy_price' so it's ready for every calculation below
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- STEP 4: FLIGHT ESTIMATE (The calculation layer) ---
    st.subheader("📅 Flight Estimate")
    
    # We check for ATR data from your volatility module
    if 'atr' in locals() and atr > 0:
        # Distance calculation
        current_price = info.get('currentPrice', buy_price)
        days_est = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        st.warning("Fetch ATR data to calculate arrival timeline.")
