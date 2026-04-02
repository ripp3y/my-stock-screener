# --- STEP 1: THE POWER SOURCE (Must be Lines 1 & 2) ---
import streamlit as st  # This defines 'st' so Line 5 works
import yfinance as yf    # This defines 'yf' for data fetching

# --- STEP 2: THE INPUT GATE ---
# This ensures buy_price is defined for the entire script
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    # Your core logic: Target = Entry * 1.80
    target_80 = buy_price * 1.80
    
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- STEP 4: FLIGHT ESTIMATE ---
    st.subheader("📅 Flight Estimate")
    
    # This safely checks for volatility data from your other modules
    if 'atr' in locals() and 'info' in locals():
        current_price = info.get('currentPrice', buy_price)
        days_est = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        # Clears the background crash and provides a clean status
        st.warning("Fetch ATR data to calculate arrival timeline.")
