import streamlit as st  # <--- THIS MUST BE LINE 1
import yfinance as yf    # <--- THIS MUST BE LINE 2

# --- 1. GET THE USER INPUT ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- 2. CALCULATE TARGETS ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- 3. FLIGHT ESTIMATE LOGIC ---
    st.subheader("📅 Flight Estimate")
    
    # We check if 'atr' was defined in your volatility module
    if 'atr' in locals() and atr > 0:
        current_price = info.get('currentPrice', buy_price)
        days_est = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        # This clears the background error and gives a clean status
        st.warning("Fetch ATR data to calculate arrival timeline.")
