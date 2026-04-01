# --- 1. GET THE USER INPUT FIRST ---
buy_price = st.sidebar.number_input("Actual Purchase Price", value=0.0, step=0.1)

# --- 2. CALCULATE TARGETS ---
if buy_price > 0:
    target_80 = buy_price * 1.80
    st.success(f"🚀 **80% Target Price:** ${round(target_80, 2)}")

    # --- 3. THE FLIGHT ESTIMATE (The final step) ---
    st.subheader("📅 Flight Estimate")
    
    # Check if we have the volatility data (ATR) ready
    if 'atr' in locals() and atr > 0:
        # Get live price to see how far we have to go
        current_price = info.get('currentPrice', buy_price)
        dist_to_go = target_80 - current_price
        
        # Estimate days based on volatility
        days_est = dist_to_go / atr
        st.info(f"Estimated Arrival: ~{int(days_est)} Trading Days")
    else:
        st.warning("Fetch ATR data to calculate arrival timeline.")
