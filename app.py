def trade_scout():
    st.title("🔭 New Trade Scout: AI Infrastructure")
    
    # The 2026 High-Conviction List
    scout_list = ["BE", "MTZ", "CCJ"]
    
    for ticker in scout_list:
        t_obj = yf.Ticker(ticker)
        # Check volume over the last 10 trading days
        hist = t_obj.history(period="10d")
        avg_vol = hist['Volume'].mean()
        curr_vol = hist['Volume'].iloc[-1]
        vol_ratio = curr_vol / avg_vol
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if vol_ratio > 2.0:
                st.success(f"🔥 {ticker} VOLUME BREAKOUT!")
            elif vol_ratio > 1.5:
                st.warning(f"⚡ {ticker} Accumulating...")
            else:
                st.info(f"🔎 {ticker} Monitoring")
        
        with col2:
            st.write(f"**Current Price:** ${hist['Close'].iloc[-1]:.2f}")
            st.caption(f"Volume Ratio: {vol_ratio:.2f}x (Current vs 10-day Avg)")
