# --- TIME TO TARGET ESTIMATOR ---
if buy_price > 0 and atr > 0:
    # How much price distance is left?
    distance_left = target_80 - curr_price
    
    # Estimate days based on current volatility (ATR)
    est_days = distance_left / atr
    
    st.subheader("📅 Target Timeline")
    if est_days > 0:
        st.write(f"At current volatility, the 'statistical path' to your 80% goal is roughly **{round(est_days)} market days**.")
        st.caption("Note: This assumes linear trend continuation. Market conditions vary.")
    else:
        st.success("🎯 You are currently beyond your 80% target area. Hold or reassess for 100%!")
