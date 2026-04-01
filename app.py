import streamlit as st
import yfinance as yf

# --- 1. INITIALIZE MEMORY (Top of Script) ---
if 'buy_price' not in st.session_state:
    st.session_state.buy_price = 0.0
if 'atr' not in st.session_state:
    st.session_state.atr = 0.0

# --- 2. INPUTS (Sidebar) ---
st.session_state.buy_price = st.sidebar.number_input(
    "Actual Purchase Price", 
    value=st.session_state.buy_price, 
    step=0.1
)

# --- 3. THE 80% CALCULATION ENGINE ---
if st.session_state.buy_price > 0:
    target_80 = st.session_state.buy_price * 1.80
    
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- 4. TIME TO TARGET (The Estimator) ---
    # Only runs if we have both a price and volatility data
    if st.session_state.atr > 0:
        dist_to_go = target_80 - curr_price
        days_est = dist_to_go / st.session_state.atr
        st.info(f"📅 **Estimated Flight Time:** {round(days_est)} Market Days")
