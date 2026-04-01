import streamlit as st  # <--- THIS IS THE MISSING KEY
import yfinance as yf

# --- GLOBAL INPUTS (Top of Script) ---
buy_price = st.sidebar.number_input("Enter Purchase Price", value=0.0, step=0.1)

# --- TARGET ALPHA: THE 80% PATH ---
st.header("🎯 Target Alpha: The 80% Path")

if buy_price > 0:
    # Your 80% and 100% logic follows...
    target_80 = buy_price * 1.80
    st.success(f"🚀 **80% Target:** ${round(target_80, 2)}")
