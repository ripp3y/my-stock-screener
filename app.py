import streamlit as st

# --- PROFIT TARGET LOGIC ---
st.header("🎯 Target Alpha: The 80% Path")

if buy_price > 0:
    # Calculate the 'Moon' price
    target_80 = buy_price * 1.80
    target_100 = buy_price * 2.00
    
    # Contextual Distance
    curr_price = info.get('currentPrice', 0)
    dist_to_80 = ((target_80 - curr_price) / curr_price) * 100
    
    st.subheader(f"Strategy for {target}")
    c1, c2, c3 = st.columns(3)
    
    c1.metric("80% Target", f"${round(target_80, 2)}", f"{round(dist_to_80, 1)}% away")
    c2.metric("100% Target", f"${round(target_100, 2)}", "The Double")
    
    # 52-Week Comparison
    high_52 = info.get('fiftyTwoWeekHigh', 1)
    if target_80 > high_52:
        st.info(f"🚀 **Breakout Required:** Your 80% target is above the 52-week high of ${high_52}. We are looking for a major structural move.")
    else:
        st.success(f"📈 **Recovery Play:** Your 80% target is within the yearly range. Reclaiming the high hits your goal.")

    # --- THE BOSS'S RISK/REWARD RATIO ---
    # Compare Stop Loss distance to Profit Target distance
    if 'stop_price' in locals():
        risk = buy_price - stop_price
        reward = target_80 - buy_price
        rr_ratio = reward / risk if risk > 0 else 0
        st.write(f"**Risk/Reward Ratio:** 1 : {round(rr_ratio, 1)}")
        
        if rr_ratio < 3:
            st.warning("⚠️ **Tight Ratio:** The volatility-adjusted stop is wide. Consider reducing position size to maintain the 80% goal.")
