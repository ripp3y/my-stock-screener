import streamlit as st
import yfinance as yf

# --- 1. THE FOUNDATION (Top of Script) ---
# Use the sidebar to establish your variables first
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- 2. THE TARGET CALCULATOR ---
# This creates 'target_80' which the flight estimate needs
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- 3. THE FLIGHT ESTIMATE (Inside the 'if' block) ---
    # Placing it here ensures 'buy_price' and 'target_80' are 100% defined
    st.subheader("📅 Flight Estimate")
    
    # We need to ensure 'atr' is fetched from your previous dynamic stop loss logic
    if 'atr' in locals() and atr > 0:
        # Distance calculation
        current_price = info.get('currentPrice', buy_price)
        days_to_go = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_to_go)} Trading Days")
