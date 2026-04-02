# --- STEP 1: THE POWER SOURCE (Must be Line 1) ---
import streamlit as st  # This defines 'st'
import yfinance as yf    # This defines 'yf'

# --- STEP 2: THE INPUT GATE ---
# Sidebars must come AFTER the imports above
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
entry_floor = st.sidebar.number_input("Institutional Floor Price", value=0.0, step=0.1)

# --- STEP 3: THE ALPHA & BUY ZONE ENGINE ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # Take Profit Ladder (New Request)
    st.subheader("🪜 Take Profit Ladder")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

    # Buy Zone Alert logic
    if entry_floor > 0:
        # Check current price vs floor
        if 'info' in locals():
            current_price = info.get('currentPrice', 0)
            if current_price <= (entry_floor * 1.02):
                st.success("✅ PRICE IN BUY ZONE")
