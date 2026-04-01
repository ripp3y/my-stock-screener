import streamlit as st
import yfinance as yf

# --- 1. THE CONTROL PANEL (Must be at the top) ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- 2. THE ALPHA ENGINE ---
if buy_price > 0:
    # All calculations must happen INSIDE this block
    target_80 = buy_price * 1.80
    
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")
    
    st.subheader("📅 Flight Estimate")
    
    # Check for ATR data from your Dynamic Stop Loss module
    if 'atr' in locals() and atr > 0:
        current_price = info.get('currentPrice', buy_price)
        dist_to_target = target_80 - current_price
        days_est = dist_to_target / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        st.warning("Fetch ATR data to calculate arrival timeline.")
