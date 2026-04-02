# --- STEP 1: INITIALIZE (Must be Line 1) ---
import streamlit as st  # Fixes the NameError
import yfinance as yf

# --- STEP 2: DYNAMIC INPUTS ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 10) # Default 10%

# --- STEP 3: THE PURSUIT ENGINE ---
if buy_price > 0:
    # 1. 80% Alpha Target
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # 2. Dynamic Trailing Stop
    if 'info' in locals():
        current_price = info.get('currentPrice', buy_price)
        # Calculate the highest price seen since purchase
        high_price = info.get('dayHigh', current_price) 
        trail_floor = high_price * (1 - (trail_percent / 100))
        
        st.subheader("🛡️ Trailing Stop Floor")
        if current_price < trail_floor:
            st.error(f"🛑 EXIT SIGNAL: Price (${current_price}) below ${round(trail_floor, 2)}")
        else:
            st.metric("Live Stop Floor", f"${round(trail_floor, 2)}", 
                      delta=f"{trail_percent}% Trail")

    # 3. Take Profit Ladder
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")
