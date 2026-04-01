# --- THE POWER SOURCE ---
import streamlit as st  # If this isn't Line 1, 'st' will never be defined
import yfinance as yf

# --- THE INPUT GATE ---
# We define the price here so the terminal knows what to calculate
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- THE ALPHA ENGINE ---
# We only open the logic gate IF buy_price exists
if buy_price > 0:
    target_80 = buy_price * 1.80
    
    # UI Elements
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")
    
    # Flight Estimate
    st.subheader("📅 Flight Estimate")
    
    # Look for 'atr' variable from your other logic blocks
    if 'atr' in locals() and atr > 0:
        current_price = info.get('currentPrice', buy_price)
        days_est = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        # This keeps the UI clean without background crashes
        st.warning("Fetch ATR data to calculate arrival timeline.")
