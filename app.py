import streamlit as st
import yfinance as yf

# --- 1. GLOBAL INPUTS (Top of Script) ---
# Putting this first ensures 'buy_price' is always defined for everything below
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.01)

# --- 2. TIME TO TARGET ESTIMATOR ---
# Now this won't crash because buy_price exists!
if buy_price > 0:
    # (Your ATR and calculation logic here)
    st.write("Estimating flight path...")

# --- 3. TARGET ALPHA: THE 80% PATH ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")
