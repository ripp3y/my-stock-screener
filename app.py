# --- STEP 1: FOUNDATION (Must be Lines 1 & 2) ---
import streamlit as st  # This defines 'st' and kills the NameError
import yfinance as yf    # This powers your live stock data

# --- STEP 2: USER INPUT GATE ---
# Sidebars must be defined AFTER the imports above
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 10)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    # 80% Target Pursuit
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # Profit-Taking Ladder
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")

    # --- STEP 4: SECTOR & VOLUME HEAT (Dynamic Content) ---
    # Fetch live info safely
    if 'ticker_symbol' in locals():
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        current_price = info.get('currentPrice', buy_price)
        
        # Trailing Stop calculation
        trail_floor = current_price * (1 - (trail_percent / 100))
        st.subheader("🛡️ Live Stop Floor")
        st.metric("Floor", f"${round(trail_floor, 2)}", delta=f"{trail_percent}% Trail")
