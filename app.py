# --- STEP 1: IMPORTS (Must be Line 1) ---
import streamlit as st
import yfinance as yf

# --- STEP 2: USER INPUTS (Sidebar) ---
# Defining this here ensures 'buy_price' exists for all logic below
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- STEP 3: TARGET CALCULATIONS ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- STEP 4: FLIGHT ESTIMATE (The final calculation) ---
    st.subheader("📅 Flight Estimate")
    
    # We check if 'atr' was defined in your volatility module
    if 'atr' in locals() and atr > 0:
        current_price = info.get('currentPrice', buy_price)
        days_est = (target_80 - current_price) / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        st.warning("Fetch ATR data to calculate arrival timeline.")
