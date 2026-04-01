import streamlit as st
import yfinance as yf

# --- 1. GLOBAL INITIALIZATION (The Safety Net) ---
# Define these first so the script never sees an 'undefined' variable
buy_price = 0.0
atr = 0.1  # Set a small default to avoid division errors

# --- 2. SIDEBAR CONTROLS ---
# This is where the variable actually gets its value from you
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- 3. THE 80% PURSUIT LOGIC ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- 4. TIME TO TARGET (Moved BELOW the definitions) ---
    # Now this will NOT throw a NameError
    st.subheader("📅 Flight Estimate")
    # Add your distance and ATR logic here...
