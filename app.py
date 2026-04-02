# --- STEP 1: INITIALIZE (Must be Line 1) ---
import streamlit as st  #
import yfinance as yf

# --- STEP 2: USER ENTRY ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- STEP 3: ALPHA & VOLUME ENGINE ---
if buy_price > 0:
    # 80% Pursuit Logic
    target_80 = buy_price * 1.80
    st.header("🎯 Target Alpha: The 80% Path")
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- NEW: Institutional Volume Check ---
    st.subheader("📊 Institutional Heat Check")
    if 'info' in locals():
        avg_vol = info.get('averageVolume', 1)
        curr_vol = info.get('volume', 0)
        vol_ratio = curr_vol / avg_vol
        
        if vol_ratio > 1.5:
            st.metric("Volume Surge", f"{round(vol_ratio, 2)}x", delta="High Conviction")
        else:
            st.metric("Volume Surge", f"{round(vol_ratio, 2)}x", delta="Normal", delta_color="off")
