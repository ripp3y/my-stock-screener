# --- STEP 1: INITIALIZE (Must be Line 1) ---
import streamlit as st  # This defines 'st'
import yfinance as yf    # This defines 'yf'

# --- STEP 2: THE INPUT GATE ---
# Sidebars must come AFTER the imports above to avoid NameError
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 10)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    # 1. 80% Pursuit Logic
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # 2. Take Profit Ladder
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

    # 3. Dynamic Trailing Stop
    if 'info' in locals():
        current_price = info.get('currentPrice', buy_price)
        high_price = info.get('dayHigh', current_price) 
        trail_floor = high_price * (1 - (trail_percent / 100))
        
        st.subheader("🛡️ Trailing Stop Floor")
        st.metric("Live Stop Floor", f"${round(trail_floor, 2)}", delta=f"{trail_percent}% Trail")
