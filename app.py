import streamlit as st
import yfinance as yf

# --- 1. GLOBAL INITIALIZATION (Top of Script) ---
# Setting these to None or 0.0 prevents 'NameErrors'
buy_price = 0.0
atr = 0.0 
target_80 = 0.0

# --- 2. SIDEBAR INPUTS ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- 3. TARGET CALCULATIONS ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

# --- 4. TIME TO TARGET ESTIMATOR (The Safety Check) ---
# We check if ALL required variables are defined before running math
if buy_price > 0 and atr > 0 and target_80 > 0:
    st.write("Estimating flight path...")
    distance_left = target_80 - curr_price
    # ... rest of your logic
