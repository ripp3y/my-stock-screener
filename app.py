# --- FLIGHT ESTIMATE LOGIC ---
if buy_price > 0 and atr > 0:
    # Current Price from yfinance
    current_price = info.get('currentPrice', buy_price)
    distance_to_target = target_80 - current_price
    
    # Simple Volatility Estimate
    days_to_target = distance_to_target / atr
    
    if days_to_target > 0:
        st.info(f"📅 **Estimated Arrival:** ~{int(days_to_target)} Trading Days")
    else:
        st.success("🎯 **Target Met!** Reassess for the 100% 'Moon' target.")
