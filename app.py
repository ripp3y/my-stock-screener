# --- STEP 1: INITIALIZE FOUNDATION (Must be Line 1) ---
import streamlit as st  # This defines 'st' and kills the NameError
import yfinance as yf    # This powers your live market data

# --- STEP 2: USER INPUT GATE ---
# These sidebar commands now work because 'st' was defined above
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 10)

# --- STEP 3: THE PURSUIT ENGINE ---
if buy_price > 0:
    # 80% Pursuit Logic
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # Profit-Taking Milestones
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

    # --- STEP 4: SECTOR & VOLUME HEAT ---
    # Fetch data safely using yfinance
    if 'info' in locals():
        current_price = info.get('currentPrice', buy_price)
        # 10% Trailing Stop Floor
        trail_floor = current_price * (1 - (trail_percent / 100))
        st.subheader("🛡️ Live Stop Floor")
        st.metric("Exit Floor", f"${round(trail_floor, 2)}", delta=f"{trail_percent}% Trail")
