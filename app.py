# --- STEP 1: INITIALIZE (MUST BE LINES 1 & 2) ---
import streamlit as st  # This defines the 'st' tool and kills the NameError
import yfinance as yf    # This defines the 'yf' tool for market data

# --- STEP 2: USER INPUT GATE ---
# Now that 'st' is defined, these sidebar tools will work perfectly
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)
trail_percent = st.sidebar.slider("Trailing Stop %", 5, 20, 9)

# --- STEP 3: THE ALPHA ENGINE ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **Ultimate Target:** ${round(target_80, 2)}")

    # Profit-Taking Milestones
    st.subheader("🪜 Profit-Taking Milestones")
    col1, col2 = st.columns(2)
    col1.warning(f"20% Trim: ${round(buy_price * 1.20, 2)}")
    col2.warning(f"50% Trim: ${round(buy_price * 1.50, 2)}")
