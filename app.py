# --- STEP 1: INITIALIZE LIBRARIES (Must be the very first lines) ---
import streamlit as st  # Defines 'st'
import yfinance as yf    # Defines 'yf'

# --- STEP 2: ESTABLISH GLOBAL INPUTS ---
# Placing this here ensures 'buy_price' is ready for all logic below
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- STEP 3: THE PURSUIT ENGINE ---
if buy_price > 0:
    # Math logic for your 80% alpha target
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- STEP 4: FLIGHT ESTIMATE ---
    st.subheader("📅 Flight Estimate")
    
    # This checks if 'atr' was defined earlier in your script
    if 'atr' in locals() and atr > 0:
        current_price = info.get('currentPrice', buy_price)
        days_est = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        # Prevents the app from crashing if volatility data isn't fetched yet
        st.warning("Fetch ATR data to calculate arrival timeline.")
